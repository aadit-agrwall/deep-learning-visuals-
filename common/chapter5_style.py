"""
common/chapter5_style.py

Shared animation infrastructure for Chapter 5+ (Machine Learning / Deep
Learning) pages. Every page scene should inherit from Chapter5Scene instead
of MovingCameraScene directly, and use self.txt(), self.formula(), etc.
instead of redefining these per file.

Usage in a page file:

    from manim import *
    from common.chapter5_style import Chapter5Scene
    from common import palette as pal

    class Page_102(Chapter5Scene):
        PAGE_NO = "102"

        def construct(self):
            self.init_page()  # sets bg, adds footer, seeds RNG

            title = self.txt("Some title", 30, pal.TEXT, BOLD)
            title.to_edge(UP, buff=0.6)
            self.type_in(title)
            ...
            self.dust_wipe([title, ...])
"""

import random
import numpy as np
from manim import *

from common import palette as pal


# ------------------------------------------------------------------
# Global render config (1:1 square, matches the rest of chapter05)
# ------------------------------------------------------------------
config.background_color = pal.BG
config.frame_width = 9
config.frame_height = 9
config.pixel_width = 1080
config.pixel_height = 1080
config.frame_rate = 60


class Chapter5Scene(MovingCameraScene):
    """
    Mixin/base Scene for all Chapter 5 pages. Provides:
      - text/formula/mono helpers with consistent fonts & defaults
      - type_in(): typewriter reveal
      - dust_wipe(): linear left->right geometric wipe transition
      - clear_scene(): plain fade fallback (rarely needed; prefer dust_wipe)
      - make_footer() / init_page(): consistent "ML-xxx" footer + black bg + RNG seed
    """

    # Override in each page subclass, e.g. PAGE_NO = "102"
    PAGE_NO = "000"

    # Override per page if you want a different deterministic layout seed
    RNG_SEED = 42

    # --------------------------------------------------------------
    # Setup
    # --------------------------------------------------------------

    def init_page(self):
        """Call once at the top of construct(). Sets background, seeds
        random, and adds the persistent ML-xxx footer."""
        random.seed(self.RNG_SEED)
        self.camera.background_color = pal.BG
        footer = self.make_footer()
        self.add(footer)
        return footer

    # --------------------------------------------------------------
    # Text / formula helpers
    # --------------------------------------------------------------

    def txt(self, text, size=26, color=None, weight=NORMAL, font="DejaVu Serif"):
        if color is None:
            color = pal.TEXT
        return Text(text, font=font, font_size=size, color=color, weight=weight)

    def mono(self, text, size=18, color=None):
        if color is None:
            color = pal.TEXT
        return Text(text, font="DejaVu Sans Mono", font_size=size, color=color)

    def formula(self, tex, size=32, color=None):
        if color is None:
            color = pal.TEXT
        return MathTex(tex, font_size=size, color=color)

    def fit_width(self, obj, width=7.4):
        if obj.width > width:
            obj.scale_to_fit_width(width)
        return obj

    # --------------------------------------------------------------
    # Footer
    # --------------------------------------------------------------

    def make_footer(self):
        f = self.txt(f"ML-{self.PAGE_NO}", 20, pal.FOOTER_COLOR, font="DejaVu Sans Mono")
        f.to_edge(DOWN, buff=0.35)
        return f

    # --------------------------------------------------------------
    # Reveal: typewriter effect
    # --------------------------------------------------------------

    def type_in(self, mobj, run_time=1.2):
        """Typewriter-style reveal. Works on Text/MathTex mobjects built
        from characters; for grouped VGroups prefer calling this per child
        or use FadeIn/Create for non-text shapes."""
        self.play(AddTextLetterByLetter(mobj), run_time=run_time)

    def type_group(self, mobjs, run_time_each=0.8, lag=0.2):
        """Type a list of text mobjects in sequence with a short pause
        between each."""
        for m in mobjs:
            self.type_in(m, run_time=run_time_each)
            self.wait(lag)

    # --------------------------------------------------------------
    # Transition: geometric linear dust wipe (left -> right)
    # --------------------------------------------------------------

    def dust_wipe(self, mobjects, run_time=2.0, direction=RIGHT, distance=9.5):
        """
        Wipes the given mobjects off screen as a single clean geometric
        sweep: every fragment travels the SAME direction at a CONSTANT
        (linear) rate, staggered by position along that direction so it
        reads as one coherent wipe rather than a random explosion.

        mobjects: list of top-level Mobjects to clear (their footer should
                  NOT be included — footer persists across the whole page).
        """
        targets = []
        for m in mobjects:
            if len(m.submobjects) > 0:
                targets.extend(m.family_members_with_points())
            else:
                targets.append(m)
        if not targets:
            return

        direction = np.array(direction, dtype=float)
        direction = direction / np.linalg.norm(direction)

        # project each fragment's position onto the wipe direction to get
        # its stagger order
        projections = [np.dot(sm.get_center(), direction) for sm in targets]
        min_p, max_p = min(projections), max(projections)
        span = max(max_p - min_p, 0.01)

        travel = direction * distance
        anims = []
        for sm in targets:
            anims.append(sm.animate.shift(travel).set_opacity(0))

        order = np.argsort(projections)
        ordered_anims = [anims[i] for i in order]

        self.play(
            LaggedStart(*ordered_anims, lag_ratio=0.02),
            run_time=run_time,
            rate_func=linear,
        )
        self.remove(*mobjects)

    # --------------------------------------------------------------
    # Transition: plain fade (fallback, rarely used — prefer dust_wipe)
    # --------------------------------------------------------------

    def clear_scene(self, run_time=0.45):
        mobs = [m for m in self.mobjects if not self._is_footer(m)]
        if mobs:
            self.play(*[FadeOut(mob) for mob in mobs], run_time=run_time)
        self.wait(0.2)

    def _is_footer(self, mob):
        # Heuristic: footer is bottom-edge-anchored mono text; skip removing it.
        return False  # kept simple; callers should pass explicit lists to dust_wipe instead

    # --------------------------------------------------------------
    # Camera utility: quick zoom emphasis
    # --------------------------------------------------------------

    def zoom_pulse(self, target_mobj, zoom_scale=0.85, run_time_in=0.8, run_time_out=0.7, hold=0.4):
        """Briefly zoom the camera in on target_mobj, hold, then zoom back out."""
        self.play(
            self.camera.frame.animate.scale(zoom_scale).move_to(target_mobj.get_center()),
            run_time=run_time_in,
        )
        self.wait(hold)
        self.play(
            self.camera.frame.animate.scale(1 / zoom_scale).move_to(ORIGIN),
            run_time=run_time_out,
        )
