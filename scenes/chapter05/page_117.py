"""Page 117 - weight decay, regularizers, definition of regularization,
no free lunch and regularization."""
import numpy as np
from manim import *

import common.palette as pal
from common.chapter5_style import Chapter5Scene
from common.sync_log import SyncLogMixin


XS = np.array([0.00, 0.36, 0.45, 0.86, 0.89, 0.93])


def true_fn(x):
    return 0.92 - 2.6 * (x - 0.42) ** 2


YS = true_fn(XS)


def wild_fn(x):
    V = np.vander(XS, 10, increasing=True)
    w = np.linalg.pinv(V) @ YS
    return float(np.polynomial.polynomial.polyval(x, w))


WEIGHTS = {
    "none": [2.4, 1.9, 1.5, 2.1, 1.2],
    "mid": [1.4, 1.1, 0.7, 0.9, 0.5],
    "big": [0.35, 0.3, 0.15, 0.2, 0.1],
}


class Page_117(SyncLogMixin, Chapter5Scene):
    PAGE_NO = "117"
    RNG_SEED = 1171

    # ---- diagram helpers -------------------------------------------------
    def curve_for(self, axes, fn, color):
        ts = np.linspace(0, 1, 600)
        segs, cur = VGroup(), []
        for t in ts:
            v = float(fn(t))
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

    def weight_bars(self, heights, color, anchor):
        bars = VGroup(*[
            Rectangle(width=0.55, height=max(h, 0.05) * 0.9, color=color,
                      stroke_width=3).set_fill(color, opacity=0.4)
            for h in heights
        ])
        bars.arrange(RIGHT, buff=0.3, aligned_edge=DOWN)
        bars.move_to(anchor, aligned_edge=DOWN)
        return bars

    def err_bars(self, train, gen, anchor):
        a = Rectangle(width=1.2, height=train, color=pal.INPUT,
                      stroke_width=3).set_fill(pal.INPUT, opacity=0.4)
        b = Rectangle(width=1.2, height=gen, color=pal.ERROR,
                      stroke_width=3).set_fill(pal.ERROR, opacity=0.4)
        g = VGroup(a, b).arrange(RIGHT, buff=0.8, aligned_edge=DOWN)
        g.move_to(anchor, aligned_edge=DOWN)
        return g

    def construct(self):
        self.init_page()
        W = config.frame_width

        # ===== Scene 1: preferring one solution ==========================
        head = self.txt("A preference between solutions", color=pal.DISTRIBUTION)
        self._fit(head, W * 0.9)
        head.to_edge(UP, buff=0.9)
        self.type_in(head)

        ax = Axes(x_range=[0, 1, 1], y_range=[0, 1, 1], x_length=4.4,
                  y_length=3.2, tips=False,
                  axis_config={"include_ticks": False, "include_numbers": False,
                               "color": pal.TEXT})
        ax.move_to(UP * 0.4)
        self.play(Create(ax))
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.07, color=pal.INPUT)
                        for x, y in zip(XS, YS)])
        self.play(FadeIn(dots, lag_ratio=0.15))
        wild = self.curve_for(ax, wild_fn, pal.ERROR)
        smooth = self.curve_for(ax, true_fn, pal.OUTPUT)
        self.play(Create(wild), run_time=1.3)
        self.play(Create(smooth), run_time=1.3)
        tag = self.txt("preferred", color=pal.OUTPUT).scale(0.7)
        tag.next_to(ax.c2p(0.42, 0.92), UP, buff=0.15)
        self.type_in(tag)

        c1 = self.txt("Both functions are eligible", color=pal.TEXT)
        c2 = self.txt("The unpreferred one wins only by fitting much better",
                      color=pal.FORMULA)
        caps = VGroup(c1, c2).arrange(DOWN, buff=0.25)
        self._fit(caps, W * 0.9)
        caps.to_edge(DOWN, buff=0.9)
        self.type_in(c1)
        self.type_in(c2)
        self.wait(1)
        self.dust_wipe([head, ax, dots, wild, smooth, tag, caps])

        # ===== Scene 2: weight decay criterion ===========================
        head = self.txt("Weight decay", color=pal.DISTRIBUTION)
        head.to_edge(UP, buff=0.9)
        self.type_in(head)

        f1 = self.formula(r"J(w) =").set_color(pal.FORMULA)
        f2 = self.formula(r"\text{MSE}_{\text{train}}").set_color(pal.INPUT)
        f3 = self.formula(r"+\ \lambda\, w^{\top} w").set_color(pal.ERROR)
        row = VGroup(f1, f2, f3).arrange(RIGHT, buff=0.3)
        self._fit(row, W * 0.9)
        row.move_to(UP * 0.9)
        self.play(Write(f1))
        self.play(Write(f2))
        self.play(Write(f3))
        l2 = self.txt("fit the training data", color=pal.INPUT).scale(0.75)
        l3 = self.txt("prefer small squared L2 norm", color=pal.ERROR).scale(0.75)
        l2.next_to(f2, DOWN, buff=0.7)
        l3.next_to(f3, DOWN, buff=0.7)
        if l2.get_right()[0] > l3.get_left()[0] - 0.2:
            l3.shift(RIGHT * 0.4)
            l2.shift(LEFT * 0.4)
        a2 = Arrow(l2.get_top(), f2.get_bottom(), buff=0.08,
                   color=pal.INPUT, stroke_width=3)
        a3 = Arrow(l3.get_top(), f3.get_bottom(), buff=0.08,
                   color=pal.ERROR, stroke_width=3)
        self.type_in(l2)
        self.play(Create(a2))
        self.type_in(l3)
        self.play(Create(a3))

        c1 = self.txt("λ is chosen ahead of time", color=pal.TEXT)
        c2 = self.txt("It sets the strength of the preference", color=pal.FORMULA)
        caps = VGroup(c1, c2).arrange(DOWN, buff=0.25)
        self._fit(caps, W * 0.9)
        caps.to_edge(DOWN, buff=1.0)
        self.type_in(c1)
        self.type_in(c2)
        self.wait(1)
        self.dust_wipe([head, row, l2, l3, a2, a3, caps])

        # ===== Scene 3: the lambda tradeoff ==============================
        head = self.txt("Larger λ, smaller weights", color=pal.DISTRIBUTION)
        self._fit(head, W * 0.9)
        head.to_edge(UP, buff=0.9)
        self.type_in(head)

        base = Line(LEFT * 2.2, RIGHT * 2.2, color=pal.TEXT, stroke_width=3)
        base.move_to(DOWN * 0.4)
        anchor = base.get_center()
        bars = self.weight_bars(WEIGHTS["none"], pal.OUTPUT, anchor)
        self.play(Create(base))
        self.play(FadeIn(bars, lag_ratio=0.15))
        wl = self.txt("weights w", color=pal.OUTPUT).scale(0.7)
        wl.next_to(base, DOWN, buff=0.2)
        self.type_in(wl)

        sl = Line(LEFT * 2.2, RIGHT * 2.2, color=pal.TEXT, stroke_width=4)
        sl.move_to(DOWN * 2.2)
        lam = self.txt("λ", color=pal.FORMULA)
        lam.next_to(sl.get_left(), LEFT, buff=0.3)
        z = self.txt("0", color=pal.TEXT).scale(0.6).next_to(sl.get_left(), DOWN, buff=0.12)
        bg = self.txt("large", color=pal.TEXT).scale(0.6).next_to(sl.get_right(), DOWN, buff=0.12)
        dot = Dot(sl.get_left(), radius=0.14, color=pal.FORMULA)
        self.play(FadeIn(VGroup(sl, lam, z, bg)), FadeIn(dot))

        note = self.txt("λ = 0: no preference", color=pal.TEXT)
        self._fit(note, W * 0.85)
        note.move_to(UP * 2.3)
        self.type_in(note)

        mid = self.weight_bars(WEIGHTS["mid"], pal.FORMULA, anchor)
        big = self.weight_bars(WEIGHTS["big"], pal.ERROR, anchor)
        self.play(Transform(bars, mid),
                  dot.animate.move_to(sl.point_from_proportion(0.5)),
                  run_time=1.6)
        self.play(Transform(bars, big),
                  dot.animate.move_to(sl.get_right()),
                  run_time=1.6)

        c1 = self.txt("A tradeoff: fit the data vs stay small", color=pal.TEXT)
        c2 = self.txt("Smaller slope, weight on fewer features", color=pal.OUTPUT)
        caps = VGroup(c1, c2).arrange(DOWN, buff=0.25)
        self._fit(caps, W * 0.9)
        caps.to_edge(DOWN, buff=0.9)
        self.type_in(c1)
        self.type_in(c2)
        self.wait(1)
        self.dust_wipe([head, base, bars, wl, sl, lam, z, bg, dot, note, caps])

        # ===== Scene 4: regularizer in general ===========================
        head = self.txt("The regularizer", color=pal.DISTRIBUTION)
        head.to_edge(UP, buff=0.9)
        self.type_in(head)

        g = self.formula(r"J(\theta) = \text{cost}\big(f(x;\theta)\big)"
                         r"\;+\; \lambda\, \Omega(\theta)")
        g.set_color(pal.FORMULA)
        self._fit(g, W * 0.9)
        g.move_to(UP * 1.4)
        self.play(Write(g))
        om = self.formula(r"\text{weight decay: } \Omega(w) = w^{\top} w")
        om.set_color(pal.ERROR)
        self._fit(om, W * 0.85)
        om.next_to(g, DOWN, buff=0.7)
        self.play(Write(om))
        more = self.txt("Chapter 7: many other regularizers", color=pal.TEXT)
        self._fit(more, W * 0.85)
        more.next_to(om, DOWN, buff=0.6)
        self.type_in(more)

        c1 = self.txt("Excluding a function from the hypothesis space", color=pal.TEXT)
        c2 = self.txt("= an infinitely strong preference against it", color=pal.ERROR)
        caps = VGroup(c1, c2).arrange(DOWN, buff=0.25)
        self._fit(caps, W * 0.9)
        caps.to_edge(DOWN, buff=0.9)
        self.type_in(c1)
        self.type_in(c2)
        self.wait(1)
        self.dust_wipe([head, g, om, more, caps])

        # ===== Scene 5: what regularization is ===========================
        head = self.txt("Regularization", color=pal.DISTRIBUTION)
        head.to_edge(UP, buff=0.9)
        self.type_in(head)

        base = Line(LEFT * 2.0, RIGHT * 2.0, color=pal.TEXT, stroke_width=3)
        base.move_to(DOWN * 0.7)
        anchor = base.get_center()
        before = self.err_bars(0.6, 2.4, anchor)
        after = self.err_bars(0.6, 1.3, anchor)
        self.play(Create(base))
        self.play(GrowFromEdge(before[0], DOWN), GrowFromEdge(before[1], DOWN),
                  run_time=1.2)
        tl = self.txt("training", color=pal.INPUT).scale(0.7)
        gl = self.txt("generalization", color=pal.ERROR).scale(0.7)
        tl.next_to(before[0], DOWN, buff=0.2)
        gl.next_to(before[1], DOWN, buff=0.2)
        self.type_in(tl)
        self.type_in(gl)
        self.play(Transform(before, after), run_time=1.6)

        c1 = self.txt("Any change meant to cut generalization error", color=pal.TEXT)
        c2 = self.txt("but not training error", color=pal.OUTPUT)
        caps = VGroup(c1, c2).arrange(DOWN, buff=0.25)
        self._fit(caps, W * 0.9)
        caps.to_edge(DOWN, buff=0.9)
        self.type_in(c1)
        self.type_in(c2)
        self.wait(1)
        self.dust_wipe([head, base, before, tl, gl, caps])

        # ===== Scene 6: no free lunch and regularization =================
        head = self.txt("No best regularizer", color=pal.DISTRIBUTION)
        head.to_edge(UP, buff=0.9)
        self.type_in(head)

        s1 = self.txt("No free lunch theorem", color=pal.ERROR)
        s2 = self.txt("No best learning algorithm", color=pal.TEXT)
        s3 = self.txt("No best form of regularization", color=pal.FORMULA)
        s4 = self.txt("Choose one suited to the task", color=pal.OUTPUT)
        arrs = [Arrow(UP * 0.25, DOWN * 0.25, buff=0, color=pal.TEXT,
                      stroke_width=4) for _ in range(3)]
        flow = VGroup(s1, arrs[0], s2, arrs[1], s3, arrs[2], s4)
        flow.arrange(DOWN, buff=0.28)
        self._fit(flow, W * 0.88)
        flow.move_to(DOWN * 0.1)
        for i, item in enumerate((s1, s2, s3, s4)):
            self.type_in(item)
            if i < 3:
                self.play(Create(arrs[i]))
        box = SurroundingRectangle(s4, color=pal.OUTPUT, buff=0.2)
        self.play(Create(box))
        self.wait(1)
        self.dust_wipe([head, flow, box])

        # ===== Scene 7: takeaway =========================================
        t1 = self.txt("Regularization expresses preferences", color=pal.TEXT)
        t2 = self.txt("to cut generalization error", color=pal.TEXT)
        take = VGroup(t1, t2).arrange(DOWN, buff=0.3)
        self._fit(take, W * 0.9)
        take.move_to(ORIGIN)
        self.type_in(t1)
        self.type_in(t2)
        underline = Line(take.get_corner(DL) + DOWN * 0.2,
                         take.get_corner(DR) + DOWN * 0.2,
                         color=pal.OUTPUT, stroke_width=5)
        self.play(Create(underline))
        self.zoom_pulse(VGroup(take, underline))
        self.wait(1)
