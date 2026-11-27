"""Daily tip content: every post teaches one thing, shows an EXAMPLE business, and ends with a brand-it-for-you CTA.
Gemini writes a fresh spec per topic; if it fails, a hand-written fallback bank is used. Reel + carousel both come from the same spec."""
import json
import os
import random
import re
import sys
import time
from pathlib import Path

import ui
from ui import *
from scripts import BRAND

TOPICS = [
    "Instagram bio कसा लिहायचा", "Highlights मध्ये काय ठेवायचं", "रील्सचा पहिला 3 सेकंदांचा hook", "कॅप्शन मध्ये CTA कसा लिहायचा",
    "हॅशटॅग कसे निवडायचे", "पोस्टिंगची योग्य वेळ आणि सातत्य", "DM ला पटकन उत्तर देण्याची सिस्टीम", "Google Maps आणि Instagram एकत्र वापरणं",
    "ग्राहकांचे रिव्ह्यू पोस्ट म्हणून वापरणं", "एका व्हिडिओचे 5 कंटेंट तुकडे", "कंटेंट कॅलेंडर कसं बनवायचं", "ऑफर पोस्ट कशी डिझाइन करायची",
    "Before-After पोस्टची ताकद", "Stories मधून ग्राहकांशी संवाद", "कॅरोसेल पोस्ट का चालतात", "प्रोफाइल फोटो आणि ब्रँड कलर्स",
    "लोकल बिझनेससाठी लोकेशन टॅग", "ट्रेंडिंग ऑडिओ कधी वापरावा", "Insights मधून काय बघायचं", "WhatsApp बटण आणि लिंक सेटअप",
    "प्रश्न-उत्तर कंटेंट (FAQ)", "पडद्यामागचं (behind the scenes) कंटेंट", "फेस्टिवल ऑफर्सची आधीपासून तयारी", "कॉम्पिटिटर्सकडून शिकण्याची पद्धत",
    "ग्राहकाची समस्या हाच कंटेंट", "पिन्ड पोस्ट्सचा वापर", "रील कव्हर आणि थंबनेल", "एकसारखा फॉन्ट आणि रंग", "कलेक्शन पोस्ट्स (सिरीज) बनवणं", "कमी बजेटमध्ये प्रोफेशनल लूक",
]

FALLBACK = [
 {"title": "Better Bio", "hook": "तुमचा **बायो** ग्राहकाला ५ सेकंदात पटवतो का?", "problem": "बायोमध्ये फक्त नाव असेल तर ग्राहकाला तुम्ही काय करता हेच कळत नाही.",
  "steps": [{"t": "WHAT", "say": "पहिल्या ओळीत तुम्ही **काय** विकता ते सांगा."}, {"t": "FOR WHOM", "say": "दुसऱ्या ओळीत ते **कुणासाठी** आहे आणि कोणत्या शहरात ते लिहा."}, {"t": "ACTION", "say": "शेवटी एकच **कृती** द्या, जसं की मेसेज करा किंवा बुक करा."}],
  "example": {"biz": "Home Bakery", "before": "Sweet Treats", "after": "Custom cakes · Kolhapur · DM to order"},
  "caption": "बायो ५ सेकंदात काम करतो: काय, कुणासाठी, आणि पुढची कृती.", "tags": "#instagrambio #instagramtips #marathi #smallbusiness #instaautomationai"},
 {"title": "Hook First", "hook": "रीलचे पहिले ३ सेकंद **ठरवतात** पुढे काय होणार.", "problem": "सुरुवात हळू असेल तर लोक स्क्रोल करून पुढे निघून जातात.",
  "steps": [{"t": "QUESTION", "say": "सुरुवात ग्राहकाच्या **प्रश्नाने** किंवा समस्येने करा."}, {"t": "PROMISE", "say": "लगेच सांगा की पुढे काय **फायदा** मिळणार आहे."}, {"t": "VISUAL", "say": "पहिल्याच फ्रेममध्ये मोठा **मजकूर** आणि स्पष्ट दृश्य ठेवा."}],
  "example": {"biz": "Salon", "before": "Hello friends, welcome", "after": "Hair fall? Fix it in 3 steps"},
  "caption": "रीलचा पहिला hook = प्रश्न + फायदा + मोठा मजकूर.", "tags": "#reelstips #hook #instagramreels #marathi #instaautomationai"},
 {"title": "Offer Post", "hook": "ऑफर पोस्ट **दिसते** पण विकली जाते का?", "problem": "रंग, मजकूर आणि तारीख गोंधळलेली असेल तर ग्राहक ऑफर समजतच नाही.",
  "steps": [{"t": "ONE OFFER", "say": "एका पोस्टमध्ये एकच **ऑफर** ठेवा."}, {"t": "DEADLINE", "say": "**शेवटची तारीख** ठळक लिहा, म्हणजे घाई निर्माण होते."}, {"t": "HOW TO", "say": "कसं मिळवायचं ते सोप्या शब्दात सांगा: **DM करा**."}],
  "example": {"biz": "Gym", "before": "Big discount on membership", "after": "20% off · till 30 Nov · DM JOIN"},
  "caption": "एक ऑफर, एक तारीख, एक कृती.", "tags": "#offers #marketing #instagrampost #marathi #instaautomationai"},
 {"title": "Reply Fast", "hook": "ग्राहकाचा **DM** आला आणि तुम्ही उशिरा उत्तर दिलं?", "problem": "उशिरा उत्तर दिल्यावर ग्राहक दुसऱ्याकडे जातो.",
  "steps": [{"t": "SAVED REPLIES", "say": "नेहमीच्या प्रश्नांची **तयार उत्तरं** ठेवा."}, {"t": "QUICK LINKS", "say": "किंमत, लोकेशन आणि बुकिंगची **लिंक** तयार ठेवा."}, {"t": "AUTO WELCOME", "say": "पहिला **स्वागत संदेश** आपोआप जाईल असं सेट करा."}],
  "example": {"biz": "Clinic", "before": "Reply after 1 day", "after": "Instant reply with timings & booking link"},
  "caption": "तयार उत्तरं + लिंक + आपोआप स्वागत संदेश.", "tags": "#dmautomation #customerservice #instagramtips #marathi #instaautomationai"},
]

