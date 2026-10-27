"""Page 111 - Figure 5.2: underfitting / appropriate capacity / overfitting,
plus the idea of representational capacity."""
import numpy as np
from manim import *

import common.palette as pal
from common.chapter5_style import Chapter5Scene


XS = np.array([0.00, 0.36, 0.45, 0.86, 0.89, 0.93])


def true_fn(x):
    return 0.92 - 2.6 * (x - 0.42) ** 2


YS = true_fn(XS)


def fit_poly(deg):
    V = np.vander(XS, deg + 1, increasing=True)
    w = np.linalg.pinv(V) @ YS
    return lambda x: float(np.polynomial.polynomial.polyval(x, w))


class Page_111(Chapter5Scene):
    PAGE_NO = "111"
    RNG_SEED = 1111

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
        with open("assets/audio/raw/page_111_events.json", "w") as f:
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

    def make_panel(self, width=3.0, height=3.9):
        axes = Axes(
            x_range=[0, 1, 1], y_range=[0, 1, 1],
            x_length=width, y_length=height, tips=False,
            axis_config={"include_ticks": False, "include_numbers": False,
                         "color": pal.TEXT},
        )
        frame = SurroundingRectangle(axes, buff=0, color=pal.TEXT, stroke_width=3)
        dots = VGroup(*[
            Dot(axes.c2p(x, y), radius=0.07, color=pal.INPUT)
            for x, y in zip(XS, YS)
        ])
        return axes, frame, dots

    def curve_for(self, axes, fn, color):
        ts = np.linspace(0, 1, 600)
        vals = np.asarray([float(fn(t)) for t in ts])
        segs, cur = VGroup(), []
        for t, v in zip(ts, vals):
            if 0 <= v <= 1:
                cur.append(axes.c2p(t, v))
            else:
                if len(cur) > 1:
                    segs.add(VMobject(color=color, stroke_width=5)
                             .set_points_as_corners(cur))
                cur = []
        if len(cur) > 1:
            segs.add(VMobject(color=color, stroke_width=5)
                     .set_points_as_corners(cur))
        return segs

    def construct(self):
        self.init_page()

        # Scene 1: training set
        title = self.txt("Figure 5.2: one dataset, three models", color=pal.TEXT)
        self.fit_width(title, config.frame_width * 0.9)
        title.to_edge(UP, buff=0.9)
        self.type_in(title)

        axes, frame, dots = self.make_panel(width=4.4, height=4.6)
        panel = VGroup(axes, frame, dots).move_to(ORIGIN).shift(DOWN * 0.1)
        self.play(Create(axes), Create(frame))
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots],
                              lag_ratio=0.15))

        note = self.txt("Data: sample x, then y = quadratic(x)", color=pal.INPUT)
        self.fit_width(note, config.frame_width * 0.85)
        note.to_edge(DOWN, buff=1.3)
        self.type_in(note)
        self.wait(1)
        self.dust_wipe([title, panel, note])

        # Scene 2: underfitting
        head = self.txt("Underfitting", color=pal.ERROR)
        head.to_edge(UP, buff=0.9)
        self.type_in(head)
        axes, frame, dots = self.make_panel(width=4.2, height=4.4)
        panel = VGroup(axes, frame, dots).move_to(ORIGIN).shift(DOWN * 0.1)
        self.play(Create(axes), Create(frame), FadeIn(dots))
        line = self.curve_for(axes, fit_poly(1), pal.ERROR)
        self.play(Create(line))
        cap = self.txt("A line cannot capture the curvature", color=pal.TEXT)
        self.fit_width(cap, config.frame_width * 0.88)
        cap.to_edge(DOWN, buff=1.3)
        self.type_in(cap)
        self.wait(1)
        self.dust_wipe([head, panel, line, cap])

        # Scene 3: appropriate capacity
        head = self.txt("Appropriate capacity", color=pal.OUTPUT)
        head.to_edge(UP, buff=0.9)
        self.type_in(head)
        axes, frame, dots = self.make_panel(width=4.2, height=4.4)
        panel = VGroup(axes, frame, dots).move_to(ORIGIN).shift(DOWN * 0.1)
        self.play(Create(axes), Create(frame), FadeIn(dots))
        quad = self.curve_for(axes, fit_poly(2), pal.OUTPUT)
        self.play(Create(quad))
        cap = self.txt("Quadratic model = true structure, so it generalizes",
                       color=pal.TEXT)
        self.fit_width(cap, config.frame_width * 0.88)
        cap.to_edge(DOWN, buff=1.3)
        self.type_in(cap)
        self.wait(1)
        self.dust_wipe([head, panel, quad, cap])

        # Scene 4: overfitting
        head = self.txt("Overfitting", color=pal.ERROR)
        head.to_edge(UP, buff=0.9)
        self.type_in(head)
        axes, frame, dots = self.make_panel(width=4.2, height=4.4)
        panel = VGroup(axes, frame, dots).move_to(ORIGIN).shift(DOWN * 0.1)
        self.play(Create(axes), Create(frame), FadeIn(dots))
        wild = self.curve_for(axes, fit_poly(9), pal.ERROR)
        self.play(Create(wild))
        cap = self.formula(r"\text{degree } 9:\ 10 \text{ parameters} > 6 \text{ points}")
        cap.set_color(pal.FORMULA)
        self.fit_width(cap, config.frame_width * 0.88)
        cap.to_edge(DOWN, buff=1.6)
        self.play(Write(cap))
        cap2 = self.txt("Infinitely many curves hit every point", color=pal.TEXT)
        self.fit_width(cap2, config.frame_width * 0.88)
        cap2.next_to(cap, DOWN, buff=0.3)
        self.type_in(cap2)
        self.wait(1)
        self.dust_wipe([head, panel, wild, cap, cap2])

        # Scene 5: representational capacity
        head = self.txt("Representational capacity", color=pal.DISTRIBUTION)
        self.fit_width(head, config.frame_width * 0.9)
        head.to_edge(UP, buff=0.9)
        self.type_in(head)
        family = self.txt("Model = family of functions", color=pal.INPUT)
        algo = self.txt("Algorithm picks one by tuning parameters", color=pal.OUTPUT)
        goal = self.txt("Goal: reduce the training objective", color=pal.FORMULA)
        stack = VGroup(family, algo, goal).arrange(DOWN, buff=0.7)
        self.fit_width(stack, config.frame_width * 0.88)
        stack.move_to(ORIGIN)
        for line_obj in stack:
            self.type_in(line_obj)
            self.wait(0.4)
        box = SurroundingRectangle(stack, color=pal.DISTRIBUTION, buff=0.35)
        self.play(Create(box))
        self.wait(1)
        self.dust_wipe([head, stack, box])

        # Scene 6: takeaway
        take = self.txt("Capacity must match the true structure of the task",
                        color=pal.TEXT)
        self.fit_width(take, config.frame_width * 0.88)
        take.move_to(ORIGIN)
        self.type_in(take)
        underline = Line(take.get_corner(DL) + DOWN * 0.15,
                         take.get_corner(DR) + DOWN * 0.15,
                         color=pal.OUTPUT, stroke_width=5)
        self.play(Create(underline))
        self.zoom_pulse(VGroup(take, underline))
        self.wait(1)
