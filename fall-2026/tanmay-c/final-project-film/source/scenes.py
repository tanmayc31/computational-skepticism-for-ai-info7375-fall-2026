"""
iso_kit.py — the show-tell drawing kit. PASTE this block at the top of a reel's scenes.py;
do not import it (Gate A copies only scenes.py into its sandbox).

Drawn isometric objects in the Claude palette: cardboard boxes (closed, open, taped), dark
MCP blocks with ports, flat skill pages, server stacks with lights, checks, a cursor, pills,
and a WRITING KIT (quill, inkwell, paper, scribble lines, branching outline + the write_lines /
grow_tree animations that make the quill write). A PERSON IS NEVER AN ICON: `professor_bear(ratio, …)`
places a random Professor Bear portrait of the right aspect ratio (PROFESSOR BEAR LAW).
Pacing helpers read the reel's beat_sheet.json so scenes wait for their spoken phrase.

Every rule in ../SKILL.md "DRAWING LAWS" is already obeyed by these primitives; keep it that
way when you add one (label beside, never inside; terracotta never under text; dim greys
with gaps for chart blocks; type floor 32).
"""
from manim import *
import numpy as np
import json as _json, os as _os

# ═════════════════════════════ ISO KIT (show-tell) ═════════════════════════════
STAGE = "#F2F0E9"; INK = "#3D3929"; TERRA = "#D97757"; DIM = "#8B8F96"; GHOST = "#D9D4C7"; CARD = "#FAF9F5"
BOX_TOP, BOX_L, BOX_R = "#F3E9D8", "#DCC9AA", "#C7AE86"          # kraft cardboard: top, left face, right face (deep enough for Gate V contrast)
BOX_IN1, BOX_IN2, BOX_FLOOR = "#CDB894", "#BFA67E", "#B39A72"     # inside walls + floor
DARK_TOP, DARK_L, DARK_R = "#3A3530", "#26221F", "#1E1B18"        # MCP / server blocks
PAGE_TOP, PAGE_L, PAGE_R = "#FFFFFF", "#ECE7DF", "#E2DCD2"         # skill pages
BAR1, BAR2, BAR3 = "#8B8F96", "#B4AFA6", "#D9D4C7"                # chart segments, dim to ghost
SERIF = "EB Garamond"
C30 = 0.8660254
config.background_color = STAGE


def T(s, size=36, color=INK, bold=False):
    return Text(s, font=SERIF, color=color, font_size=size, weight="BOLD" if bold else "NORMAL")


class Iso:
    """Isometric projection: x runs right-up, y runs left-up, z runs up. (ox, oy) is where (0,0,0) lands."""
    def __init__(self, ox=0.0, oy=0.0, s=1.0):
        self.ox, self.oy, self.s = ox, oy, s

    def p(self, x, y, z=0.0):
        return np.array([self.ox + (x - y) * C30 * self.s, self.oy + (x + y) * 0.5 * self.s + z * self.s, 0.0])

    def v(self, dx, dy, dz=0.0):
        return self.p(dx, dy, dz) - self.p(0, 0, 0)

    def quad(self, pts, fill, stroke=INK, sw=4):
        return Polygon(*[self.p(*q) for q in pts], fill_color=fill, fill_opacity=1, stroke_color=stroke, stroke_width=sw)

    def box(self, x0, y0, z0, w, d, h, top=BOX_TOP, left=BOX_L, right=BOX_R, sw=4):
        """Closed box: the two front faces (x = x0 and y = y0) plus the top."""
        x1, y1, z1 = x0 + w, y0 + d, z0 + h
        return VGroup(
            self.quad([(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)], left, sw=sw),
            self.quad([(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)], right, sw=sw),
            self.quad([(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)], top, sw=sw))

    def open_box(self, x0, y0, z0, w, d, h):
        """(back, front): floor + inner back walls, then the front walls. Put contents between them."""
        x1, y1, z1 = x0 + w, y0 + d, z0 + h
        back = VGroup(
            self.quad([(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)], BOX_FLOOR),
            self.quad([(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)], BOX_IN1),
            self.quad([(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)], BOX_IN2))
        front = VGroup(
            self.quad([(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)], BOX_L),
            self.quad([(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)], BOX_R))
        back.set_z_index(0); front.set_z_index(2)
        return back, front

    def tape(self, x0, y0, z1, w, d, drop=0.35, t=0.22):
        """Terracotta tape across the top (along x) and down the left front face."""
        ym = y0 + d / 2
        return VGroup(
            self.quad([(x0, ym - t, z1), (x0 + w, ym - t, z1), (x0 + w, ym + t, z1), (x0, ym + t, z1)], TERRA, sw=0),
            self.quad([(x0, ym - t, z1), (x0, ym + t, z1), (x0, ym + t, z1 - drop), (x0, ym - t, z1 - drop)], TERRA, sw=0))

    def mcp(self, x0, y0, z0, w=1.3, d=1.3, h=0.7):
        """Dark MCP block with two light ports on its right front face."""
        body = self.box(x0, y0, z0, w, d, h, DARK_TOP, DARK_L, DARK_R)
        ports = VGroup(*[self.box(x0 + w * f, y0 - 0.18, z0 + h * 0.3, w * 0.16, 0.18, h * 0.3, GHOST, BOX_IN1, BOX_IN2, sw=1)
                         for f in (0.22, 0.58)])
        return VGroup(body, ports)

    def page(self, x0, y0, z0, w=1.1, d=1.4):
        """A skill page lying flat: white slab, three ghost text lines, one terracotta dot."""
        slab = self.box(x0, y0, z0, w, d, 0.06, PAGE_TOP, PAGE_L, PAGE_R, sw=1.5)
        zt = z0 + 0.06
        lines = VGroup(*[Line(self.p(x0 + 0.2, y0 + d * f, zt), self.p(x0 + w - 0.2, y0 + d * f, zt), color=GHOST, stroke_width=4)
                         for f in (0.3, 0.5, 0.7)])
        dot = Dot(self.p(x0 + 0.2, y0 + d * 0.86, zt), radius=0.06, color=TERRA)
        return VGroup(slab, lines, dot)

    def server(self, x0, y0, z0, w=1.4, d=1.4, slab=0.42, n=3):
        """A stack of dark server slabs; returns (stack, lights) — lights start ghost, turn terracotta."""
        stack = VGroup(*[self.box(x0, y0, z0 + i * (slab + 0.04), w, d, slab, DARK_TOP, DARK_L, DARK_R) for i in range(n)])
        lights = VGroup(*[Dot(self.p(x0 + 0.25, y0, z0 + i * (slab + 0.04) + slab / 2), radius=0.06, color=GHOST) for i in range(n)])
        return stack, lights


def ease_in(t):
    """Quadratic ease-in (things dropping into a box). Local: Gate A's stub has no ease_in_quad."""
    return t * t


