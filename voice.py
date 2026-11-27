"""Narration: Gemini TTS (one request per video, cut at the pauses) with edge-tts fallback. Returns per-scene wav clips + durations."""
import asyncio
import base64
import os
import re
import subprocess
import sys
import time
import wave
from pathlib import Path

API = "https://generativelanguage.googleapis.com/v1beta"
VOICE = os.getenv("GEMINI_TTS_VOICE") or "Orus"
MODELS = [m for m in dict.fromkeys([os.getenv("GEMINI_TTS_MODEL") or "", "gemini-3.8-flash-tts", "gemini-3.8-flash-lite-tts"]) if m]
LEGACY = ["gemini-2.5-flash-preview-tts"]
STYLE = os.getenv("GEMINI_TTS_STYLE") or "a friendly, energetic young Indian male social-media coach speaking Marathi, clear and upbeat, confident and brisk, like a tech explainer reel"
EDGE_VOICE = os.getenv("EDGE_VOICE") or "mr-IN-ManoharNeural"
SPEED = float(os.getenv("IAA_SPEED") or 1.08)


def run(cmd):
    subprocess.run(cmd, check=True)


def dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return float(r.stdout.strip())


def _find(o):
    if isinstance(o, dict):
        if o.get("type") == "audio" and isinstance(o.get("data"), str):
            return o["data"]
        for k in ("inlineData", "inline_data"):
            if isinstance(o.get(k), dict) and isinstance(o[k].get("data"), str):
                return o[k]["data"]
        for v in o.values():
            r = _find(v)
            if r:
                return r
    elif isinstance(o, list):
        for v in reversed(o):
            r = _find(v)
            if r:
                return r


def _save(b64, out):
    raw = base64.b64decode(b64)
    if raw[:4] == b"RIFF":
        Path(out).write_bytes(raw)
    else:
        with wave.open(str(out), "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(raw)


def gemini(text, out):
    import requests
    hdr = {"x-goog-api-key": os.environ["GEMINI_API_KEY"], "Content-Type": "application/json"}
    errs, end = [], time.time() + 300
    for model in MODELS + LEGACY:
        legacy = "2.5" in model
        t = text.replace("<long pause>", "...") if legacy else text
        for att in range(4):
            if time.time() > end:
                raise RuntimeError("Gemini TTS out of time " + " | ".join(errs[-3:]))
            try:
                if legacy:
                    r = requests.post(f"{API}/models/{model}:generateContent", headers=hdr, timeout=180, json={
                        "contents": [{"parts": [{"text": f"Say in a {STYLE} tone: {t}"}]}],
                        "generationConfig": {"responseModalities": ["AUDIO"], "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": VOICE}}}}})
                else:
                    r = requests.post(f"{API}/interactions", headers=hdr, timeout=120, json={
                        "model": model,
                        "input": [{"type": "user_input", "content": [{"type": "text", "text": t, "annotations": [{"type": "speech_metadata", "style": STYLE}]}]}],
                        "response_format": {"type": "audio"},
                        "generation_config": {"speech_config": [{"voice": VOICE}]}})
            except requests.RequestException as ex:
                errs.append(f"{model}: net {str(ex)[:60]}"); time.sleep(5); continue
            if r.ok:
                d = None
                try:
                    d = _find(r.json())
                except Exception:
                    pass
                if d:
                    _save(d, out)
                    return f"gemini:{model}:{VOICE}"
                errs.append(f"{model}: no audio"); break
            errs.append(f"{model}: {r.status_code} {r.text[:100]}")
            if r.status_code == 429:
                if re.search(r"PerDay|per day|daily|limit: 0", r.text, re.I):
                    break
                time.sleep(min(60, 20 * (att + 1))); continue
            if r.status_code in (500, 502, 503, 504):
                time.sleep(8); continue
            break
    raise RuntimeError("Gemini TTS failed: " + " | ".join(errs[-4:]))


