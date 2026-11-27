"""Daily auto-post planner. Each run posts ONE item: today's plan = reel, reel, carousel, reel (max 4/day).
Reels: the 4 intro videos first, then fresh tip reels (Gemini topic + example + brand CTA). Carousel: tip carousel from the same kind of spec.
python post.py [--dry-run] [--force reel|carousel] [--diagnose] [--fake] [--reset]"""
import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import ig
import make
import scenes
import tips
from scripts import VIDEOS

STATE = Path(__file__).parent / "state.json"
PLAN = ["reel", "reel", "carousel", "reel"]
MAX_DAY = int(os.getenv("IAA_MAX_PER_DAY") or len(PLAN))


def load():
    try:
        return json.loads(STATE.read_text())
    except Exception:
        return {}


def save(st):
    STATE.write_text(json.dumps(st, ensure_ascii=False, indent=1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", choices=["reel", "carousel"])
    ap.add_argument("--diagnose", action="store_true")
    ap.add_argument("--fake", action="store_true")
    ap.add_argument("--reset", action="store_true")
    a = ap.parse_args()
    if a.diagnose:
        ig.diagnose()
        return
    if a.reset:
        save({})
        print("state reset")
        return
    st = load()
    today = (datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)).strftime("%Y-%m-%d")
    if st.get("day") != today:
        st["day"], st["count"] = today, 0
    if st["count"] >= MAX_DAY and not a.force:
        print(f"Already posted {st['count']} today. Nothing to do.")
        return
    kind = a.force or PLAN[st["count"] % len(PLAN)]
    scenes.HANDLE = os.getenv("IAA_HANDLE", "")
    posted = st.setdefault("posted", [])
    made = st.setdefault("made", [])
    if kind == "reel":
        intro = [v for v in VIDEOS if v["id"] not in posted]
        if intro:
            v, how = intro[0], "intro"
        else:
            spec, how = tips.pick(st)
            v = tips.video(spec)
        make.render(v, a.fake, Path("/tmp/iaa_tmp") / v["id"])
        mp4 = make.OUT / f"{v['id']}.mp4"
        cap = v["caption"] + "\n\n" + v["tags"]
        print(f"REEL {v['id']} ({how})")
        if a.dry_run:
            print("DRY RUN, not posting:", mp4)
            return
        pid = ig.reel(str(mp4), cap)
        (posted if how == "intro" else made).append(v["id"])
    else:
        spec, how = tips.pick(st)
        paths = tips.carousel(spec, make.OUT / f"car_{spec['id']}", os.getenv("IAA_HANDLE", ""))
        cap = spec["caption"] + "\n\n🔍 उदाहरण: " + spec["example"]["biz"] + " (काल्पनिक उदाहरण)\n\nतुमच्या ब्रँडसाठी असं करून हवं असेल तर Insta Automation AI ला मेसेज करा.\n\n" + spec["tags"]
        print(f"CAROUSEL {spec['id']} ({how}) slides={len(paths)}")
        if a.dry_run:
            print("DRY RUN, not posting")
            return
        pid = ig.carousel(paths, cap)
        made.append(spec["id"])
    st["count"] += 1
    save(st)
    print("POSTED", kind, pid)


if __name__ == "__main__":
    try:
        main()
    except ig.TokenError as ex:
        print("TOKEN PROBLEM:", ex, file=sys.stderr)
        sys.exit(1)