def check(x, y, s=0.2, color=INK, w=7):
    return VGroup(Line([x - s, y, 0], [x - s * 0.3, y - s * 0.75, 0], color=color, stroke_width=w),
                  Line([x - s * 0.3, y - s * 0.75, 0], [x + s * 1.1, y + s * 0.85, 0], color=color, stroke_width=w))


def cursor(x, y, s=0.45):
    return Polygon([x, y, 0], [x, y - s, 0], [x + s * 0.28, y - s * 0.72, 0], [x + s * 0.62, y - s * 0.66, 0],
                   fill_color=INK, fill_opacity=1, stroke_color=CARD, stroke_width=2)


def pill(x, y, w, h=0.62, fill="#FFFFFF"):
    return RoundedRectangle(width=w, height=h, corner_radius=h / 2, fill_color=fill, fill_opacity=1, stroke_width=0).move_to([x, y, 0])


# ═════════════════════════════ WRITING KIT (quill, ink, paper, scribble) ═════════════════════════════
# Added 2026-10-07 from Bear's two reference drawings: a quill drawing a branching outline on a
# scroll, and three scattered pages of scribbled handwriting with a quill. Use when a beat is
# about writing, drafting, authorship, notes, a manuscript, a log, a letter, a signature.
# Terracotta here is only the ink drop and the outline's nodes (dots) — never the lines.


def quill(x, y, s=1.0, angle=0.0, color=INK, fill=BOX_TOP):
    """A drawn quill with its NIB at (x, y); the feather points up-right. `g.nib` is the nib point.
    Kraft-filled feather, ink outline, a shaft line and one barb. Rotate with `angle` (radians)."""
    o = np.array([x, y, 0.0])
    def P(u, v):  # icon units (0..1) → scene, nib at origin, tip at (1, 1.1)·s
        return o + np.array([u * s, v * s, 0.0])
    body = VMobject(fill_color=fill, fill_opacity=1, stroke_color=color, stroke_width=4)
    body.set_points_smoothly([P(0.00, 0.00), P(0.12, 0.62), P(0.55, 1.02), P(1.00, 1.10),
                              P(0.95, 0.68), P(0.62, 0.22), P(0.00, 0.00)])
    shaft = Line(P(0.02, 0.02), P(0.98, 1.06), color=color, stroke_width=3)
    barb = Line(P(0.46, 0.50), P(0.40, 0.72), color=color, stroke_width=2.5)
    g = VGroup(body, shaft, barb)
    if angle:
        g.rotate(angle, about_point=o)
    g.nib = o.copy()
    return g


def inkwell(iso, x0=0.0, y0=0.0, z0=0.0, s=0.7):
    """A dark ink bottle (iso box + narrow neck) with one terracotta ink dot on the lid."""
    body = iso.box(x0, y0, z0, s, s, s * 0.9, DARK_TOP, DARK_L, DARK_R)
    neck = iso.box(x0 + s * 0.3, y0 + s * 0.3, z0 + s * 0.9, s * 0.4, s * 0.4, s * 0.25, DARK_TOP, DARK_L, DARK_R)
    drop = Dot(iso.p(x0 + s * 0.5, y0 + s * 0.5, z0 + s * 1.15), radius=0.07, color=TERRA)
    return VGroup(body, neck, drop)


