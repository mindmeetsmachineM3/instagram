"""Drawing kit for the Insta Automation AI explainer videos: midnight-indigo background, cyan + violet + pink accents, phone mock-ups and clean UI cards.
Everything is drawn at 2x and scaled down (smooth edges). Components take t (seconds in the scene) so they animate."""
import math
import random
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).parent
W, H = 720, 1280
S = 2
BG1, BG2 = (8, 11, 36), (26, 14, 70)
CYAN, VIOLET, PINK, AMBER = (46, 226, 232), (146, 112, 255), (255, 96, 170), (255, 196, 70)
WHITE, MUTE = (246, 247, 255), (150, 160, 205)
CARD, CARD2, LINE = (19, 25, 62), (30, 38, 88), (58, 70, 130)
INK = (16, 20, 44)
GREEN = (60, 220, 150)


def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def pr(t, a, b):
    """progress 0..1 of t between a and b (eased)"""
    return ease((t - a) / max(1e-6, b - a))


def lerp(a, b, k):
    return a + (b - a) * k


def mixc(a, b, k):
    return tuple(int(lerp(a[i], b[i], k)) for i in range(3))


@lru_cache(maxsize=None)
def F(kind, size):
    p = {"lat": "Poppins-Bold.ttf", "latm": "Poppins-Medium.ttf", "dev": "NotoSansDevanagari-Bold.ttf"}[kind]
    return ImageFont.truetype(str(BASE / "fonts" / p), int(size * S))


def is_dev(s):
    return any("ऀ" <= c <= "ॿ" for c in s)


def wfont(word, size, light=False):
    return F("dev", size) if is_dev(word) else F("latm" if light else "lat", size)


_BG = {}


def background():
    if "im" not in _BG:
        w, h = W * S, H * S
        ys = [i / (h - 1) for i in range(h)]
        col = Image.new("RGB", (1, h))
        col.putdata([mixc(BG1, BG2, y ** 1.4) for y in ys])
        im = col.resize((w, h)).convert("RGB")
        d = ImageDraw.Draw(im, "RGBA")
        for cx, cy, r, c, a in ((120, 1050, 380, VIOLET, 46), (640, 180, 300, CYAN, 30), (560, 1180, 260, PINK, 28)):
            for k in range(14, 0, -1):
                rr = r * k / 14 * S
                d.ellipse((cx * S - rr, cy * S - rr, cx * S + rr, cy * S + rr), fill=c + (int(a / 14 * 1.4),))
        for gx in range(0, W, 48):                                   # faint grid
            d.line((gx * S, 0, gx * S, h), fill=(255, 255, 255, 7), width=1)
        for gy in range(0, H, 48):
            d.line((0, gy * S, w, gy * S), fill=(255, 255, 255, 7), width=1)
        _BG["im"] = im
    return _BG["im"]