PROMPT = """तुम्ही मराठी Instagram मार्केटिंग शिक्षक आहात. विषय: "{topic}". लहान बिझनेस मालकांसाठी एक छोटा रील/कॅरोसेल लिहा.
फक्त JSON द्या:
{{"title":"2-3 English words","hook":"मराठी, 8-14 शब्द, एक-दोन महत्त्वाचे शब्द **असे** लिहा","problem":"मराठी, 10-16 शब्द",
"steps":[{{"t":"1-2 English words","say":"मराठी, 10-18 शब्द, एक शब्द **असा**"}} x3],
"example":{{"biz":"2-3 English words (a typical local business e.g. Cafe, Salon, Gym)","before":"English, max 6 words","after":"English, max 9 words"}},
"caption":"मराठी, 1-2 वाक्ये","tags":"#instagramtips #marathi #instaautomationai + 2-3 more"}}
नियम: खोटे आकडे, खोटे निकाल किंवा वचनं नाहीत. उदाहरण काल्पनिक असल्याचं मान्य आहे. स्पष्ट, सोपी, बोलीभाषेतली मराठी. English शब्द (Instagram, DM, reel) देवनागरी वाक्यात चालतील."""


def validate(s):
    try:
        assert s["title"] and len(s["hook"].split()) <= 18 and len(s["problem"].split()) <= 20
        assert len(s["steps"]) == 3 and all(x["t"] and 4 <= len(x["say"].split()) <= 24 for x in s["steps"])
        ex = s["example"]
        assert ex["biz"] and ex["before"] and ex["after"] and len(ex["after"].split()) <= 12
        assert s["caption"] and "#" in s["tags"]
        txt = json.dumps(s, ensure_ascii=False)
        assert re.search(r"[ऀ-ॿ]", s["hook"]) and not re.search(r"\d+\s*(x|X|%|लाख|हजार)\s*(ग्राहक|sales|followers)", txt)
        return True
    except Exception:
        return False


def gen(topic):
    import requests
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        return None
    models = [m for m in (os.getenv("PAGE_MODELS") or "gemini-3.6-flash,gemini-3.5-flash,gemini-3.7-flash").split(",") if m]
    end = time.time() + 120
    for m in models * 2:
        if time.time() > end:
            break
        try:
            r = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent", headers={"x-goog-api-key": key, "Content-Type": "application/json"},
                              json={"contents": [{"parts": [{"text": PROMPT.format(topic=topic)}]}], "generationConfig": {"temperature": .8, "responseMimeType": "application/json"}}, timeout=60)
            if r.ok:
                t = "".join(p.get("text", "") for p in r.json()["candidates"][0]["content"]["parts"])
                s = json.loads(t[t.index("{"): t.rindex("}") + 1])
                if validate(s):
                    return s
                print("tips: spec failed validation", file=sys.stderr)
            else:
                print("tips:", m, r.status_code, file=sys.stderr)
        except Exception as ex:
            print("tips:", m, str(ex)[:100], file=sys.stderr)
        time.sleep(2)
    return None


