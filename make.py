"""python make.py [--fake] [--only v1_profile_makeover]  -> output/<id>.mp4 + output/<id>.txt"""
import argparse
import subprocess
import sys
from pathlib import Path

import music
import scenes
import ui
from scripts import BRAND, ALL as VIDEOS
import voice

FPS = 24
OUT = Path(__file__).parent / "output"


def render(v, fake, tmp):
    sc = v["scenes"]
    durs, vwav, vname = voice.build([s["say"] for s in sc], tmp, fake)
    total = sum(durs)
    bgm = tmp / "bgm.wav"
    music.track(total + 1, abs(hash(v["id"])) % 9999, str(bgm))
    mix = tmp / "mix.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(vwav), "-i", str(bgm), "-filter_complex",
                    "[1:a]volume=0.16[b];[0:a][b]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[o]", "-map", "[o]", str(mix)], check=True)
    out = OUT / f"{v['id']}.mp4"
    OUT.mkdir(exist_ok=True)
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{ui.W}x{ui.H}", "-r", str(FPS), "-i", "-",
                          "-i", str(mix), "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
                          "-shortest", str(out)], stdin=subprocess.PIPE)
    for k, s in enumerate(sc):
        d = durs[k]
        for f in range(int(d * FPS)):
            t = f / FPS
            cv = ui.Cv()
            ui.header(cv, v["tag"], BRAND.upper())
            scenes.draw(cv, s, t, d)
            ui.subtitle(cv, s["say"], t, d)
            gt = sum(durs[:k]) + t
            cv.rr((34, 1236, 34 + (ui.W - 68) * gt / total, 1241), 3, fill=ui.CYAN)
            cv.text(ui.W / 2, 1262, BRAND, "latm", 11, ui.MUTE, "mm")
            p.stdin.write(cv.out().tobytes())
    p.stdin.close()
    p.wait()
    (OUT / f"{v['id']}.txt").write_text(v["caption"] + "\n\n" + v["tags"] + "\n\nVoice: " + vname + "\n", encoding="utf-8")
    print("done", out, f"{total:.1f}s", vname)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--fake", action="store_true")
    ap.add_argument("--only")
    a = ap.parse_args()
    import os
    scenes.HANDLE = os.getenv("IAA_HANDLE", "")
    for v in VIDEOS:
        if a.only and a.only != v["id"]:
            continue
        render(v, a.fake, Path("/tmp/iaa_tmp") / v["id"])
