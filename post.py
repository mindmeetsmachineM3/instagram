"""Auto-post: renders the next not-yet-posted video and publishes it as an Instagram Reel.
python post.py [--dry-run] [--force <video id>] [--diagnose] [--fake] [--reset]"""
import argparse
import json
import os
import sys
from pathlib import Path

import ig
import make
import scenes
from scripts import VIDEOS

STATE = Path(__file__).parent / "state.json"


def load():
    try:
        return json.loads(STATE.read_text())
    except Exception:
        return {"posted": []}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force")
    ap.add_argument("--diagnose", action="store_true")
    ap.add_argument("--fake", action="store_true")
    ap.add_argument("--reset", action="store_true")
    a = ap.parse_args()
    if a.diagnose:
        ig.diagnose()
        return
    st = load()
    if a.reset:
        st = {"posted": []}
        STATE.write_text(json.dumps(st))
        print("state reset")
        return
    todo = [v for v in VIDEOS if v["id"] not in st["posted"]]
    if a.force:
        todo = [v for v in VIDEOS if v["id"] == a.force]
    if not todo:
        print("All videos already posted. Add new videos in scripts.py (or run with reset).")
        return
    v = todo[0]
    scenes.HANDLE = os.getenv("IAA_HANDLE", "")
    make.render(v, a.fake, Path("/tmp/iaa_tmp") / v["id"])
    mp4 = make.OUT / f"{v['id']}.mp4"
    cap = v["caption"] + "\n\n" + v["tags"]
    if a.dry_run:
        print("DRY RUN, not posting:", mp4)
        return
    try:
        mid = ig.reel(str(mp4), cap)
    except ig.TokenError as ex:
        print("TOKEN PROBLEM:", ex, file=sys.stderr)
        sys.exit(1)
    st["posted"].append(v["id"])
    STATE.write_text(json.dumps(st))
    print("POSTED", v["id"], mid)


if __name__ == "__main__":
    main()
