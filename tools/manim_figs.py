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

# The house palette, from docs/figure-design-system.md.
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

    # ---- render ---------------------------------------------------------
    def _geometry_svg(self):
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
        cam.capture_mobjects(self.mobjects)
        surface.finish()
        s = buf.getvalue().decode("utf-8")
        # keep only the drawing, drop cairo's xml prolog and root <svg>
        inner = s[s.index(">", s.index("<svg")) + 1:s.rindex("</svg>")]
        inner = re.sub(r"rgb\(([^)]*)\)", _pct_to_hex, inner)
        inner = re.sub(r'\s+(fill|stroke)-opacity="1"', "", inner)
        inner = re.sub(r'\s+stroke-miterlimit="10"', "", inner)
        inner = re.sub(r"<g [^>]*>|</g>", "", inner)
        return inner.strip()

    def svg(self):
        parts = [
            f'<svg viewBox="0 0 {self.w} {self.h}" xmlns="http://www.w3.org/2000/svg"'
            f' role="img" aria-label="{self.aria}"'
            f' font-family="Space Grotesk, sans-serif">',
            self._geometry_svg(),
        ]
        for L in self.labels:
            style = f' font-style="italic"' if L["italic"] else ""
            parts.append(
                f'<text x="{L["x"]:.1f}" y="{L["y"]:.1f}" font-size="{L["size"]}"'
                f' font-weight="{L["weight"]}" fill="{L["color"]}"'
                f' text-anchor="{L["anchor"]}"'
                f' dominant-baseline="{L["baseline"]}"{style}>{L["text"]}</text>')
        parts.append("</svg>")
        return "".join(parts)

    def write(self, path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.svg())
        return path