class Cv:
    def __init__(self, h=H):
        self.h = h
        self.im = background().crop((0, 0, W * S, h * S))  # RGB so translucent fills blend
        self.d = ImageDraw.Draw(self.im, "RGBA")

    def s(self, v):
        return v * S

    def rr(self, box, r=14, fill=None, outline=None, w=0):
        self.d.rounded_rectangle([self.s(v) for v in box], self.s(r), fill=fill, outline=outline, width=int(self.s(w)) if w else 0)

    def ell(self, cx, cy, r, fill=None, outline=None, w=0):
        self.d.ellipse((self.s(cx - r), self.s(cy - r), self.s(cx + r), self.s(cy + r)), fill=fill, outline=outline, width=int(self.s(w)) if w else 0)

    def line(self, pts, fill, w=2):
        self.d.line([(self.s(x), self.s(y)) for x, y in pts], fill=fill, width=int(self.s(w)), joint="curve")

    def poly(self, pts, fill, outline=None):
        self.d.polygon([(self.s(x), self.s(y)) for x, y in pts], fill=fill, outline=outline)

    def arc(self, cx, cy, r, a0, a1, fill, w=6):
        self.d.arc((self.s(cx - r), self.s(cy - r), self.s(cx + r), self.s(cy + r)), a0, a1, fill=fill, width=int(self.s(w)))

    def text(self, x, y, s, kind="lat", size=20, fill=WHITE, anchor="la"):
        if is_dev(s) and any(c.isascii() and c.isalpha() for c in s):
            parts = s.split(" ")
            fonts = [F("dev" if is_dev(p) else "lat", size) for p in parts]
            sp = self.d.textlength(" ", font=F("dev", size)) / S
            ws = [self.d.textlength(p, font=f) / S for p, f in zip(parts, fonts)]
            tot = sum(ws) + sp * (len(parts) - 1)
            x0 = x - tot / 2 if anchor[0] == "m" else (x - tot if anchor[0] == "r" else x)
            va = "m" + anchor[1] if anchor[1] in "mb" else "l" + anchor[1]
            for p, f, w_ in zip(parts, fonts, ws):
                self.d.text((self.s(x0), self.s(y)), p, font=f, fill=fill, anchor="l" + anchor[1])
                x0 += w_ + sp
            return
        if is_dev(s):
            kind = "dev"
        self.d.text((self.s(x), self.s(y)), s, font=F(kind, size), fill=fill, anchor=anchor)

    def tw(self, s, kind, size):
        return self.d.textlength(s, font=F(kind, size)) / S

    def glass(self, box, r=18, fill=CARD, outline=LINE, w=1.5, glow=None):
        x0, y0, x1, y1 = box
        if glow:
            for k in range(6, 0, -1):
                self.rr((x0 - k * 2, y0 - k * 2, x1 + k * 2, y1 + k * 2), r + k * 2, outline=glow + (int(26 / k),), w=2)
        self.rr(box, r, fill=fill, outline=outline, w=w)

    def paste(self, im, x, y, alpha=1.0):
        if alpha < 1:
            im = im.copy()
            im.putalpha(im.getchannel("A").point(lambda v: int(v * alpha)))
        self.im.paste(im, (int(x * S), int(y * S)), im)

    def out(self, scale=1.0):
        return self.im.resize((int(W * scale), int(self.h * scale)), Image.LANCZOS).convert("RGB")


# ------------------------------------------------------------------ text with mixed Marathi + English words, **accent** words
def parse(text):
    out = []
    for w in text.split():
        acc = w.startswith("**") or w.endswith("**") or (out and out[-1][2] and not out[-1][3])
        out.append([w.replace("**", ""), None, False, False])
    res, on = [], False
    for w in text.split():
        n = w.count("**")
        if n == 1 and not on or n == 2:
            on = True if n == 1 else on
        cur = on or n == 2
        if n == 1 and on and w.startswith("**") is False:
            pass
        res.append((w.replace("**", ""), cur))
        if n == 1 and not w.startswith("**"):
            on = False
        elif n == 1:
            on = True
    return res


def sub_lines(cv, words, size, maxw):
    lines, cur, curw = [], [], 0.0
    sp = cv.tw(" ", "lat", size)
    for w, acc in words:
        ww = cv.tw(w, "dev" if is_dev(w) else "lat", size)
        if cur and curw + sp + ww > maxw:
            lines.append(cur)
            cur, curw = [], 0.0
        cur.append((w, acc, ww))
        curw += (sp if len(cur) > 1 else 0) + ww
    if cur:
        lines.append(cur)
    return lines


def subtitle(cv, text, t, dur, y=905, size=31):
    """words appear as they are spoken; the ones marked ** are cyan"""
    words = parse(text)
    if not words:
        return
    lines = sub_lines(cv, words, size, 600)
    n = len(words)
    start, end = 0.15, max(1.2, dur - 0.5)
    wts = [len(w) + 2 for w, _ in words]
    tot, acc_t, marks = sum(wts), 0.0, []
    for w in wts:
        marks.append(start + (end - start) * acc_t / tot)
        acc_t += w
    sp = cv.tw(" ", "lat", size)
    y0 = y - max(0, len(lines) - 3) * 22
    k = 0
    for ln in lines:
        total_w = sum(w for _, _, w in ln) + sp * (len(ln) - 1)
        x = W / 2 - total_w / 2
        for w, acc, ww in ln:
            a = ease((t - marks[k]) / .22)
            if a > 0:
                col = (CYAN if acc else WHITE) + (int(255 * a),)
                cv.text(x, y0 + (1 - a) * 8, w, "dev" if is_dev(w) else "lat", size, col)
            x += ww + sp
            k += 1
        y0 += size * 1.55
    return


