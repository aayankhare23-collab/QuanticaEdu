#!/usr/bin/env python3
"""Render Quantica lesson figures with manim, out as house-style inline SVG.

Manim CE only writes raster stills (png|gif|mp4|webm|mov), so this module points
manim's own cairo renderer at a `cairo.SVGSurface` instead of the in-memory pixel
buffer. Every mobject is already a bezier VMobject, so the result is real vector
SVG, not a traced bitmap.

Two deliberate choices:

* Manim draws GEOMETRY only. Labels are emitted as live `<text>` elements in
  Space Grotesk, so they match the app's webfont exactly, stay selectable and
  accessible, and satisfy `check_lesson.py`'s font check honestly. Manim's own
  `Text` would bake glyphs into paths using whatever font the machine happens to
  have, and Space Grotesk is not installed here.
* Colours are un-swapped. Manim reverses RGB on purpose (`rgbas[0][2::-1]`)
  because a cairo ARGB32 image surface is byte-reversed. An SVG surface is not,
  so the swap has to be undone or every figure ships with its channels flipped.

Usage: build a Fig, add mobjects and labels, call `.write()`. See
`tools/lesson-figs/` for the chapter 7 figures built on it.
"""
from __future__ import annotations

import io
import re

import cairo
import numpy as np
from manim import VMobject
from manim.camera.camera import Camera

# The house palette, from docs/figure-design-system.md. These are the course app's
# :root tokens, which is the surface a lesson figure actually renders on (a white
# .lessonfig card inside the app). The lime/slate WEMBI set belongs to the marketing
# region and the ads, per the note in ~/manim-projects/milo_manim/quantica.py.
#
# The STRUCTURE, though, is taken from that brand kit: two surfaces and one rule.
# Slate is the ordinary surface, gold is the surface that matters, and a near-black
# editorial rule separates them. Fills are flat at full opacity and carry an ink
# stroke, rather than the thin unfilled outlines the earlier figures used.
INK = "#0e1726"          # near-black. All rules, and type that has to carry.
SURFACE = "#eef4fb"      # the ordinary surface
SURFACE_EDGE = "#cddff2"
BLUE = "#2f6fe0"
BLUE_DEEP = "#2257c5"
BLUE_LIGHT = "#3b82f6"
GOLD = "#fcd76a"
GOLD_MID = "#f0b429"
GOLD_DEEP = "#8a5a08"
GREY = "#eef1f6"
GREY_MID = "#dbe1ea"
GREY_LINE = "#aab4c2"
SLATE = "#475569"
HAIRLINE = "#e4e9f1"
WHITE = "#ffffff"


def _no_swap_color(self, ctx, rgbas, vmobject):
    """`Camera.set_cairo_context_color` without manim's BGR compensation."""
    import itertools as it

    if len(rgbas) == 1:
        ctx.set_source_rgba(*rgbas[0][:3], rgbas[0][3])
    else:
        points = vmobject.get_gradient_start_and_end_points()
        points = self.transform_points_pre_display(vmobject, points)
        pat = cairo.LinearGradient(*it.chain(*(p[:2] for p in points)))
        for rgba, offset in zip(rgbas, np.linspace(0, 1, len(rgbas))):
            pat.add_color_stop_rgba(offset, *rgba[:3], rgba[3])
        ctx.set_source(pat)
    return self


def _esc(t):
    """Escape label text for SVG.

    A label reading "<" was previously written straight into the markup, producing
    <text ...><</text>. The parser reads that "<" as the start of a tag and the glyph
    silently disappears, with no error anywhere. An inequalities chapter labels "<"
    constantly, so this is not a corner case. Ampersand goes first or it would
    double-escape the entities the other two produce.
    """
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _pct_to_hex(m):
    vals = [float(v.strip().rstrip("%")) for v in m.group(1).split(",")]
    return "#" + "".join(f"{round(v * 255 / 100):02x}" for v in vals)


