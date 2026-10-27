"""Page 112 - effective capacity, Occam's razor, VC dimension, bounds."""
import numpy as np
from manim import *

import common.palette as pal
from common.chapter5_style import Chapter5Scene


class Page_112(Chapter5Scene):
    PAGE_NO = "112"
    RNG_SEED = 1121

    # ---- timing log for music sync ----
    def _now(self):
        try:
            return float(self.renderer.time)
        except Exception:
            return float(self.time)

    def _log(self, kind, t0, t1, n=0):
        import json, os
        ev = getattr(self, "_events", None)
        if ev is None:
            ev = self._events = []
        ev.append({"kind": kind, "t0": t0, "t1": t1, "n": n})
        os.makedirs("assets/audio/raw", exist_ok=True)
        with open("assets/audio/raw/page_112_events.json", "w") as f:
            json.dump(ev, f)

    def type_in(self, *args, **kwargs):
        t0 = self._now()
        r = super().type_in(*args, **kwargs)
        mob = args[0] if args else None
        try:
            n = len(mob.submobjects)
        except Exception:
            n = 0
        self._log("type", t0, self._now(), n)
        return r

    def dust_wipe(self, *args, **kwargs):
        t0 = self._now()
        r = super().dust_wipe(*args, **kwargs)
        self._log("wipe", t0, self._now())
        return r

    def construct(self):
        self.init_page()
        W = config.frame_width

        # ===== Scene 1: effective vs representational capacity ==========
        head = self.txt("Effective capacity", color=pal.DISTRIBUTION)
        head.to_edge(UP, buff=0.9)
        self.type_in(head)

        rep = Rectangle(width=6.6, height=0.9, color=pal.INPUT, stroke_width=4)
        eff = Rectangle(width=3.4, height=0.9, color=pal.OUTPUT, stroke_width=4)
        eff.set_fill(pal.OUTPUT, opacity=0.35)
        rep.move_to(UP * 0.8)
        eff.move_to(rep.get_left() + RIGHT * 1.7 + DOWN * 1.5)
        rep_l = self.txt("Representational capacity", color=pal.INPUT)
        eff_l = self.txt("Effective capacity", color=pal.OUTPUT)
        self.fit_width(rep_l, W * 0.8)
        self.fit_width(eff_l, W * 0.6)
        rep_l.next_to(rep, UP, buff=0.25)
        eff_l.next_to(eff, DOWN, buff=0.25)
        self.play(Create(rep))
        self.type_in(rep_l)
        self.play(Create(eff))
        self.type_in(eff_l)

        cap = self.txt("The optimizer finds a good function, not the best",
                       color=pal.ERROR)
        self.fit_width(cap, W * 0.88)
        cap.to_edge(DOWN, buff=1.3)
        self.type_in(cap)
        self.wait(1)
        self.dust_wipe([head, rep, eff, rep_l, eff_l, cap])

        # ===== Scene 2: Occam's razor ====================================
        head = self.txt("Occam's razor", color=pal.DISTRIBUTION)
        head.to_edge(UP, buff=0.9)
        self.type_in(head)

        left = VGroup(
            RoundedRectangle(width=3.0, height=2.0, corner_radius=0.2,
                             color=pal.OUTPUT),
            self.txt("Simple", color=pal.OUTPUT),
        )
        left[1].move_to(left[0])
        right = VGroup(
            RoundedRectangle(width=3.0, height=2.0, corner_radius=0.2,
                             color=pal.ERROR),
            self.txt("Complex", color=pal.ERROR),
        )
        right[1].move_to(right[0])
        pair = VGroup(left, right).arrange(RIGHT, buff=0.7).move_to(ORIGIN)
        self.play(Create(left[0]), Create(right[0]))
        self.type_in(left[1])
        self.type_in(right[1])

        same = self.txt("Both explain the data equally well", color=pal.TEXT)
        self.fit_width(same, W * 0.88)
        same.next_to(pair, UP, buff=0.6)
        self.type_in(same)
        self.play(right.animate.set_opacity(0.3),
                  left[0].animate.set_fill(pal.OUTPUT, opacity=0.25))

        cap = self.txt("Choose the simplest hypothesis", color=pal.OUTPUT)
        self.fit_width(cap, W * 0.88)
        cap.to_edge(DOWN, buff=1.3)
        self.type_in(cap)
        self.wait(1)
        self.dust_wipe([head, pair, same, cap])

        # ===== Scene 3: VC dimension =====================================
        head = self.txt("VC dimension", color=pal.DISTRIBUTION)
        head.to_edge(UP, buff=0.9)
        self.type_in(head)

        dots = VGroup(*[Dot(radius=0.2, color=pal.INPUT) for _ in range(3)])
        dots.arrange(RIGHT, buff=1.2).move_to(UP * 0.4)
        self.play(FadeIn(dots, lag_ratio=0.2))
        patterns = [
            (pal.OUTPUT, pal.OUTPUT, pal.ERROR),
            (pal.ERROR, pal.OUTPUT, pal.ERROR),
            (pal.OUTPUT, pal.ERROR, pal.ERROR),
            (pal.ERROR, pal.ERROR, pal.OUTPUT),
        ]
        for pat in patterns:
            self.play(*[d.animate.set_color(c) for d, c in zip(dots, pat)],
                      run_time=0.5)

        l1 = self.txt("Largest m binary classifier can", color=pal.TEXT)
        l2 = self.txt("label arbitrarily", color=pal.TEXT)
        lines = VGroup(l1, l2).arrange(DOWN, buff=0.2)
        self.fit_width(lines, W * 0.85)
        lines.next_to(dots, DOWN, buff=0.8)
        self.type_in(l1)
        self.type_in(l2)
        fm = self.formula(r"2^m \text{ labelings}")
        fm.set_color(pal.FORMULA)
        fm.next_to(lines, DOWN, buff=0.5)
        self.play(Write(fm))
        self.wait(1)
        self.dust_wipe([head, dots, lines, fm])

        # ===== Scene 4: generalization bound =============================
        head = self.txt("Bounding the gap", color=pal.DISTRIBUTION)
        head.to_edge(UP, buff=0.9)
        self.type_in(head)

        fm = self.formula(
            r"\text{gap} \le f\big(\text{capacity}\ \uparrow,\ m\ \downarrow\big)")
        fm.set_color(pal.FORMULA)
        self.fit_width(fm, W * 0.9)
        fm.move_to(UP * 1.2)
        self.play(Write(fm))

        up = self.txt("Grows with model capacity", color=pal.ERROR)
        dn = self.txt("Shrinks with more examples", color=pal.OUTPUT)
        st = VGroup(up, dn).arrange(DOWN, buff=0.5)
        self.fit_width(st, W * 0.85)
        st.next_to(fm, DOWN, buff=0.8)
        self.type_in(up)
        self.type_in(dn)

        loose = self.txt("Often loose, rarely used for deep learning",
                         color=pal.TEXT)
        self.fit_width(loose, W * 0.88)
        loose.to_edge(DOWN, buff=1.3)
        self.type_in(loose)
        self.wait(1)
        self.dust_wipe([head, fm, st, loose])

        # ===== Scene 5: training error vs capacity =======================
        head = self.txt("Training error vs capacity", color=pal.DISTRIBUTION)
        self.fit_width(head, W * 0.9)
        head.to_edge(UP, buff=0.9)
        self.type_in(head)

        axes = Axes(x_range=[0, 1, 1], y_range=[0, 1, 1],
                    x_length=5.2, y_length=3.6, tips=False,
                    axis_config={"include_ticks": False,
                                 "include_numbers": False,
                                 "color": pal.TEXT})
        axes.move_to(DOWN * 0.1)
        xl = self.txt("capacity", color=pal.TEXT)
        xl.scale(0.8).next_to(axes, DOWN, buff=0.25)
        yl = self.txt("training error", color=pal.TEXT)
        yl.scale(0.8).rotate(PI / 2).next_to(axes, LEFT, buff=0.25)
        self.play(Create(axes), FadeIn(xl), FadeIn(yl))
        curve = axes.plot(lambda x: 0.18 + 0.75 * np.exp(-5 * x),
                          x_range=[0, 1], color=pal.INPUT, stroke_width=5)
        floor = DashedLine(axes.c2p(0, 0.18), axes.c2p(1, 0.18),
                           color=pal.OUTPUT)
        self.play(Create(curve), run_time=1.5)
        self.play(Create(floor))

        cap = self.txt("Falls to the minimum possible error", color=pal.TEXT)
        self.fit_width(cap, W * 0.88)
        cap.to_edge(DOWN, buff=1.3)
        self.type_in(cap)
        self.wait(1)
        self.dust_wipe([head, axes, xl, yl, curve, floor, cap])

        # ===== Scene 6: takeaway =========================================
        t1 = self.txt("Simple enough to generalize,", color=pal.TEXT)
        t2 = self.txt("complex enough to fit", color=pal.TEXT)
        take = VGroup(t1, t2).arrange(DOWN, buff=0.25)
        self.fit_width(take, W * 0.88)
        take.move_to(ORIGIN)
        self.type_in(t1)
        self.type_in(t2)
        underline = Line(take.get_corner(DL) + DOWN * 0.2,
                         take.get_corner(DR) + DOWN * 0.2,
                         color=pal.OUTPUT, stroke_width=5)
        self.play(Create(underline))
        self.zoom_pulse(VGroup(take, underline))
        self.wait(1)