# ------------------------------------------------------------------ small pieces
def chip(cv, cx, cy, s, size=19, fill=CYAN, fg=INK, a=1.0):
    w = cv.tw(s, "lat", size) + 30
    h = size + 20
    cv.rr((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), h / 2, fill=fill + (int(255 * a),))
    cv.text(cx, cy, s, "lat", size, fg + (int(255 * a),), "mm")
    return w


def icon(cv, name, cx, cy, r, col=WHITE):
    if name == "play":
        cv.poly([(cx - r * .35, cy - r * .5), (cx - r * .35, cy + r * .5), (cx + r * .55, cy)], col)
    elif name == "star":
        pts = []
        for i in range(10):
            a = -math.pi / 2 + i * math.pi / 5
            rr = r if i % 2 == 0 else r * .45
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        cv.poly(pts, col)
    elif name == "pin":
        cv.ell(cx, cy - r * .2, r * .55, fill=col)
        cv.poly([(cx - r * .45, cy), (cx + r * .45, cy), (cx, cy + r * .8)], col)
        cv.ell(cx, cy - r * .2, r * .2, fill=INK)
    elif name == "menu":
        for k in (-.5, 0, .5):
            cv.rr((cx - r * .7, cy + k * r - r * .1, cx + r * .7, cy + k * r + r * .1), 2, fill=col)
    elif name == "heart":
        cv.ell(cx - r * .3, cy - r * .2, r * .38, fill=col)
        cv.ell(cx + r * .3, cy - r * .2, r * .38, fill=col)
        cv.poly([(cx - r * .64, cy - r * .02), (cx + r * .64, cy - r * .02), (cx, cy + r * .72)], col)
    elif name == "chat":
        cv.rr((cx - r * .7, cy - r * .5, cx + r * .7, cy + r * .35), r * .25, fill=col)
        cv.poly([(cx - r * .3, cy + r * .3), (cx - r * .5, cy + r * .75), (cx + r * .05, cy + r * .3)], col)
    elif name == "check":
        cv.line([(cx - r * .55, cy), (cx - r * .1, cy + r * .45), (cx + r * .6, cy - r * .45)], col, 3.2)
    elif name == "bolt":
        cv.poly([(cx + r * .1, cy - r * .8), (cx - r * .5, cy + r * .1), (cx, cy + r * .1), (cx - r * .1, cy + r * .8), (cx + r * .5, cy - r * .1), (cx, cy - r * .1)], col)
    elif name == "cal":
        cv.rr((cx - r * .7, cy - r * .6, cx + r * .7, cy + r * .7), r * .15, outline=col, w=2.4)
        cv.rr((cx - r * .7, cy - r * .6, cx + r * .7, cy - r * .2), r * .1, fill=col)
    elif name == "bars":
        for i, hh in enumerate((.4, .75, 1.1)):
            cv.rr((cx - r * .7 + i * r * .55, cy + r * .6 - r * hh, cx - r * .3 + i * r * .55, cy + r * .6), 2, fill=col)
    elif name == "user":
        cv.ell(cx, cy - r * .25, r * .35, fill=col)
        cv.rr((cx - r * .6, cy + r * .2, cx + r * .6, cy + r * .8), r * .3, fill=col)
    elif name == "eye":
        cv.ell(cx, cy, r * .65, outline=col, w=2.4)
        cv.ell(cx, cy, r * .25, fill=col)
    elif name == "target":
        cv.ell(cx, cy, r * .7, outline=col, w=2.4)
        cv.ell(cx, cy, r * .35, outline=col, w=2.4)
        cv.ell(cx, cy, r * .1, fill=col)


def header(cv, label, brand="INSTA AUTOMATION AI"):
    cv.text(34, 34, brand, "lat", 12, MUTE)
    cv.text(W - 34, 34, label, "lat", 12, CYAN, "ra")
    cv.line([(34, 58), (W - 34, 58)], LINE + (160,), 1)