def pick(state, rng=random):
    """-> (spec, source) choosing an unused topic; fallback bank if Gemini fails"""
    used = state.setdefault("used_topics", [])
    left = [t for t in TOPICS if t not in used] or (used.clear() or TOPICS[:])
    topic = rng.choice(left)
    s = gen(topic)
    if s:
        used.append(topic)
        s["id"] = f"t{len(state.get('made', []))}_{abs(hash(topic)) % 9999}"
        return s, "gemini"
    fb = [f for f in FALLBACK if f["title"] not in state.setdefault("used_fb", [])] or FALLBACK
    s = dict(rng.choice(fb))
    state["used_fb"].append(s["title"])
    s["id"] = f"fb_{s['title'].replace(' ', '')}_{len(state['used_fb'])}"
    return s, "fallback"


def video(s):
    st = s["steps"]
    sc = [{"say": s["hook"], "vis": "tip_hook", "big": s["title"].upper().split(" ", 1) if " " in s["title"] else [s["title"].upper()]},
          {"say": s["problem"], "vis": "tip_problem"}]
    for i, x in enumerate(st):
        sc.append({"say": x["say"], "vis": "tip_step", "n": i + 1, "t": x["t"].upper(), "ex": s["example"]})
    sc.append({"say": f"एक उदाहरण पाहू: {s['example']['biz']}. आधी असं होतं आणि आता असं दिसतं.", "vis": "tip_example", "ex": s["example"]})
    sc.append({"say": "तुमच्या ब्रँडसाठी असं **ब्रँडिंग** करायचं असेल तर **Insta Automation AI** ला मेसेज करा.", "vis": "brand", "line": "We can brand this for your business"})
    return {"id": s["id"], "title": s["title"], "tag": s["title"].upper(), "scenes": sc,
            "caption": s["caption"] + "\n\n🔍 उदाहरण: " + s["example"]["biz"] + " (काल्पनिक उदाहरण)\n\nतुमच्या ब्रँडसाठी असं करून हवं असेल तर Insta Automation AI ला मेसेज करा.", "tags": s["tags"]}


# ------------------------------------------------------------------ scene drawing (used by scenes.draw)
def draw_tip(cv, sc, t, dur, W_=720, base=0):
    v = sc["vis"]
    if v == "tip_problem":
        a = pr(t, 0, .5)
        cv.ell(W_ / 2, 360, 120 * a + 1, fill=PINK + (60,), outline=PINK, w=5)
        cv.line([(W_ / 2 - 46, 314), (W_ / 2 + 46, 406)], PINK, 12)
        cv.line([(W_ / 2 + 46, 314), (W_ / 2 - 46, 406)], PINK, 12)
        chip(cv, W_ / 2, 560, "THE PROBLEM", 20, PINK, INK, pr(t, .5, 1))
    elif v == "tip_step":
        n = sc["n"]
        for i in range(3):
            cv.ell(W_ / 2 - 60 + i * 60, 140, 9, fill=CYAN if i < n else LINE)
        a = pr(t, 0, .5)
        cv.ell(W_ / 2, 330, 90 * a + 1, fill=CYAN)
        cv.text(W_ / 2, 330, str(n), "lat", max(4, 92 * a), INK, "mm")
        cv.text(W_ / 2, 500, sc["t"], "lat", 44, WHITE, "mm")
        b = pr(t, .5, 1.1)
        cv.glass((90, 590, 630, 760), 22, fill=CARD2 + (int(255 * b),), outline=LINE + (int(255 * b),))
        cv.text(110, 620, "EXAMPLE · " + sc["ex"]["biz"].upper(), "lat", 14, AMBER + (int(255 * b),))
        cv.text(W_ / 2, 690, sc["ex"]["after"], "latm", 22, WHITE + (int(255 * b),), "mm")
    elif v == "tip_example":
        ex = sc["ex"]
        chip(cv, W_ / 2, 130, "EXAMPLE · " + ex["biz"].upper(), 17, AMBER, INK)
        for i, (lab, txt, c) in enumerate((("BEFORE", ex["before"], PINK), ("AFTER", ex["after"], CYAN))):
            a = pr(t, .3 + i * .7, .9 + i * .7)
            y = 220 + i * 290 + (1 - a) * 30
            cv.glass((70, y, 650, y + 230), 24, fill=CARD2 + (int(255 * a),), outline=c + (int(255 * a),), glow=None)
            cv.text(100, y + 34, lab, "lat", 20, c + (int(255 * a),))
            cv.text(W_ / 2, y + 140, txt, "latm", 26, WHITE + (int(255 * a),), "mm")
        cv.text(W_ / 2, 830, "ILLUSTRATIVE EXAMPLE", "lat", 13, MUTE, "mm")