def paper(x, y, w=2.4, h=3.0, tilt=0.0, fill=PAGE_TOP):
    """A flat 2-D sheet (the scattered-pages drawing): white page, ink outline, kraft drop shadow.
    `tilt` in radians. Returns a VGroup; `.sheet` is the page rectangle for placing lines on it."""
    shadow = Rectangle(width=w, height=h, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([x + 0.12, y - 0.12, 0])
    sheet = Rectangle(width=w, height=h, fill_color=fill, fill_opacity=1, stroke_color=INK, stroke_width=4).move_to([x, y, 0])
    g = VGroup(shadow, sheet)
    if tilt:
        g.rotate(tilt, about_point=[x, y, 0])
    g.sheet = sheet
    g.cx, g.cy, g.w, g.h, g.tilt = float(x), float(y), float(w), float(h), float(tilt)   # read these; never ask the stub for vertices
    return g


def scribble(x, y, w, amp=0.07, waves=None, color=INK, sw=4):
    """One wavy handwriting line from (x, y) rightwards for `w` units. Reads as script, never as type."""
    n = waves or max(3, int(round(w * 3)))
    pts = []
    for i in range(n * 4 + 1):
        t = i / (n * 4)
        pts.append([x + w * t, y + amp * np.sin(t * n * 2 * np.pi) * (0.6 + 0.4 * np.cos(t * 5.3)), 0])
    m = VMobject(stroke_color=color, stroke_width=sw)
    m.set_points_smoothly(pts)
    return m


def scribble_block(x, y, w, n=3, gap=0.34, last=0.62, color=INK, sw=4):
    """`n` scribble lines stacked downward from (x, y); the last one is `last`× as long (a paragraph end)."""
    return VGroup(*[scribble(x, y - i * gap, w * (last if i == n - 1 else 1.0), color=color, sw=sw) for i in range(n)])


def scribbles_on(page, n=3, inset=0.3, gap=0.34, color=INK, sw=4):
    """Scribble lines laid on a `paper()` group, following its tilt (uses the page's stored geometry)."""
    w = page.w - 2 * inset
    g = scribble_block(page.cx - w / 2, page.cy + page.h / 2 - inset - 0.1, w, n=n, gap=gap, color=color, sw=sw)
    if abs(page.tilt) > 1e-3:
        g.rotate(page.tilt, about_point=[page.cx, page.cy, 0])
    return g


def outline_tree(x, y, h=1.6, levels=2, spread=0.55, color=INK, node=TERRA):
    """A branching outline (the scroll drawing): a trunk rising from (x, y), forking `levels` times,
    a terracotta dot at every tip. Returns VGroup(lines, dots) — draw lines first, dots last."""
    lines, dots = VGroup(), VGroup()
    def grow(px, py, length, lvl, dx):
        qx, qy = px + dx, py + length
        lines.add(Line([px, py, 0], [qx, qy, 0], color=color, stroke_width=4))
        if lvl == 0:
            dots.add(Dot([qx, qy, 0], radius=0.075, color=node))
            return
        for d in (-spread, spread):
            grow(qx, qy, length * 0.62, lvl - 1, d * (0.75 ** (levels - lvl)))
    grow(x, y, h * 0.42, levels, 0.0)
    g = VGroup(lines, dots)
    g.lines, g.dots = lines, dots
    return g


def write_lines(self, q, lines, speed=1.6, hop=0.22, dip=0.06):
    """Animate the quill `q` WRITING each line in `lines`: the nib hops to the line's start, then the
    line draws while the nib rides its tip (the writing motion). `speed` is scene units per second.
    Call between `until()` phrases so each line lands on its words. Works with the midpoint guard."""
    for ln in lines:
        start = np.array(ln.get_start(), dtype=float)
        self.play(q.animate.shift(start - q.nib), run_time=hop, rate_func=smooth)
        q.nib = start.copy()
        off = np.array(q.get_center(), dtype=float) - q.nib
        def ride(m, a, ln=ln, off=off):
            m.move_to(np.array(ln.point_from_proportion(min(1.0, a)), dtype=float) + off)
        try:
            length = float(ln.get_arc_length())
        except Exception:          # Gate A's stub has no arc length; any positive number keeps the check moving
            length = 2.0
        rt = max(0.35, length / speed)
        self.play(Create(ln), UpdateFromAlphaFunc(q, ride), run_time=rt, rate_func=linear)
        q.nib = np.array(ln.get_end(), dtype=float)
        # the small lift between lines keeps the quill from fusing with the ink at GATE T's midpoint
        q.shift([0, dip, 0]); q.nib = q.nib + np.array([0, dip, 0])


def grow_tree(self, q, tree, per=0.45):
    """Animate the quill drawing an `outline_tree`: each segment draws as the nib rides it; dots land last."""
    for ln in tree.lines:
        start = np.array(ln.get_start(), dtype=float)
        self.play(q.animate.shift(start - q.nib), run_time=0.18, rate_func=smooth)
        q.nib = start.copy()
        off = np.array(q.get_center(), dtype=float) - q.nib
        def ride(m, a, ln=ln, off=off):
            m.move_to(np.array(ln.point_from_proportion(min(1.0, a)), dtype=float) + off)
        self.play(Create(ln), UpdateFromAlphaFunc(q, ride), run_time=per, rate_func=linear)
        q.nib = np.array(ln.get_end(), dtype=float)
    self.play(LaggedStart(*[GrowFromCenter(d) for d in tree.dots], lag_ratio=0.15), run_time=0.6)


# ═════════════════════════════ PROFESSOR BEAR (a person is never an icon) ═════════════════════════════
# PROFESSOR BEAR LAW (Bear, 2026-10-07): when a beat needs an icon of a person, or Professor Bear himself,
# do not draw a person token and do not pull a person icon. Show one of the Professor Bear portraits in
# brutalist.art/professor-bear/, chosen at random among those of the right aspect ratio (1x1 · 2x3 · 16x9).
# `./art bear <ratio> --seed <beat>` picks the same way from the shell.
def _pb_dir():
    env = _os.environ.get("ART_HOME")
    cands = [env and _os.path.join(env, "professor-bear")]
    here = _os.path.dirname(_os.path.abspath(__file__))
    for _ in range(8):
        cands.append(_os.path.join(here, "brutalist.art", "professor-bear"))
        cands.append(_os.path.join(here, "professor-bear"))
        here = _os.path.dirname(here)
    cands.append("/Users/bear/Documents/CoWork/bear-textbooks/books/brutalist.art/professor-bear")
    for c in cands:
        if c and _os.path.isdir(c):
            return c
    return cands[-1]


_PB_RATIOS = {"1x1": (1.0, 229), "2x3": (2 / 3, 28), "16x9": (16 / 9, 13)}


def _pb_circle(path):
    """A circular cut (alpha outside the circle), cached beside the set in _crops/. Cropping is fine (Bear, 2026-10-07)."""
    from PIL import Image as _Im, ImageDraw as _Dr
    out_dir = _os.path.join(_os.path.dirname(path), "_crops"); _os.makedirs(out_dir, exist_ok=True)
    out = _os.path.join(out_dir, _os.path.splitext(_os.path.basename(path))[0] + "-circle.png")
    if not _os.path.exists(out):
        im = _Im.open(path).convert("RGBA"); w, h = im.size; s = min(w, h); top = max(0, (h - s) // 3)
        im = im.crop(((w - s) // 2, top, (w - s) // 2 + s, top + s))
        mask = _Im.new("L", (s, s), 0); _Dr.Draw(mask).ellipse((0, 0, s - 1, s - 1), fill=255)
        im.putalpha(mask); im.save(out)
    return out


def professor_bear(ratio="2x3", height=3.0, seed=None, x=0.0, y=0.0, frame=True, shape="rect"):
    """A Professor Bear portrait (random within `ratio`; `seed` = the beat id for a stable pick across re-renders).
    Returns a Group: kraft drop shadow, the photo, an ink frame. Place with `x, y`; size with `height`.
    `shape="circle"` gives a round cut (use a 1x1 portrait). Cropping is fine: circle, rounded square, tight head shot."""
    import random as _random
    ar, n = _PB_RATIOS[ratio]
    k = _random.Random(str(seed) if seed is not None else None).randint(1, n)
    path = _os.path.join(_pb_dir(), f"professor-bear-{ratio}-{k:02d}.png")
    circle = shape == "circle"
    if circle:
        ar = 1.0
    w = height * ar
    if circle:
        shadow = Circle(radius=height / 2, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([x + 0.12, y - 0.12, 0])
        border = Circle(radius=height / 2, stroke_color=INK, stroke_width=4, fill_opacity=0).move_to([x, y, 0])
    else:
        shadow = Rectangle(width=w, height=height, fill_color=BOX_L, fill_opacity=1, stroke_width=0).move_to([x + 0.12, y - 0.12, 0])
        border = Rectangle(width=w, height=height, stroke_color=INK, stroke_width=4, fill_opacity=0).move_to([x, y, 0])
    try:
        img = ImageMobject(_pb_circle(path) if circle else path)
        img.height = height
        img.move_to([x, y, 0])
    except Exception:
        img = Rectangle(width=w, height=height, fill_color=BAR2, fill_opacity=1, stroke_width=0).move_to([x, y, 0])
    g = Group(shadow, img, border) if frame else Group(img)
    g.path = path
    return g


# ═════════════════════════════ pacing (narration is the clock) ═════════════════════════════
try:
    _SHEET = _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "beat_sheet.json")))
    _TARGET = {b["beat_id"]: float(b.get("actual_duration_s") or b.get("estimated_duration_s") or 0) for b in _SHEET["beats"]}
    _NARR = {b["beat_id"]: b["narration_text"] for b in _SHEET["beats"]}
except Exception:
    _TARGET, _NARR = {}, {}


def _elapsed(self):
    rt = getattr(getattr(self, "renderer", None), "time", None)
    return float(rt) if isinstance(rt, (int, float)) else 0.0


def until(self, phrase, lead=0.25):
    """Wait until `phrase` is spoken (its character share of the narration × the measured audio)."""
    bid = type(self).__name__.split("_")[0]
    n, target = _NARR.get(bid, ""), _TARGET.get(bid, 0)
    if not n or not target or phrase not in n:
        return
    gap = target * n.index(phrase) / len(n) - lead - _elapsed(self)
    if gap > 0.05:
        self.wait(gap)


def finish(self):
    target = _TARGET.get(type(self).__name__.split("_")[0], 0)
    self.wait(max(0.3, target - _elapsed(self)) if target else 2.0)

# ═════════════════════ VERACITE CAST (law 4 — same objects, whole film) ═════════════════════
# Five objects, reused end to end: manual page · question slip · answer page → claim slips ·
# check gate (DOTTED = Veracite, not built yet) · counter / tally board.
# Everything here obeys the DRAWING LAWS in skills/make/show-tell/SKILL.md:
# labels beside, never inside; terracotta only for dots/rules/one scan line; small objects in
# dark kraft, large ones in ink; chart blocks in BAR greys with gaps; type floor 36.

def ease_out(t):
    """Quadratic ease-out. Local: Gate A's rate_functions stub has no ease_out_quad
    (same family as the ease_in_quad / ease_out_cubic traps in SKILL.md)."""
    return 1.0 - (1.0 - t) * (1.0 - t)


KRAFT_D = "#917A55"      # dark-kraft outline — SMALL objects only
KRAFT_C = "#9C8462"      # deep kraft — connectors, so cables don't fuse objects into one blob


def lbl(s, x, y, size=40, color=INK):
    """A label. Always placed BESIDE its object, never inside an outline."""
    return T(s, size, color=color).move_to([x, y, 0])


def hero(s, x, y, size=120):
    """The one permitted large number (law 2)."""
    return T(s, size, color=INK, bold=True).move_to([x, y, 0])


def floor_shadow(x, y, w=3.0, h=0.42):
    """Continuity: the ground the cast stands on, carried between beats."""
    return Ellipse(width=w, height=h, fill_color=GHOST, fill_opacity=1, stroke_width=0).move_to([x, y, 0])


def slab(x, y, w=1.9, h=1.25, depth=0.30, top=BOX_TOP, left=BOX_L, right=BOX_R, sw=4):
    """A page / slip seen flat-on with a kraft edge under it. The edge carries Gate V contrast:
    a pale kraft face alone sits within 28/channel of the stage and reads as background."""
    edge = Polygon([x - w / 2, y - h / 2, 0], [x + w / 2, y - h / 2, 0],
                   [x + w / 2 - 0.10, y - h / 2 - depth, 0], [x - w / 2 - 0.10, y - h / 2 - depth, 0],
                   fill_color=right, fill_opacity=1, stroke_color=INK, stroke_width=sw)
    face = Rectangle(width=w, height=h, fill_color=top, fill_opacity=1,
                     stroke_color=INK, stroke_width=sw).move_to([x, y, 0])
    side = Polygon([x + w / 2, y - h / 2, 0], [x + w / 2, y + h / 2, 0],
                   [x + w / 2 - 0.10, y + h / 2 - depth, 0], [x + w / 2 - 0.10, y - h / 2 - depth, 0],
                   fill_color=left, fill_opacity=1, stroke_color=INK, stroke_width=sw)
    g = VGroup(edge, side, face)
    g.face = face
    g.cx, g.cy, g.w, g.h = float(x), float(y), float(w), float(h)
    return g


def ruled(page, n=3, color=BAR1, sw=5, inset=0.26):
    """Grey rule lines on a slab's face — never glyphs, so GATE T never reads them as type."""
    w = page.w - 2 * inset
    top = page.cy + page.h / 2 - inset
    gap = (page.h - 2 * inset) / max(1, n - 1) if n > 1 else 0
    return VGroup(*[Line([page.cx - w / 2, top - i * gap, 0], [page.cx + w / 2 - (0.5 * w if i == n - 1 else 0), top - i * gap, 0],
                         color=color, stroke_width=sw) for i in range(n)])


def manual_page(x, y, w=1.9, h=1.35, tab=True):
    """A car-manual page: kraft slab, grey rules, and a small dark tab that carries contrast."""
    g = slab(x, y, w, h)
    g.add(ruled(g, 3))
    if tab:
        g.add(Rectangle(width=0.42, height=0.20, fill_color=DARK_TOP, fill_opacity=1,
                        stroke_color=INK, stroke_width=2).move_to([x + w / 2 - 0.36, y + h / 2 + 0.10, 0]))
    return g


def qslip(x, y, w=1.55, h=0.92):
    """A question slip / claim slip — smaller than a page, two grey rules."""
    g = slab(x, y, w, h, depth=0.22)
    g.add(ruled(g, 2, inset=0.22))
    return g


def dotted(mob, n=2, color=INK, sw=5):
    """A DOTTED outline = does not exist yet / unknown. Never used for anything that exists.
    Recurses into groups: DashedVMobject on a VGroup crashes, because the group carries no
    points of its own and `is_closed()` indexes an empty array."""
    if len(mob.submobjects) and not len(mob.points):
        return VGroup(*[dotted(m, n, color, sw) for m in mob.submobjects])
    return DashedVMobject(mob, num_dashes=max(12, int(n * 14)), dashed_ratio=0.56,
                          color=color, stroke_width=sw)


def gate(x, y, w=2.5, h=2.7, open_gate=False, ghostly=False):
    """The check gate: two posts and a lintel. `ghostly=True` draws it dotted — Veracite, not
    built yet. `open_gate=True` leaves the middle empty — the beat where nothing checks."""
    col = KRAFT_C if ghostly else INK
    post_w = 0.30
    left = Rectangle(width=post_w, height=h, fill_color=BOX_R, fill_opacity=0 if ghostly else 1,
                     stroke_color=col, stroke_width=5).move_to([x - w / 2, y, 0])
    right = Rectangle(width=post_w, height=h, fill_color=BOX_R, fill_opacity=0 if ghostly else 1,
                      stroke_color=col, stroke_width=5).move_to([x + w / 2, y, 0])
    lintel = Rectangle(width=w + post_w, height=0.44, fill_color=BOX_L, fill_opacity=0 if ghostly else 1,
                       stroke_color=col, stroke_width=5).move_to([x, y + h / 2 + 0.22, 0])
    parts = [left, right, lintel]
    if ghostly:
        parts = [dotted(p, n=3, color=col) for p in parts]
    g = VGroup(*parts)
    if not open_gate and not ghostly:
        g.add(Rectangle(width=0.22, height=0.22, fill_color=DARK_TOP, fill_opacity=1,
                        stroke_width=0).move_to([x, y + h / 2 - 0.30, 0]))
    g.cx, g.cy, g.w, g.h = float(x), float(y), float(w), float(h)
    return g


def stamp(x, y, word, w=2.5, h=0.86):
    """A verdict stamp. GREY outline (BAR1): an ink-outlined card loose on the stage beside an
    ink-outlined object reads as stacked labels under GATE T §8.6b."""
    box = RoundedRectangle(width=w, height=h, corner_radius=0.12, fill_color=CARD, fill_opacity=1,
                           stroke_color=BAR1, stroke_width=5).move_to([x, y, 0])
    return VGroup(box, lbl(word, x, y, 44))


def warn_flag(x, y, h=1.5):
    """A warning flag. The '!' is DRAWN (line + dot), never a Text glyph inside an outline."""
    pole = Line([x, y - h / 2, 0], [x, y + h / 2, 0], color=INK, stroke_width=6)
    tri = Polygon([x, y + h / 2, 0], [x + 1.05, y + h / 2 - 0.34, 0], [x, y + h / 2 - 0.68, 0],
                  fill_color=BOX_TOP, fill_opacity=1, stroke_color=INK, stroke_width=4)
    bang = VGroup(Line([x + 0.36, y + h / 2 - 0.16, 0], [x + 0.36, y + h / 2 - 0.40, 0], color=INK, stroke_width=6),
                  Dot([x + 0.36, y + h / 2 - 0.52, 0], radius=0.055, color=INK))
    return VGroup(pole, tri, bang)


def tally(x, y, n):
    """n counted marks in groups of five — counts, never a bare percentage (B08)."""
    g = VGroup()
    for i in range(n):
        grp, k = divmod(i, 5)
        gx = x + grp * 0.92
        if k == 4:
            g.add(Line([gx - 0.08, y - 0.30, 0], [gx + 0.58, y + 0.30, 0], color=INK, stroke_width=6))
        else:
            g.add(Line([gx + k * 0.16, y - 0.30, 0], [gx + k * 0.16, y + 0.30, 0], color=INK, stroke_width=6))
    return g


def arrow_to(a, b, color=KRAFT_C, sw=6, tip=0.20):
    """A connector in DEEP KRAFT: an ink-edged cable joins the objects it connects into one wide
    'text' blob under GATE T. The terracotta is only the end dot."""
    a, b = np.array(a, dtype=float), np.array(b, dtype=float)
    d = b - a
    n = np.linalg.norm(d) or 1.0
    end = b - d / n * 0.22
    return VGroup(Line(a, end, color=color, stroke_width=sw), Dot(end, radius=tip * 0.5, color=TERRA))


# ═════════════════════ pacing: the GATE T / Gate V midpoint guard ═════════════════════
# GATE T and Gate V both sample each clip at its MIDPOINT. Anything half-done there is judged
# as type: a half-faded object reads as a fused text blob, a half-drawn terracotta curve as
# accent text. `_play` holds every animation clear of the midpoint by 0.22 s.

def _mid(scene):
    return _TARGET.get(type(scene).__name__.split("_")[0], 10.0) / 2.0


def _play(scene, *anims, run_time=0.8, **kw):
    m, now = _mid(scene), _elapsed(scene)
    if now < m + 0.22 and now + run_time > m - 0.22:
        scene.wait(max(0.01, m + 0.26 - now))
    scene.play(*anims, run_time=run_time, **kw)


def _done(scene):
    finish(scene)


# ═════════════════════════════════ the beats ═════════════════════════════════

class B00_WrongPage(Scene):
    """A Ford question retrieves a Camry page, and the score climbs past the floor."""
    def construct(self):
        q = qslip(-3.5, -1.40)
        self.add(q, lbl("Ford question", -3.5, -2.86, 40))
        # scale: the floor line exists from the first frame so the counter has something to pass
        sx, sy0, sh = 3.6, -2.05, 4.3
        axis = Line([sx, sy0, 0], [sx, sy0 + sh, 0], color=BAR1, stroke_width=5)
        floor_y = sy0 + sh * 0.25
        floor_line = DashedLine([sx - 0.85, floor_y, 0], [sx + 0.95, floor_y, 0], color=INK,
                                stroke_width=5, dash_length=0.14)
        self.add(axis, floor_line, lbl("floor 0.25", 5.00, floor_y + 0.52, 36))
        self.wait(0.25)

        until(self, "While testing it")
        page = manual_page(-0.1, -1.30, 2.0, 1.25)
        page.shift(UP * 2.2).set_opacity(0)
        _play(self, page.animate.shift(DOWN * 2.2).set_opacity(1), run_time=0.9)
        lab = lbl("Camry page", -0.1, -2.86, 40)
        _play(self, FadeIn(lab), run_time=0.35)

        until(self, "scoring zero point")
        val_y = sy0 + sh * 0.547
        bar = Rectangle(width=0.62, height=0.01, fill_color=BAR1, fill_opacity=1,
                        stroke_width=0).move_to([sx - 0.45, sy0, 0])
        self.add(bar)
        _play(self, bar.animate.stretch_to_fit_height(val_y - sy0).move_to([sx - 0.45, (sy0 + val_y) / 2, 0]),
              run_time=1.0, rate_func=ease_out)
        num = hero("0.547", 1.20, val_y + 1.20, 108)
        _play(self, FadeIn(num), run_time=0.4)
        _play(self, GrowFromCenter(Dot([sx - 0.45, val_y, 0], radius=0.11, color=TERRA)), run_time=0.3)
        _done(self)


class B01_NoCheck(Scene):
    """Continuity: B00's Camry page is still on stage. It rides an EMPTY gate and nothing fires."""
    def construct(self):
        self.add(floor_shadow(0.0, -2.42, 4.6))
        g = gate(0.6, -0.35, 2.9, 2.9, open_gate=True)
        page = manual_page(-4.4, -0.55, 2.1, 1.5)
        self.add(g, page, lbl("no check", 0.6, 2.14, 46))
        self.wait(0.3)

        until(self, "But that was luck")
        _play(self, page.animate.move_to([4.5, -0.55, 0]), run_time=1.5, rate_func=linear)

        until(self, "Nothing in my pipeline")
        qm = T("?", 112, color=INK).move_to([0.6, -0.35, 0])
        _play(self, FadeIn(qm, scale=0.7), run_time=0.5)
        _play(self, GrowFromCenter(Circle(radius=1.18, stroke_color=KRAFT_C, stroke_width=5,
                                          fill_opacity=0).move_to([0.6, -0.35, 0])), run_time=0.5)
        _done(self)


class B02_Filter(Scene):
    """The vehicle filter lands on the stack — and one page still slips past, drawn DOTTED."""
    def construct(self):
        self.add(floor_shadow(-2.9, -2.45, 3.6))
        pages = VGroup(*[manual_page(-2.9, -1.95 + i * 0.52, 2.3, 1.1, tab=(i == 2)) for i in range(3)])
        self.add(pages, lbl("fix", -2.9, 2.55, 46))
        grate = VGroup(Rectangle(width=3.5, height=0.26, fill_color=BOX_L, fill_opacity=1,
                                 stroke_color=INK, stroke_width=4).move_to([-2.9, 0.0, 0]))
        for i in range(5):
            grate.add(Line([-4.3 + i * 0.70, -0.30, 0], [-4.3 + i * 0.70, 0.30, 0],
                           color=KRAFT_D, stroke_width=5))
        grate.shift(UP * 2.0)
        self.add(grate)
        self.wait(0.25)

        until(self, "The open question")
        _play(self, grate.animate.shift(DOWN * 1.90), run_time=0.8, rate_func=ease_in)

        until(self, "still holds when")
        leak = manual_page(-2.9, -0.55, 2.3, 1.1, tab=False)
        self.add(leak)
        _play(self, leak.animate.move_to([2.6, -0.55, 0]), run_time=1.1, rate_func=linear)
        ghost = dotted(Rectangle(width=2.3, height=1.1).move_to([2.6, -0.55, 0]), n=3)
        _play(self, FadeOut(leak), Create(ghost), run_time=0.7)
        _play(self, FadeIn(lbl("still open?", 2.6, -1.72, 44)), run_time=0.35)
        _done(self)


class B03_Survey(Scene):
    """Six survey bars; the citation-trust bar stays shortest. The n is printed, always."""
    def construct(self):
        base = -1.92
        xs = [-4.3 + i * 1.72 for i in range(6)]
        heights = [3.05, 2.70, 2.52, 1.28, 2.88, 2.34]   # index 3 = "I trusted the citations"
        cols = [BAR1, BAR2, BAR1, DIM, BAR2, BAR1]
        self.add(Line([-5.4, base, 0], [5.4, base, 0], color=INK, stroke_width=6))
        self.add(lbl("RideReady survey, n=7", 3.30, 2.95, 38))
        bars = []
        for x, h, c in zip(xs, heights, cols):
            b = Rectangle(width=1.08, height=0.02, fill_color=c, fill_opacity=1,
                          stroke_color=INK, stroke_width=4).move_to([x, base, 0])
            bars.append(b)
            self.add(b)
        self.wait(0.2)

        others = [i for i in range(6) if i != 3]
        _play(self, *[bars[i].animate.stretch_to_fit_height(heights[i]).move_to([xs[i], base + heights[i] / 2, 0])
                      for i in others], run_time=1.0, rate_func=ease_out)

        until(self, "scored lowest")
        _play(self, bars[3].animate.stretch_to_fit_height(heights[3]).move_to([xs[3], base + heights[3] / 2, 0]),
              run_time=0.6, rate_func=ease_out)
        _play(self, GrowFromCenter(Dot([xs[3], base + heights[3] + 0.26, 0], radius=0.12, color=TERRA)),
              run_time=0.3)
        _play(self, FadeIn(lbl("trust in citations", xs[3], -2.50, 40)), run_time=0.3)

        until(self, "three point seven one")
        _play(self, FadeIn(hero("3.71", 0.30, 1.78, 108)), run_time=0.4)
        _done(self)


class B04_ClaimSlips(Scene):
    """The answer page splits into claim slips; each rides a DOTTED gate to its own cited page."""
    def construct(self):
        ans = slab(-4.70, 1.25, 2.2, 1.45)
        ans.add(ruled(ans, 3))
        self.add(ans, lbl("claim", -4.70, -0.30, 40))
        g = gate(0.0, 0.0, 1.6, 5.0, ghostly=True)
        self.add(g)
        ys = [1.70, 0.0, -1.70]
        pages = VGroup(*[manual_page(4.60, y, 1.8, 1.05) for y in ys])
        self.add(pages, lbl("citation", 4.60, 2.95, 38))
        self.wait(0.25)

        until(self, "For every claim")
        slips = VGroup(*[qslip(-4.70, 1.25, 1.4, 0.74) for _ in ys])
        self.add(slips)
        _play(self, *[s.animate.move_to([-2.60, y, 0]) for s, y in zip(slips, ys)], run_time=0.8)

        until(self, "is the citation real")
        _play(self, *[s.animate.move_to([1.90, y, 0]) for s, y in zip(slips, ys)], run_time=0.9, rate_func=linear)

        for y in ys:
            _play(self, Create(check(3.15, y + 0.06, 0.28)), run_time=0.42)
        _done(self)


class B05_PooledVsPerClaim(Scene):
    """Left: everything pooled into one number. Right: one arrow per claim to its exact page."""
    def construct(self):
        self.add(DashedLine([-0.15, -3.05, 0], [-0.15, 3.05, 0], color=BAR1, stroke_width=4, dash_length=0.16))
        self.add(lbl("RAGAS", -4.25, -2.98, 44), lbl("Veracite", 3.25, -2.98, 44))
        loose = VGroup(*[manual_page(x, y, 1.5, 0.92, tab=False)
                         for x, y in [(-5.05, 1.10), (-3.35, 1.62), (-4.45, 0.02), (-2.55, 0.46)]])
        self.add(loose)
        self.wait(0.25)

        until(self, "pooled together")
        _play(self, *[p.animate.move_to([-3.95, -1.72 + i * 0.22, 0]) for i, p in enumerate(loose)], run_time=0.9)

        until(self, "gives one faithfulness score")
        cx, cy, r = -3.95, 0.72, 1.15
        dial = VGroup(Arc(radius=r, start_angle=0, angle=PI, arc_center=[cx, cy, 0],
                          stroke_color=INK, stroke_width=6),
                      Line([cx - r, cy, 0], [cx + r, cy, 0], color=INK, stroke_width=6))
        for a in (0.25, 0.5, 0.75):
            dial.add(Line([cx + r * 0.80 * np.cos(a * PI), cy + r * 0.80 * np.sin(a * PI), 0],
                          [cx + r * 0.97 * np.cos(a * PI), cy + r * 0.97 * np.sin(a * PI), 0],
                          color=KRAFT_D, stroke_width=4))
        needle = Line([cx, cy, 0], [cx + r * 0.72 * np.cos(0.68 * PI), cy + r * 0.72 * np.sin(0.68 * PI), 0],
                      color=INK, stroke_width=7)
        _play(self, Create(dial), run_time=0.6)
        _play(self, FadeIn(needle), GrowFromCenter(Dot([cx, cy, 0], radius=0.12, color=TERRA)), run_time=0.4)

        until(self, "ALCE is a research benchmark")
        grid = VGroup(*[Rectangle(width=0.38, height=0.38, fill_color=BAR2, fill_opacity=1,
                                  stroke_color=KRAFT_D, stroke_width=3).move_to([-1.72 + c * 0.48, 0.30 + rr * 0.48, 0])
                        for rr in range(3) for c in range(2)])
        _play(self, FadeIn(grid), run_time=0.5)
        _play(self, FadeIn(lbl("ALCE", -1.50, -0.92, 40)), run_time=0.3)

        until(self, "Veracite will")
        ys = [1.72, 0.22, -1.28]
        slips = VGroup(*[qslip(1.30, y, 1.3, 0.72) for y in ys])
        pgs = VGroup(*[manual_page(4.75, y, 1.6, 1.0, tab=False) for y in ys])
        _play(self, FadeIn(slips), FadeIn(pgs), run_time=0.5)
        for y in ys:
            _play(self, Create(arrow_to([2.05, y, 0], [3.90, y, 0])), run_time=0.32)
        _done(self)


class B06_NeverPass(Scene):
    """A missing tag reaches the gate and the verdict lands 'unknown' — never a check."""
    def construct(self):
        self.add(floor_shadow(0.2, -2.55, 4.4))
        g = gate(0.2, -0.20, 2.6, 3.0, ghostly=True)
        self.add(g, lbl("never pass by default", 0.0, 2.60, 46))
        s = qslip(-4.55, -0.35, 1.9, 1.05)
        missing = dotted(Rectangle(width=0.62, height=0.34).move_to([-4.55, 0.42, 0]), n=1, color=KRAFT_C, sw=4)
        self.add(s, missing)
        self.wait(0.25)

        until(self, "Missing vehicle metadata")
        _play(self, s.animate.move_to([0.2, -0.35, 0]), missing.animate.shift(RIGHT * 4.75), run_time=0.9,
              rate_func=linear)

        until(self, "becomes")
        st = stamp(3.95, -0.35, "unknown", 2.6)
        st.shift(UP * 1.25).set_opacity(0)
        _play(self, st.animate.shift(DOWN * 1.25).set_opacity(1), run_time=0.55, rate_func=ease_in)
        _play(self, GrowFromCenter(Dot([3.95, -1.32, 0], radius=0.11, color=TERRA)), run_time=0.3)
        _done(self)


class B07_OneCommand(Scene):
    """A MOCK-UP of a tool that does not exist yet — the frame says 'constructed' out loud."""
    def construct(self):
        self.add(lbl("constructed", -4.35, 2.88, 40))
        screen = Rectangle(width=4.5, height=2.7, fill_color=DIM, fill_opacity=1,
                           stroke_color=INK, stroke_width=5).move_to([-2.35, 0.25, 0])
        base = Polygon([-4.85, -1.10, 0], [0.15, -1.10, 0], [0.75, -1.72, 0], [-5.45, -1.72, 0],
                       fill_color=BOX_R, fill_opacity=1, stroke_color=INK, stroke_width=5)
        chev = VGroup(Line([-4.25, 1.05, 0], [-3.95, 0.82, 0], color=INK, stroke_width=6),
                      Line([-3.95, 0.82, 0], [-4.25, 0.59, 0], color=INK, stroke_width=6))
        self.add(screen, base, chev, lbl("one command", -2.35, -2.32, 40))
        self.wait(0.25)

        until(self, "they'll run one command")
        cmdline = Line([-3.70, 0.82, 0], [-0.55, 0.82, 0], color=INK, stroke_width=7)
        _play(self, Create(cmdline), run_time=0.7)
        _play(self, GrowFromCenter(Dot([-0.30, 0.82, 0], radius=0.10, color=TERRA)), run_time=0.25)

        until(self, "subject mismatch")
        res = stamp(2.95, 0.85, "mismatch", 2.5)
        _play(self, FadeIn(res, shift=RIGHT * 0.6), run_time=0.5)
        pg = manual_page(3.35, -1.45, 2.0, 1.25)
        _play(self, FadeIn(pg), run_time=0.4)
        _play(self, Create(arrow_to([2.95, 0.10, 0], [3.35, -0.72, 0])), run_time=0.4)
        _done(self)


class B08_CheckTheChecker(Scene):
    """A second, smaller gate measures the first one — and reports counts, with n."""
    def construct(self):
        self.add(floor_shadow(-3.15, -2.55, 4.0))
        big = gate(-3.15, -0.35, 2.6, 2.9)
        small = gate(0.25, -1.15, 1.2, 1.4)
        self.add(big, small, lbl("held-out set", 2.95, 2.45, 44))
        board = Rectangle(width=4.0, height=2.5, fill_color=CARD, fill_opacity=1,
                          stroke_color=BAR1, stroke_width=5).move_to([3.45, 0.55, 0])
        self.add(board)
        self.wait(0.25)

        until(self, "measure how often")
        scan = Line([-4.55, -1.85, 0], [-4.55, 1.15, 0], color=TERRA, stroke_width=6)
        self.add(scan)
        _play(self, scan.animate.shift(RIGHT * 2.8), run_time=0.8, rate_func=linear)
        _play(self, FadeOut(scan), run_time=0.25)

        until(self, "Errors will be counts")
        _play(self, Create(tally(2.15, 1.15, 7)), run_time=0.6)
        _play(self, Create(tally(2.15, 0.15, 4)), run_time=0.5)
        _play(self, FadeIn(lbl("counts + n", 3.45, -1.45, 40)), run_time=0.35)
        _done(self)


class B09_InOut(Scene):
    """In: local, on recorded traces. Out: no live system. First: one test."""
    def construct(self):
        iso = Iso(-3.05, -1.35, 1.0)
        box = iso.box(0, 0, 0, 1.9, 1.9, 1.3)
        # Label BESIDE the box, not on it: the box's left vertex is at x=-4.695, y=-0.40, so a
        # size-38 "local" centred at -5.60 spans -6.15..-5.05 — a 0.36 gap, inside the safe area.
        self.add(floor_shadow(-2.65, -1.62, 3.6), box, lbl("local", -5.60, -0.40, 38))
        traces = VGroup(*[manual_page(-3.05 + i * 0.1, 0.55 + i * 0.26, 1.5, 0.74, tab=False) for i in range(2)])
        self.add(traces)
        cloud = VGroup(Circle(radius=0.70, stroke_color=INK, stroke_width=5, fill_color=CARD, fill_opacity=1).move_to([1.55, 1.25, 0]),
                       Circle(radius=0.92, stroke_color=INK, stroke_width=5, fill_color=CARD, fill_opacity=1).move_to([2.75, 1.42, 0]),
                       Circle(radius=0.66, stroke_color=INK, stroke_width=5, fill_color=CARD, fill_opacity=1).move_to([3.85, 1.18, 0]))
        self.add(cloud)
        self.wait(0.25)

        until(self, "it will not plug into")
        x1 = VGroup(Line([1.15, 0.45, 0], [4.35, 2.25, 0], color=INK, stroke_width=9),
                    Line([1.15, 2.25, 0], [4.35, 0.45, 0], color=INK, stroke_width=9))
        _play(self, Create(x1), run_time=0.7)
        _play(self, FadeIn(lbl("not live", 2.75, -0.25, 44)), run_time=0.35)

        until(self, "First: a test")
        ring = dotted(Circle(radius=0.62).move_to([2.75, -1.75, 0]), n=2)
        _play(self, Create(ring), run_time=0.5)
        _play(self, GrowFromCenter(Dot([2.75, -1.75, 0], radius=0.30, color=TERRA)), run_time=0.4)
        _play(self, FadeIn(lbl("first test", 4.70, -1.75, 40)), run_time=0.3)
        _done(self)


class B10_JudgeWrong(Scene):
    """The judge stamps 'supported' on a slip that is wrong — so an unmeasured verdict is flagged."""
    def construct(self):
        self.add(floor_shadow(-2.45, -2.25, 3.6))
        s = qslip(-2.45, -0.85, 2.6, 1.5)
        wrong = VGroup(Line([-3.35, -0.35, 0], [-2.75, -0.95, 0], color=INK, stroke_width=7),
                       Line([-3.35, -0.95, 0], [-2.75, -0.35, 0], color=INK, stroke_width=7))
        self.add(s, wrong, lbl("risk", -2.45, 2.72, 46))
        self.wait(0.25)

        until(self, "like a false")
        st = stamp(-2.45, 1.15, "supported", 2.9)
        st.shift(UP * 1.15).set_opacity(0)
        _play(self, st.animate.shift(DOWN * 1.15).set_opacity(1), run_time=0.55, rate_func=ease_in)

        until(self, "gets a warning")
        flag = warn_flag(2.75, 0.15, 2.5)
        flag.shift(DOWN * 1.9)
        _play(self, flag.animate.shift(UP * 1.9), run_time=0.7)
        _play(self, FadeIn(lbl("warning", 3.35, -1.65, 44)), run_time=0.35)
        _play(self, GrowFromCenter(Dot([2.75, 1.52, 0], radius=0.11, color=TERRA)), run_time=0.3)
        _done(self)


class B11_HaveNew(Scene):
    """One box already stands (RAG pipelines in Python) and the repo's git history beside it.
    Three NEW skills arrive one at a time, each on the phrase that names it (law 5: the motion
    carries the claim — the viewer sees the 'new' column fill as the voice lists it)."""
    def construct(self):
        self.add(DashedLine([0.15, -2.75, 0], [0.15, 2.75, 0], color=BAR1, stroke_width=4, dash_length=0.16))
        self.add(lbl("have", -4.60, 2.30, 48), lbl("new", 4.75, 2.75, 48))
        self.add(floor_shadow(-4.60, -1.05, 3.0))
        isoL = Iso(-4.60, -0.90, 0.85)
        self.wait(0.25)

        until(self, "RAG pipelines")
        box = isoL.box(0, 0, 0, 1.9, 1.9, 0.9)
        _play(self, FadeIn(box), run_time=0.5)
        _play(self, FadeIn(lbl("RAG pipelines", -4.60, -1.85, 36)), run_time=0.3)

        until(self, "my RideReady repo")
        trunk = Line([-1.60, -1.10, 0], [-1.60, 1.10, 0], color=INK, stroke_width=6)
        commits = VGroup(*[Dot([-1.60, y, 0], radius=0.13, color=INK) for y in (-1.10, -0.45, 0.30, 1.10)])
        arc = ArcBetweenPoints([-1.60, -0.10, 0], [-0.85, 0.55, 0], angle=-0.9,
                               stroke_color=INK, stroke_width=6)
        _play(self, Create(trunk), run_time=0.45)
        _play(self, Create(arc), FadeIn(commits), run_time=0.45)
        _play(self, GrowFromCenter(Dot([-0.85, 0.55, 0], radius=0.13, color=TERRA)),
              FadeIn(lbl("git history", -1.60, -1.98, 36)), run_time=0.35)

        # One dotted box per NEW skill — dotted because these do not exist yet, the same
        # convention B02/B04/B12 use. Each lands on its own spoken phrase.
        for y, text, phrase in ((1.45, "splitting claims", "splitting claims"),
                                (0.00, "LLM judges", "LLM judges"),
                                (-1.45, "own error", "measuring a verifier")):
            until(self, phrase)
            shell = dotted(Rectangle(width=2.2, height=0.95).move_to([4.75, y, 0]), n=3)
            _play(self, Create(shell), FadeIn(lbl(text, 2.15, y, 36)), run_time=0.45)
        _done(self)


class B12_ExistsWillExist(Scene):
    """Solid on the left is what exists today. Dotted on the right is what does not, yet."""
    def construct(self):
        self.add(DashedLine([0.0, -2.75, 0], [0.0, 2.75, 0], color=BAR1, stroke_width=4, dash_length=0.16))
        self.add(lbl("exists", -3.25, 2.95, 46), lbl("will exist", 3.25, 2.95, 46))
        self.add(floor_shadow(-4.60, -2.62, 3.0))
        doc = manual_page(-4.95, 1.55, 1.9, 1.25)
        isoR = Iso(-1.95, -0.35, 0.85)
        repo = isoR.box(0, 0, 0, 1.5, 1.5, 1.1)
        rec = manual_page(-4.60, -1.85, 1.9, 1.25)
        self.add(doc, repo, rec)
        self.wait(0.25)

        until(self, "Everything else")
        shells = [dotted(Rectangle(width=2.2, height=1.3).move_to([2.35, 1.25, 0]), n=3),
                  dotted(Rectangle(width=2.2, height=1.3).move_to([4.05, -0.25, 0]), n=3),
                  dotted(Rectangle(width=2.2, height=1.3).move_to([2.35, -1.75, 0]), n=3)]
        for sh in shells:
            _play(self, Create(sh), run_time=0.55)

        until(self, "come next")
        _play(self, GrowFromCenter(Dot([3.55, -1.75, 0], radius=0.12, color=TERRA)), run_time=0.35)
        _done(self)


class BOUT_Title(Scene):
    """Title outro. No channel handle, no mascot — the author's own name (rule 1)."""
    def construct(self):
        t = T("Veracite", 138, color=INK, bold=True).move_to([0, 0.85, 0])
        self.add(t)
        self.wait(0.22)
        rule = Line([-2.35, -0.25, 0], [2.35, -0.25, 0], color=TERRA, stroke_width=9)
        _play(self, Create(rule), run_time=0.45)
        caps = VGroup(Dot([-2.35, -0.25, 0], radius=0.10, color=TERRA),
                      Dot([2.35, -0.25, 0], radius=0.10, color=TERRA))
        _play(self, FadeIn(T("Tanmay Chandan", 62, color=INK).move_to([0, -1.15, 0])),
              GrowFromCenter(caps), run_time=0.45)
        _done(self)