# ------------------------------------------------------------------ phone + profile mock-up
def phone(cv, x, y, w, h, a=1.0, dark=False):
    cv.rr((x - 7, y - 7, x + w + 7, y + h + 7), 44, fill=(14, 18, 48, int(255 * a)), outline=CYAN + (int(200 * a),), w=2.5)
    cv.rr((x, y, x + w, y + h), 38, fill=((18, 22, 52) if dark else (247, 248, 253)) + (int(255 * a),))
    cv.rr((x + w / 2 - 34, y + 9, x + w / 2 + 34, y + 25), 8, fill=(14, 18, 48))
    return (x, y + 34, x + w, y + h)


def tile(cv, box, style, k, rng):
    x0, y0, x1, y1 = box
    if style == "random":
        cols = [(255, 90, 70), (255, 200, 40), (60, 200, 120), (60, 130, 255), (230, 70, 200), (255, 140, 30), (120, 80, 220)]
        cv.rr(box, 2, fill=cols[k % len(cols)])
        sh = (k * 7 + rng.randint(0, 5)) % 4
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        r = (x1 - x0) * .26
        if sh == 0:
            cv.ell(cx, cy, r, fill=(255, 255, 255, 190))
        elif sh == 1:
            cv.poly([(cx, cy - r), (cx + r, cy + r), (cx - r, cy + r)], (20, 20, 20, 200))
        elif sh == 2:
            cv.rr((cx - r, cy - r, cx + r, cy + r), 3, fill=(255, 255, 255, 170))
        else:
            cv.text(cx, cy, ["Hi", "SALE", "New!", "OFFER", "Hello"][k % 5], "lat", 11, (255, 255, 255), "mm")
    else:
        labels = [("OFFER", "star"), ("MENU", "menu"), ("REVIEWS", "heart"), ("TOUR", "play"), ("BOOK", "cal"), ("FIND US", "pin")]
        lab, ic = labels[k % len(labels)]
        c = [(16, 22, 58), (30, 20, 84), (14, 56, 78)][k % 3]
        cv.rr(box, 2, fill=c)
        icon(cv, ic, (x0 + x1) / 2, (y0 + y1) / 2 - 6, (x1 - x0) * .17, CYAN if k % 2 == 0 else AMBER)
        cv.text((x0 + x1) / 2, y1 - 9, lab, "lat", 8.5, (230, 235, 255), "mb")