# ------------------------------------------------------------------ carousel (720x900 -> 1080x1350)
def carousel(s, out_dir, handle=""):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    H4 = 900
    slides = []

    def base(label):
        cv = Cv(H4)
        ui.header(cv, label, BRAND.upper())
        return cv

    def wrap(cv, text, y, size, col=WHITE):
        words = parse(text)
        for ln in sub_lines(cv, words, size, 600):
            tot = sum(w for _, _, w in ln) + cv.tw(" ", "lat", size) * (len(ln) - 1)
            x = W / 2 - tot / 2
            for w, acc, ww in ln:
                cv.text(x, y, w, "dev" if is_dev(w) else "lat", size, CYAN if acc else col)
                x += ww + cv.tw(" ", "lat", size)
            y += size * 1.6
        return y

    cv = base("SWIPE ➜".replace("➜", ">"))
    cv.ell(W / 2, 220, 52, fill=CYAN); icon(cv, "bolt", W / 2, 220, 26, INK)
    cv.text(W / 2, 360, s["title"].upper(), "lat", 62, WHITE, "mm")
    wrap(cv, s["hook"], 450, 36)
    chip(cv, W / 2, 800, "SWIPE  >", 20, VIOLET, WHITE)
    slides.append(cv)
    cv = base("THE PROBLEM")
    cv.ell(W / 2, 250, 90, fill=PINK + (60,), outline=PINK, w=5)
    cv.line([(W / 2 - 34, 216), (W / 2 + 34, 284)], PINK, 10); cv.line([(W / 2 + 34, 216), (W / 2 - 34, 284)], PINK, 10)
    wrap(cv, s["problem"], 430, 34)
    slides.append(cv)
    for i, x in enumerate(s["steps"]):
        cv = base(f"STEP {i + 1} / 3")
        cv.ell(W / 2, 220, 70, fill=CYAN); cv.text(W / 2, 220, str(i + 1), "lat", 72, INK, "mm")
        cv.text(W / 2, 340, x["t"].upper(), "lat", 40, WHITE, "mm")
        wrap(cv, x["say"], 420, 32)
        cv.glass((70, 700, 650, 820), 20, fill=CARD2)
        cv.text(95, 720, "EXAMPLE · " + s["example"]["biz"].upper(), "lat", 13, AMBER)
        cv.text(W / 2, 775, s["example"]["after"], "latm", 20, WHITE, "mm")
        slides.append(cv)
    cv = base("EXAMPLE")
    chip(cv, W / 2, 130, s["example"]["biz"].upper(), 18, AMBER, INK)
    for i, (lab, txt, c) in enumerate((("BEFORE", s["example"]["before"], PINK), ("AFTER", s["example"]["after"], CYAN))):
        y = 200 + i * 270
        cv.glass((60, y, 660, y + 220), 24, fill=CARD2, outline=c)
        cv.text(90, y + 30, lab, "lat", 20, c)
        cv.text(W / 2, y + 130, txt, "latm", 26, WHITE, "mm")
    cv.text(W / 2, 810, "ILLUSTRATIVE EXAMPLE", "lat", 12, MUTE, "mm")
    slides.append(cv)
    cv = base("YOUR BRAND")
    brand_card(cv, W / 2, 420, 9, line="We can brand this for your business", handle=handle)
    slides.append(cv)
    paths = []
    for i, c in enumerate(slides):
        p = out_dir / f"slide_{i + 1:02d}.jpg"
        c.out(1.5).save(p, quality=92)
        paths.append(str(p))
    return paths
