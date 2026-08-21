"""
Milo, as a presenter that can stand in the corner of a scene and stay alive.

Two things this fixes over a plain ImageMobject swap:

1. **The poses are normalised.** The supplied PNGs are all cropped differently, so
   giving them a common ``height`` makes Milo visibly grow and jump every time his
   expression changes. Here each pose is measured from its own alpha channel, and all
   of them are aligned on the same two features: the bottom of his feet, and the
   horizontal centre of his head. Body height (head crown to feet, ignoring the leaf)
   is what gets matched, not the crop.

2. **He breathes on his own.** A single updater drives a slow rise and fall, a small
   sway, and a settle after each pose change, all off scene time. It runs during every
   other animation in the scene, so Milo is never a frozen sticker while the maths
   moves.
"""

from functools import lru_cache
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

ASSET_DIR = Path(__file__).parent / "assets"

POSES = {
    "neutral": "milo_neutral.png",
    "happy": "milo_happy.png",
    "surprised": "milo_surprised.png",
    "thinking": "milo_thinking.png",
    "excited": "milo_excited.png",
    "wink": "milo_wink.png",
}

_ALPHA_CUTOFF = 25
# A row is "body" once it is wider than this fraction of the widest row. Below it we
# are still in the stem and leaf, which differ wildly between poses and must not be
# allowed to set the scale.
_BODY_ROW_FRACTION = 0.55


@lru_cache(maxsize=None)
def _pose_metrics(pose: str):
    """Measure one pose in pixels: image size, feet row, head crown row, head centre."""
    path = ASSET_DIR / POSES[pose]
    with Image.open(path) as im:
        alpha = np.array(im.convert("RGBA"))[:, :, 3] > _ALPHA_CUTOFF

    rows = alpha.sum(axis=1)
    filled = np.flatnonzero(rows)
    top, feet = int(filled[0]), int(filled[-1])

    threshold = _BODY_ROW_FRACTION * rows[top : feet + 1].max()
    crown = int(next(y for y in range(top, feet + 1) if rows[y] > threshold))

    body_px = feet - crown + 1
    # Centre on the head band only. Arms and props swing the full bounding box around,
    # the head does not.
    band = alpha[crown : crown + max(1, int(0.35 * body_px)), :]
    cols = np.flatnonzero(band.any(axis=0))
    centre_x = (int(cols[0]) + int(cols[-1])) / 2.0

    height, width = alpha.shape
    return {
        "w": width,
        "h": height,
        "body_px": body_px,
        "feet": feet,
        "cx": centre_x,
    }