def profile(cv, box, t, style="clean", reveal=(0, 0.3, 0.6, 0.9, 1.2), name="Your Business", full=False):
    """phone screen content. reveal = times when avatar, bio, highlights, grid-row-1, grid-row-2+ appear"""
    x0, y0, x1, y1 = box
    w = x1 - x0
    rng = random.Random(4)
    cv.text(x0 + 16, y0 + 8, "yourbusiness", "lat", 11, INK)
    ar = pr(t, reveal[0], reveal[0] + .5) if not full else 1
    r = 24
    cx, cy = x0 + 16 + r, y0 + 58
    cv.ell(cx, cy, r + 3, outline=CYAN if style == "clean" else (190, 190, 200), w=2.5)
    cv.ell(cx, cy, r - 1, fill=(24, 30, 80) if style == "clean" else (180, 180, 190))
    if style == "clean":
        cv.text(cx, cy, "B", "lat", 20, CYAN, "mm")
        icon(cv, "bolt", cx + 14, cy + 15, 6, AMBER)
    for i, (n, lab) in enumerate((("12", "posts"), ("3.4K", "followers"), ("86", "following"))):
        sx = x0 + 100 + i * (w - 112) / 3
        cv.text(sx + 24, y0 + 44, n if style == "clean" else ["0", "0", "0"][i], "lat", 13, INK, "ma")
        cv.text(sx + 24, y0 + 62, lab, "latm", 8.5, (90, 96, 120), "ma")
    br = pr(t, reveal[1], reveal[1] + .5) if not full else 1
    if style == "clean":
        cv.text(x0 + 16, y0 + 96, "Your Business | City", "lat", 11, INK)
        cv.text(x0 + 16, y0 + 112, "Services · Offers · Location", "latm", 9, (90, 96, 120))
        if br > 0:
            for i, (lab, col) in enumerate((("Message", (225, 230, 245)), ("Book now", CYAN), ("Call", (225, 230, 245)))):
                bx = x0 + 16 + i * ((w - 40) / 3 + 4)
                cv.rr((bx, y0 + 130, bx + (w - 40) / 3, y0 + 152), 6, fill=col)
                cv.text(bx + (w - 40) / 6, y0 + 141, lab, "lat", 8.5, INK, "mm")
    else:
        cv.text(x0 + 16, y0 + 96, "Account Name", "lat", 11, (140, 140, 150))
        for k in range(3):
            cv.rr((x0 + 16, y0 + 114 + k * 12, x0 + 16 + (w - 60) * (1 - .2 * k), y0 + 120 + k * 12), 3, fill=(215, 216, 225))
    hr = pr(t, reveal[2], reveal[2] + .6) if not full else 1
    if style == "clean" and hr > 0:
        for i, (lab, ic) in enumerate((("Services", "gear" if False else "target"), ("Menu", "menu"), ("Offers", "star"), ("Reviews", "heart"), ("Visit", "pin"))):
            cx = x0 + 28 + i * (w - 34) / 5 + 8
            a = ease(hr * 5 - i)
            if a <= 0:
                continue
            cv.ell(cx, y0 + 188, 19, outline=CYAN + (int(255 * a),), w=2)
            cv.ell(cx, y0 + 188, 15, fill=(228, 236, 250, int(255 * a)))
            icon(cv, ic, cx, y0 + 188, 8, (20, 40, 110))
            cv.text(cx, y0 + 214, lab, "latm", 7.5, (70, 76, 100, int(255 * a)), "ma")
    elif style != "clean":
        for i in range(5):
            cx = x0 + 28 + i * (w - 34) / 5 + 8
            cv.ell(cx, y0 + 188, 19, fill=(226, 226, 232))
    gy = y0 + 236
    gr = [pr(t, reveal[3], reveal[3] + .6), pr(t, reveal[4], reveal[4] + .6)]
    cw = (w - 4) / 3
    th = cw * 1.12
    k = 0
    row = 0
    while gy + row * (th + 2) < y1 - 6:
        a = gr[0] if row == 0 else gr[1]
        if full:
            a = 1
        for c in range(3):
            if a > 0 and ease(a * 3 - c * .4) > 0:
                bx = x0 + 2 + c * (cw + 1)
                by = gy + row * (th + 2)
                if by > y1 - 30:
                    k += 1
                    continue
                tile(cv, (bx, by, bx + cw, min(by + th, y1 - 4)), style, k, rng)
            k += 1
        row += 1


# ------------------------------------------------------------------ generic components
def toggle(cv, cx, cy, p, w=190, h=84):
    """Manual -> Automatic switch"""
    col = mixc(LINE, CYAN, p)
    cv.rr((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), h / 2, fill=col)
    kx = lerp(cx - w / 2 + h / 2, cx + w / 2 - h / 2, p)
    cv.ell(kx, cy, h / 2 - 7, fill=WHITE)
    cv.text(cx, cy + h / 2 + 34, "AUTOMATIC" if p > .5 else "MANUAL", "lat", 20, CYAN if p > .5 else MUTE, "mm")


def ring(cv, cx, cy, r, p, label="", col=CYAN, w=12):
    cv.ell(cx, cy, r, outline=LINE, w=w)
    if p > 0:
        cv.arc(cx, cy, r, -90, -90 + 360 * p, col, w)
    if label:
        cv.text(cx, cy, label, "lat", r * .5, WHITE, "mm")


def bar_chart(cv, box, vals, t, col=CYAN, a0=0.0):
    x0, y0, x1, y1 = box
    n = len(vals)
    gw = (x1 - x0) / n
    for i, v in enumerate(vals):
        p = pr(t, a0 + i * .12, a0 + i * .12 + .7)
        hh = (y1 - y0) * v * p
        cv.rr((x0 + i * gw + gw * .15, y1 - hh, x0 + (i + 1) * gw - gw * .15, y1), 6, fill=mixc(VIOLET, col, i / max(1, n - 1)))
    cv.line([(x0, y1 + 2), (x1, y1 + 2)], LINE, 2)