class Fig:
    """One lesson figure. Scene units in, house-style inline SVG out."""

    def __init__(self, width=580, frame_width=14.0, frame_height=8.0, aria=""):
        self.w = width
        self.h = int(round(width * frame_height / frame_width))
        self.fw, self.fh = frame_width, frame_height
        self.aria = aria
        self.mobjects: list[VMobject] = []
        self.labels: list[dict] = []
        self.anim: list | None = None
        self.anim_dur = 6.0
        self.anim_hold = 0.0
        self.motions: list[dict] = []
        self.draws: list[dict] = []
        self.uid = f'q{abs(hash((width, frame_width, aria))) % 100000:05d}'

    # ---- scene coords -> svg pixel coords -------------------------------
    def px(self, point):
        x, y = float(point[0]), float(point[1])
        return (self.w / self.fw * x + self.w / 2,
                self.h / 2 - self.h / self.fh * y)

    def add(self, *mobjects):
        for m in mobjects:
            self.mobjects.append(m)
        return self

    def label(self, point, text, size=13, weight=500, color=SLATE,
              anchor="middle", dx=0, dy=0, baseline="middle", italic=False):
        """A live <text> label anchored at a scene-coordinate point.

        dx/dy are nudges in SVG pixels, applied after the coordinate transform.
        """
        x, y = self.px(point)
        self.labels.append(dict(x=x + dx, y=y + dy, text=text, size=size,
                                weight=weight, color=color, anchor=anchor,
                                baseline=baseline, italic=italic))
        return self

    def rule(self, y_px, x0_px=42, x1_px=None, width=2.6):
        """The near-black editorial rule that separates the two bands."""
        from manim import Line
        x1 = self.w - x0_px if x1_px is None else x1_px
        self.add(Line(self.sp(x0_px, y_px), self.sp(x1, y_px),
                      color=INK, stroke_width=width))
        return self

    def pill(self, cx_px, cy_px, w_px, h_px, fill=SURFACE, stroke=INK, width=2.6, r=16):
        """A flat filled pill with an ink stroke. The brand kit's core shape."""
        from manim import RoundedRectangle
        ppu = self.w / self.fw
        self.add(RoundedRectangle(corner_radius=r / ppu, width=w_px / ppu,
                                  height=h_px / ppu, fill_color=fill, fill_opacity=1,
                                  stroke_color=stroke, stroke_width=width)
                 .move_to(self.sp(cx_px, cy_px)))
        return self

    def sp(self, x_px, y_px):
        """Pixel position on the canvas -> scene coordinates."""
        return np.array([(x_px - self.w / 2) / (self.w / self.fw),
                         (self.h / 2 - y_px) / (self.w / self.fw), 0.0])

    def mklabel(self, *a, **k):
        """A label dict for a frame, rather than for the static layer."""
        before = len(self.labels)
        self.label(*a, **k)
        return self.labels.pop(before)

    def draw(self, mobjects, dur=6.0, begin=0.0, span=1.0, labels=None, label_at=None):
        """Draw a stroke on progressively, the way a hand would.

        A growing line is not a similarity transform, so `motion` cannot carry it.
        `pathLength="1"` normalises every path to unit length, so one dash pattern
        and one offset animation reveal it regardless of its real length. Smooth at
        the browser's refresh rate, and it costs about a hundred bytes.

        `begin` and `span` are FRACTIONS OF THE CYCLE, not seconds, and the delay is
        baked into keyTimes rather than into SMIL's `begin`. Using `begin` puts each
        stage on its own clock: with dur=8s and begin=4.96s an element repeats on
        4.96, 12.96, 20.96 while its neighbours repeat on 0, 8, 16, so a multi-stage
        figure drifts out of phase after the first pass. One clock for everything.
        """
        self.draws.append(dict(mobjects=mobjects, dur=dur, begin=begin, span=span,
                               labels=labels or [], label_at=label_at))
        return self

    def motion(self, mobjects, keys, dur=6.0, labels=None, label_keys=None,
               spline=True, begin=0.0, about=None):
        """Smooth motion. Manim fixes the geometry AND the keyframes; SVG tweens.

        A flipbook of manim frames tops out around 12 fps before the file gets
        heavy (measured: ~2.4KB per frame, so 30 fps for 7s would be half a
        megabyte for ONE figure). That reads as a slideshow, not as animation.

        So for motion that is a similarity transform, which is most of it, the
        geometry is emitted ONCE and carried by an SVG `<animateTransform>` whose
        `values` are the positions manim computed. The browser then interpolates
        at its own refresh rate, so it is genuinely smooth at any duration and
        costs a few hundred bytes instead of hundreds of kilobytes.

        `keys` is a list of (dx, dy, scale) in SCENE units, one per keyframe.
        `calcMode="spline"` with an ease-in-out control gives 3b1b-style motion
        rather than the constant-velocity look of a linear tween.
        """
        # SVG scale() is about the origin, so scaling has to happen in a frame whose
        # origin sits at `about`. The content is counter-translated by -about, and the
        # animated translate carries it back, which makes the scale local.
        ppu_x, ppu_y = self.w / self.fw, self.h / self.fh
        ax, ay = self.px(about) if about is not None else (0.0, 0.0)
        tr = ";".join(f"{ax + dx * ppu_x:.2f},{ay - dy * ppu_y:.2f}" for dx, dy, _ in keys)
        sc = ";".join(f"{s:.4f}" for _, _, s in keys)
        n = len(keys)
        kt = ";".join(f"{i / (n - 1):.4f}" for i in range(n))
        splines = " ".join(["0.42 0 0.58 1"] * (n - 1)) if spline else None
        # Labels ride the travel but NOT the scale. Text inside a scaled group grows
        # with it, which doubled the type on the way across before this was split out.
        ltr = None
        if label_keys:
            ltr = ";".join(f"{dx * ppu_x:.2f},{-dy * ppu_y:.2f}" for dx, dy in label_keys)
        self.motions.append(dict(mobjects=mobjects, labels=labels or [], tr=tr, sc=sc,
                                 ltr=ltr, kt=kt, splines=splines, dur=dur, begin=begin,
                                 ax=ax, ay=ay,
                                 uniform=all(abs(s - keys[0][2]) < 1e-9 for _, _, s in keys)))
        return self

    def frames(self, builder, n=30, dur=6.0, hold=0.0):
        """Animate. `builder(t)` returns the mobjects for t in [0, 1].

        Manim does the interpolation, which is what it is for. The frames are
        emitted as one self-contained animated SVG rather than a video: each
        frame is a `<g>` and a CSS keyframe shows exactly one at a time. That
        keeps an animated figure a drop-in for a static one, with no binary
        asset, no `<video>` tag, and no change to the fig block schema. It also
        means the SEO pages animate for free, since they embed the same markup.

        `builder(t)` returns either a list of mobjects, or a
        `(mobjects, labels)` pair when text has to travel with the geometry.
        Build those labels with `mklabel`, which takes the same arguments as
        `label` but returns the dict instead of pinning it to the static layer.

        `hold` adds a pause on the last frame, as a fraction of the cycle.
        """
        raw = [builder(i / max(1, n - 1)) for i in range(n)]
        self.anim = [r if isinstance(r, tuple) else (r, []) for r in raw]
        self.anim_dur = dur
        self.anim_hold = hold
        return self

    # ---- render ---------------------------------------------------------
    def _geometry_svg(self, mobjects=None):
        buf = io.BytesIO()
        surface = cairo.SVGSurface(buf, self.w, self.h)
        surface.set_document_unit(cairo.SVGUnit.PX)
        ctx = cairo.Context(surface)
        ctx.set_matrix(cairo.Matrix(self.w / self.fw, 0, 0, -(self.h / self.fh),
                                    self.w / 2, self.h / 2))
        cam = Camera(pixel_width=self.w, pixel_height=self.h,
                     frame_width=self.fw, frame_height=self.fh)
        cam.get_cairo_context = lambda pixel_array: ctx
        cam.set_cairo_context_color = _no_swap_color.__get__(cam, Camera)
        cam.capture_mobjects(self.mobjects if mobjects is None else mobjects)
        surface.finish()
        s = buf.getvalue().decode("utf-8")
        # keep only the drawing, drop cairo's xml prolog and root <svg>
        inner = s[s.index(">", s.index("<svg")) + 1:s.rindex("</svg>")]
        inner = re.sub(r"rgb\(([^)]*)\)", _pct_to_hex, inner)
        inner = re.sub(r'\s+(fill|stroke)-opacity="1"', "", inner)
        inner = re.sub(r'\s+stroke-miterlimit="10"', "", inner)
        inner = re.sub(r"<g [^>]*>|</g>", "", inner)
        return inner.strip()

    def _anim_css(self, n):
        """One frame visible per slot. Negative delays stagger them in order."""
        u, k = self.uid, f'{self.uid}k'
        slot = 100.0 / n
        on = slot * (1 - self.anim_hold) if self.anim_hold else slot
        css = [f'@keyframes {k}{{0%{{opacity:1}}{on:.4f}%{{opacity:1}}'
               f'{on + 0.0001:.4f}%{{opacity:0}}100%{{opacity:0}}}}',
               f'.{u}{{opacity:0;animation:{k} {self.anim_dur}s linear infinite}}']
        # A negative delay of -D starts the frame D seconds in, so frame i lands in
        # slot i only with -(n-i)/n of the cycle. Using -i/n runs the whole thing
        # backwards, which is silent and wrong rather than broken.
        for i in range(n):
            css.append(f'.{u}-{i}{{animation-delay:'
                       f'{-(n - i) * self.anim_dur / n:.4f}s}}')
        # a still figure for anyone who has asked the OS to stop motion
        css.append(f'@media(prefers-reduced-motion:reduce){{'
                   f'.{u}{{animation:none;opacity:0}}.{u}-{n - 1}{{opacity:1}}}}')
        return '<style>' + ''.join(css) + '</style>'

    def svg(self):
        parts = [
            f'<svg viewBox="0 0 {self.w} {self.h}" xmlns="http://www.w3.org/2000/svg"'
            f' role="img" aria-label="{self.aria}"'
            f' font-family="Space Grotesk, sans-serif">',
        ]
        if self.anim:
            parts.append(self._anim_css(len(self.anim)))
        parts.append(self._geometry_svg())
        for d in self.draws:
            inner = self._geometry_svg(d['mobjects'])
            # normalise every stroke to unit length so one offset animation fits all
            inner = re.sub(r'<path ', '<path pathLength="1" stroke-dasharray="1" ', inner)
            b = min(0.999, max(0.0, d['begin']))
            e = min(1.0, b + d['span'])
            kt = f'0;{b:.4f};{e:.4f};1' if b > 0 else f'0;{e:.4f};1'
            vals = '1;1;0;0' if b > 0 else '1;0;0'
            spl = ('0 0 1 1;0.42 0 0.58 1;0 0 1 1' if b > 0
                   else '0.42 0 0.58 1;0 0 1 1')
            anim = (f'<animate attributeName="stroke-dashoffset" values="{vals}"'
                    f' keyTimes="{kt}" dur="{d["dur"]}s" begin="0s"'
                    f' repeatCount="indefinite" calcMode="spline" keySplines="{spl}"/>')
            parts.append(f'<g stroke-dashoffset="1">{anim}{inner}</g>')
            for L in d['labels']:
                at = b + (d['label_at'] if d['label_at'] is not None else d['span'])
                at = min(0.97, at)
                parts.append(f'<g opacity="0"><animate attributeName="opacity"'
                             f' values="0;0;1;1" keyTimes="0;{at:.4f};{at + 0.02:.4f};1"'
                             f' dur="{d["dur"]}s" begin="0s"'
                             f' repeatCount="indefinite"/>{self._text(L)}</g>')
        for m in self.motions:
            inner = self._geometry_svg(m['mobjects'])
            a = (f'<animateTransform attributeName="transform" type="translate"'
                 f' values="{m["tr"]}" keyTimes="{m["kt"]}" dur="{m["dur"]}s"'
                 f' begin="{m["begin"]}s" repeatCount="indefinite"'
                 + (f' calcMode="spline" keySplines="{m["splines"]}"' if m['splines'] else '')
                 + ' additive="sum"/>')
            if not m['uniform']:
                a += (f'<animateTransform attributeName="transform" type="scale"'
                      f' values="{m["sc"]}" keyTimes="{m["kt"]}" dur="{m["dur"]}s"'
                      f' begin="{m["begin"]}s" repeatCount="indefinite"'
                      + (f' calcMode="spline" keySplines="{m["splines"]}"' if m['splines'] else '')
                      + ' additive="sum"/>')
            parts.append(f'<g>{a}<g transform="translate({-m["ax"]:.2f},{-m["ay"]:.2f})">'
                         f'{inner}</g></g>')
            if m['labels']:
                lt = m['ltr'] or m['tr']
                la = (f'<animateTransform attributeName="transform" type="translate"'
                      f' values="{lt}" keyTimes="{m["kt"]}" dur="{m["dur"]}s"'
                      f' begin="{m["begin"]}s" repeatCount="indefinite"'
                      + (f' calcMode="spline" keySplines="{m["splines"]}"' if m['splines'] else '')
                      + '/>')
                parts.append(f'<g>{la}{"".join(self._text(L) for L in m["labels"])}</g>')
        if self.anim:
            for i, (mobs, labs) in enumerate(self.anim):
                parts.append(f'<g class="{self.uid} {self.uid}-{i}">'
                             + self._geometry_svg(mobs)
                             + ''.join(self._text(L) for L in labs) + '</g>')
        for L in self.labels:
            parts.append(self._text(L))
        parts.append("</svg>")
        return "".join(parts)

    def _text(self, L):
        style = ' font-style="italic"' if L["italic"] else ""
        return (
                f'<text x="{L["x"]:.1f}" y="{L["y"]:.1f}" font-size="{L["size"]}"'
                f' font-weight="{L["weight"]}" fill="{L["color"]}"'
                f' text-anchor="{L["anchor"]}"'
                f' dominant-baseline="{L["baseline"]}"{style}>{_esc(L["text"])}</text>')

    def write(self, path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.svg())
        return path