class MiloActor(Group):
    """Milo standing at a fixed anchor point, breathing, able to change expression.

    ``anchor`` is where the bottom of his feet meets the centre line of his head, so
    he is placed by where he stands rather than by a bounding box.
    """

    def __init__(self, anchor, body_height=2.4, pose="neutral", **kwargs):
        super().__init__(**kwargs)

        self.anchor = np.array(anchor, dtype=float)
        self.body_height = body_height

        self.t = 0.0
        self.speaking = False
        self.hop = 0.0
        self._settle = 0.0  # decaying impulse, kicked by pose changes and nods
        self._ghosts = []

        self.sprite = self._sprite_for(pose)
        self.add(self.sprite)
        self._place_all()
        self.add_updater(lambda m, dt: self._tick(dt))

    # -- construction -------------------------------------------------------

    def _sprite_for(self, pose):
        if pose not in POSES:
            raise ValueError(f"Unknown Milo pose {pose!r}. Choose from {sorted(POSES)}")
        sprite = ImageMobject(str(ASSET_DIR / POSES[pose]))
        sprite.pose_name = pose
        return sprite

    # -- geometry -----------------------------------------------------------

    def _place(self, sprite, bob, sway, squash):
        """Write the sprite's four corners directly.

        Setting the quad rather than calling scale/rotate keeps this exact frame after
        frame. Repeated relative transforms would drift.
        """
        m = _pose_metrics(sprite.pose_name)
        unit = self.body_height / m["body_px"]
        w, h = m["w"] * unit, m["h"] * unit

        # Where the image centre sits relative to the standing anchor.
        cx = -(m["cx"] + 0.5 - m["w"] / 2) * unit
        cy = ((m["feet"] + 1) - m["h"] / 2) * unit

        # Squash about the feet, and widen slightly to keep him from looking starved.
        sy = squash
        sx = 1.0 / (squash**0.5)

        base = self.anchor + np.array([0.0, bob, 0.0])
        centre = np.array([cx * sx, cy * sy, 0.0])
        half = np.array([w * sx / 2, h * sy / 2, 0.0])

        corners = np.array(
            [
                centre + np.array([-half[0], +half[1], 0.0]),
                centre + np.array([+half[0], +half[1], 0.0]),
                centre + np.array([-half[0], -half[1], 0.0]),
                centre + np.array([+half[0], -half[1], 0.0]),
            ]
        )

        if sway:
            c, s = np.cos(sway), np.sin(sway)
            rot = np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]])
            corners = corners @ rot.T

        sprite.points = corners + base

    def _place_all(self, bob=0.0, sway=0.0, squash=1.0):
        for sprite in self.submobjects:
            if isinstance(sprite, ImageMobject):
                self._place(sprite, bob, sway, squash)

    # -- life ---------------------------------------------------------------

    def _tick(self, dt):
        self.t += dt
        self._settle = max(0.0, self._settle - dt * 2.4)

        # Two breath rates, slightly detuned, so the loop never lands on an obvious beat.
        breath = np.sin(TAU * self.t / 3.1)
        drift = np.sin(TAU * self.t / 7.3 + 1.1)

        gain = 1.55 if self.speaking else 1.0
        bob = 0.030 * gain * breath + 0.012 * drift + self.hop
        squash = 1.0 + 0.016 * gain * np.sin(TAU * self.t / 3.1 + PI / 2)
        sway = (1.4 * DEGREES) * drift + (0.9 * DEGREES) * gain * np.sin(TAU * self.t / 2.3)

        if self._settle > 0:
            # A pose change lands with a short bounce rather than a cut.
            k = self._settle
            bob += 0.055 * k * np.sin(TAU * 1.8 * self.t)
            squash -= 0.045 * k

        self._place_all(bob=bob, sway=sway, squash=squash)

    def nod(self):
        """Kick the settle impulse. Cheap way to punctuate a sentence."""
        self._settle = 1.0
        return self

    # -- expression ---------------------------------------------------------

    def pose(self, name, run_time=0.16):
        """Return an animation that crossfades to another pose.

        Composable, so it can ride along inside a ``self.play(...)`` with the maths
        instead of costing its own beat.
        """
        for ghost in self._ghosts:
            self.remove(ghost)
        self._ghosts.clear()

        if name == self.sprite.pose_name:
            return Wait(run_time, frozen_frame=False)

        incoming = self._sprite_for(name)
        # A z_index stamped on the current sprite must survive pose changes, or Milo
        # silently drops behind whatever he was told to stand in front of.
        incoming.set_z_index(self.sprite.z_index)
        incoming.set_opacity(0.0)
        self.add(incoming)
        self._place_all()

        outgoing = self.sprite
        self._ghosts.append(outgoing)
        self.sprite = incoming
        self._settle = 1.0

        return AnimationGroup(
            outgoing.animate.set_opacity(0.0),
            incoming.animate.set_opacity(1.0),
            run_time=run_time,
            rate_func=smooth,
        )

    def set_pose(self, name):
        """Hard cut, no scene time. Use before Milo is visible."""
        for ghost in self._ghosts:
            self.remove(ghost)
        self._ghosts.clear()
        z = self.sprite.z_index
        self.remove(self.sprite)
        self.sprite = self._sprite_for(name)
        self.sprite.set_z_index(z)
        self.add(self.sprite)
        self._place_all()
        return self

    # -- entrances ----------------------------------------------------------

    def enter(self, scene, run_time=0.7):
        self.sprite.set_opacity(0.0)
        scene.add(self)
        scene.play(
            self.sprite.animate.set_opacity(1.0),
            run_time=run_time,
            rate_func=smooth,
        )
        self.nod()
        return self

    def jump(self, height=0.42, run_time=0.62):
        """An arc hop, driven through the same updater so it composes with breathing."""

        def drive(_, alpha):
            self.hop = height * np.sin(PI * alpha) ** 0.75

        return UpdateFromAlphaFunc(Mobject(), drive, run_time=run_time, rate_func=linear)

    def celebrate(self, scene, run_time=0.9):
        """A big hop and a smaller one, sized to fill ``run_time``.

        Takes a duration because the caller knows how long the narration line is,
        and a fixed celebration against a slower voice leaves Milo standing still
        for the rest of it.
        """
        first = max(0.35, run_time * 0.5)
        second = max(0.25, run_time - first)
        scene.play(
            self.pose("excited", run_time=0.14),
            self.jump(height=0.42, run_time=first),
        )
        scene.play(self.jump(height=0.24, run_time=second))
        self.hop = 0.0
        self.nod()
        return self

    def shift_anchor(self, delta):
        self.anchor = self.anchor + np.array(delta, dtype=float)
        self._place_all()
        return self