def silences(path, noise, d):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-af", f"silencedetect=noise={noise}dB:d={d}", "-f", "null", "-"], capture_output=True, text=True)
    out, st = [], None
    for ln in r.stderr.splitlines():
        m = re.search(r"silence_start: ([\d.]+)", ln)
        if m:
            st = float(m.group(1))
        m = re.search(r"silence_end: ([\d.]+) \| silence_duration: ([\d.]+)", ln)
        if m and st is not None:
            out.append((st, float(m.group(1)), float(m.group(2)))); st = None
    return out


def cuts_for(path, says, total):
    n = len(says)
    w = [len(s.split()) + 3 for s in says]
    est, acc = [], 0
    for x in w[:-1]:
        acc += x
        est.append(acc / sum(w) * total)
    for noise, d in ((-38, .30), (-34, .22), (-30, .15)):
        sil = silences(path, noise, d)
        if len(sil) < n - 1:
            continue
        top = sorted(sorted(sil, key=lambda x: -x[2])[:n - 1])
        cuts = [(a + b) / 2 for a, b, _ in top]
        e = [0.0] + cuts + [total]
        if all(.4 * (w[i] / sum(w) * total) <= e[i + 1] - e[i] <= 2.5 * (w[i] / sum(w) * total) + 1 for i in range(n)):
            return cuts
    return est


def edge_clip(text, out):
    import edge_tts
    async def go():
        await edge_tts.Communicate(text, EDGE_VOICE, rate="+8%").save(str(out))
    asyncio.run(go())


def clean(s):
    return s.replace("**", "")


def build(says, tmp, fake=False):
    """-> (scene durations, voice wav, voice name)"""
    tmp = Path(tmp); tmp.mkdir(parents=True, exist_ok=True)
    says = [clean(s) for s in says]
    raws, name = [], "silent-preview"
    if fake:
        for i, s in enumerate(says):
            p = tmp / f"f{i}.wav"
            run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", f"{max(2.6, len(s.split()) / 2.6):.2f}", str(p)])
            raws.append(p)
    else:
        try:
            if (os.getenv("IAA_TTS") or "gemini").lower() == "edge":
                raise RuntimeError("IAA_TTS=edge")
            full = tmp / "g.wav"
            name = gemini(" <long pause> ".join(says), full)
            total = dur(full)
            e = [0.0] + cuts_for(full, says, total) + [total]
            for i in range(len(says)):
                p = tmp / f"g{i}.wav"
                run(["ffmpeg", "-v", "error", "-y", "-i", str(full), "-ss", f"{e[i]:.3f}", "-to", f"{e[i + 1]:.3f}", "-ar", "44100", "-ac", "1", str(p)])
                raws.append(p)
        except Exception as ex:
            print("gemini voice failed, edge fallback:", str(ex)[:200], file=sys.stderr)
            raws, name = [], "edge:" + EDGE_VOICE
            for i, s in enumerate(says):
                p = tmp / f"e{i}.mp3"
                edge_clip(s, p)
                raws.append(p)
    trim = "silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.04,areverse,silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.04,areverse"
    flt = ("anull" if fake else trim) + ",equalizer=f=140:t=q:w=1.1:g=3,acompressor=threshold=-20dB:ratio=3:attack=8:release=120" + (f",atempo={SPEED}" if not fake else "")
    durs, wavs = [], []
    for i, p in enumerate(raws):
        a, b = tmp / f"t{i}.wav", tmp / f"s{i}.wav"
        run(["ffmpeg", "-v", "error", "-y", "-i", str(p), "-af", flt, "-ar", "44100", "-ac", "1", str(a)])
        d = max(2.6, dur(a) + .55)
        run(["ffmpeg", "-v", "error", "-y", "-i", str(a), "-af", "adelay=150|150,apad", "-t", f"{d:.3f}", "-ar", "44100", "-ac", "1", str(b)])
        durs.append(d); wavs.append(b)
    lst = tmp / "l.txt"
    lst.write_text("".join(f"file '{w}'\n" for w in wavs))
    full = tmp / "voice.wav"
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "44100", str(full)])
    return durs, full, name