def card_row(cv, cx, y, items, t, a0=0.0, w=190, h=170):
    """feature cards [(icon, title, sub)] side by side or wrapped"""
    n = len(items)
    gap = 14
    tw_ = n * w + (n - 1) * gap
    x = cx - tw_ / 2
    for i, (ic, ti, su) in enumerate(items):
        a = pr(t, a0 + i * .25, a0 + i * .25 + .5)
        if a <= 0:
            continue
        yy = y + (1 - a) * 30
        cv.glass((x + i * (w + gap), yy, x + i * (w + gap) + w, yy + h), 18, fill=CARD2 + (int(255 * a),), outline=LINE + (int(255 * a),), glow=None)
        cv.ell(x + i * (w + gap) + w / 2, yy + 46, 26, fill=(CYAN if i % 2 == 0 else PINK) + (int(255 * a),))
        icon(cv, ic, x + i * (w + gap) + w / 2, yy + 46, 13, INK)
        cv.text(x + i * (w + gap) + w / 2, yy + 94, ti, "lat", 17, WHITE + (int(255 * a),), "ma")
        if su:
            cv.text(x + i * (w + gap) + w / 2, yy + 120, su, "latm", 12, MUTE + (int(255 * a),), "ma")


def check_list(cv, x, y, items, t, a0=0.0, w=520, gap=84):
    for i, (ic, label) in enumerate(items):
        a = pr(t, a0 + i * .45, a0 + i * .45 + .5)
        if a <= 0:
            continue
        yy = y + i * gap + (1 - a) * 24
        cv.glass((x, yy, x + w, yy + 66), 33, fill=CARD2 + (int(255 * a),), outline=CYAN + (int(110 * a),), glow=None)
        cv.ell(x + 36, yy + 33, 22, fill=CYAN + (int(255 * a),))
        icon(cv, ic, x + 36, yy + 33, 11, INK)
        cv.text(x + 78, yy + 33, label, "lat", 22, WHITE + (int(255 * a),), "lm")
        ck = pr(t, a0 + i * .45 + .5, a0 + i * .45 + .8)
        if ck > 0:
            cv.ell(x + w - 36, yy + 33, 16, fill=GREEN + (int(255 * ck),))
            icon(cv, "check", x + w - 36, yy + 33, 9, INK)


def loop_diagram(cv, cx, cy, t, labels=("PLAN", "CREATE", "ANALYSE")):
    r = 170
    pts = []
    for i in range(3):
        a = math.radians(-90 + i * 120)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    cv.ell(cx, cy, r, outline=LINE, w=3)
    sweep = (t * 70) % 360
    cv.arc(cx, cy, r, sweep - 90, sweep - 30, CYAN, 8)
    ics = ("cal", "play", "bars")
    for i, (px, py) in enumerate(pts):
        a = pr(t, .3 + i * .35, .8 + i * .35)
        cv.ell(px, py, 52 * a + 1, fill=CARD2, outline=(CYAN, VIOLET, PINK)[i], w=3)
        if a > .5:
            icon(cv, ics[i], px, py - 4, 20, WHITE)
            cv.text(px, py + (84 if i else -82), labels[i], "lat", 15, WHITE, "mm")
    cv.text(cx, cy, "SYSTEM", "lat", 17, CYAN, "mm")


def brand_card(cv, cx, cy, t, name="INSTA AUTOMATION AI", line="Message us to know more", handle=""):
    a = pr(t, .1, .7)
    cv.glass((cx - 300, cy - 190, cx + 300, cy + 190), 30, fill=CARD2 + (int(255 * a),), outline=CYAN + (int(180 * a),), glow=CYAN)
    cv.ell(cx, cy - 92, 46 * a + 1, fill=CYAN)
    icon(cv, "bolt", cx, cy - 92, 24 * a, INK)
    cv.text(cx, cy - 20, name, "lat", 30, WHITE + (int(255 * a),), "mm")
    cv.text(cx, cy + 26, line, "latm", 18, MUTE + (int(255 * a),), "mm")
    if handle:
        cv.text(cx, cy + 62, "@" + handle, "lat", 20, CYAN + (int(255 * a),), "mm")
    if pr(t, .9, 1.4) > 0:
        chip(cv, cx, cy + 128, "FOLLOW  ·  SAVE  ·  SHARE", 17, VIOLET, WHITE, pr(t, .9, 1.4))
