import math
import ui
from ui import *

HANDLE = ""


def big_text(cv, lines, t, y=330):
    for i, s in enumerate(lines):
        a = pr(t, .1 + i * .25, .6 + i * .25)
        col = CYAN if i else WHITE
        cv.text(W / 2, y + i * 110 + (1 - a) * 40, s, "lat", 74 if len(s) < 9 else 64, col + (int(255 * a),), "mm")


def draw(cv, sc, t, dur):
    v = sc["vis"]
    if v == "hook":
        a = pr(t, 0, .6)
        cv.ell(W / 2, 220, 52 * a + 1, fill=CYAN)
        icon(cv, "bolt", W / 2, 220, 26 * a, INK)
        big_text(cv, sc["big"] if "big" in sc else ["?"], t)
        cv.rr((W / 2 - 60, 560, W / 2 + 60, 566), 3, fill=VIOLET)
        for i, (ic, c) in enumerate((("eye", CYAN), ("heart", PINK), ("chat", VIOLET))):
            a = pr(t, .6 + i * .25, 1.1 + i * .25)
            cv.ell(W / 2 - 150 + i * 150, 700, 52 * a + 1, fill=c)
            icon(cv, ic, W / 2 - 150 + i * 150, 700, 26 * a, INK)
    elif v == "phone":
        x, y, w, h = 190, 105, 340, 740
        sx = pr(t, 0, .5)
        box = phone(cv, x, y + (1 - sx) * 40, w, h)
        box = (box[0], box[1], box[2], box[3])
        rv = sc.get("reveal", [0.2, 0.6, 1.0, 1.4, 1.9])
        profile(cv, box, t, sc["style"], rv, full=sc.get("full", False))
        chip(cv, W / 2, 80, sc["label"], 17, CYAN if sc["style"] == "clean" else PINK, INK)
    elif v == "compare":
        for i, st in enumerate(("random", "clean")):
            a = pr(t, i * .3, i * .3 + .6)
            x = 50 + i * 330
            box = phone(cv, x, 190 + (1 - a) * 40, 280, 600, a)
            profile(cv, box, 9, st, full=True) if a > .98 else None
            chip(cv, x + 140, 150, "A" if i == 0 else "B", 18, PINK if i == 0 else CYAN, INK, a)
        cv.text(W / 2, 830, "VS", "lat", 22, MUTE, "mm")
    elif v == "cards":
        items = sc["items"]
        for i, it in enumerate(items):
            a = pr(t, .2 + i * .35, .7 + i * .35)
            yy = 160 + i * 220 + (1 - a) * 30
            cv.glass((90, yy, 630, yy + 180), 22, fill=CARD2 + (int(255 * a),), outline=LINE + (int(255 * a),))
            cv.ell(180, yy + 90, 46, fill=(CYAN, VIOLET, PINK)[i % 3] + (int(255 * a),))
            icon(cv, it[0], 180, yy + 90, 24, INK)
            cv.text(255, yy + 70, it[1], "lat", 34, WHITE + (int(255 * a),), "lm")
            cv.text(255, yy + 116, it[2], "latm", 20, MUTE + (int(255 * a),), "lm")
            if i < len(items) - 1 and a > .9:
                cv.line([(360, yy + 180), (360, yy + 218)], CYAN, 3)
    elif v == "checks":
        check_list(cv, 90, 210, sc["items"], t, .2, 540, 130)
    elif v == "bars":
        n = len(sc["vals"])
        cv.glass((70, 160, 650, 800), 26)
        bar_chart(cv, (130, 250, 590, 680), sc["vals"], t, CYAN, .2)
        gw = 460 / n
        for i, l in enumerate(sc["labels"]):
            cv.text(130 + i * gw + gw / 2, 715, l, "lat", 18, WHITE, "mm")
        chip(cv, W / 2, 200, sc.get("note", "SAMPLE"), 14, AMBER, INK)
    elif v == "cta_phone":
        box = phone(cv, 190, 130, 340, 700)
        x0, y0, x1, y1 = box
        cv.rr((x0 + 16, y0 + 20, x1 - 16, y0 + 380), 18, fill=(30, 20, 90))
        p = (t * .6) % 1
        cv.ell((x0 + x1) / 2, y0 + 200, 44, fill=(255, 255, 255, 40))
        icon(cv, "play", (x0 + x1) / 2, y0 + 200, 30, WHITE)
        cv.rr((x0 + 30, y0 + 360, x0 + 30 + (x1 - x0 - 60) * p, y0 + 366), 3, fill=CYAN)
        for i, (lab, c) in enumerate((("Message", CYAN), ("Call", VIOLET), ("Book", PINK))):
            a = pr(t, .6 + i * .35, 1 + i * .35)
            bx = x0 + 22 + i * 100
            cv.rr((bx, y0 + 420 + (1 - a) * 30, bx + 92, y0 + 466 + (1 - a) * 30), 14, fill=c + (int(255 * a),))
            cv.text(bx + 46, y0 + 443 + (1 - a) * 30, lab, "lat", 15, INK + (int(255 * a),), "mm")
        chip(cv, W / 2, 90, "ONE CLEAR ACTION", 16, CYAN, INK)
    elif v == "toggle":
        toggle(cv, W / 2, 400, pr(t, 1.2, 1.9))
        for i, (ic, s) in enumerate((("cal", "Plan"), ("play", "Create"), ("chat", "Post"))):
            a = pr(t, 1.8 + i * .25, 2.3 + i * .25)
            cx = 150 + i * 210
            cv.glass((cx - 80, 620, cx + 80, 760), 22, fill=CARD2 + (int(255 * a),))
            icon(cv, ic, cx, 670, 24, CYAN)
            cv.text(cx, 725, s, "lat", 20, WHITE + (int(255 * a),), "mm")
    elif v == "loop":
        loop_diagram(cv, W / 2, 440, t)
    elif v == "ring":
        p = pr(t, .3, 1.6)
        ring(cv, W / 2, 400, 150, p, f"{int(p * 100)}%", CYAN, 18)
        chip(cv, W / 2, 640, sc.get("label", "DONE"), 22, GREEN, INK, pr(t, 1.4, 1.9))
    elif v == "brand":
        brand_card(cv, W / 2, 440, t, handle=HANDLE)
