"""Page 116 - No free lunch (cont.), 5.2.2 Regularization, hypothesis space."""
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


class Page_116(SyncLogMixin, Chapter5Scene):
    PAGE_NO = "116"
    RNG_SEED = 1161

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

    def construct(self):
        self.init_page()
        W = config.frame_width

        # ===== Scene 1: no free lunch, continued =========================
        head = self.txt("No free lunch, continued", color=pal.DISTRIBUTION)
        self._fit(head, W * 0.9)
        head.to_edge(UP, buff=0.9)
        self.type_in(head)

        names = ["Fancy", "Other", "Constant"]
        bars = VGroup(*[
            Rectangle(width=1.4, height=2.2, color=pal.INPUT,
                      stroke_width=4).set_fill(pal.INPUT, opacity=0.3)
            for _ in names
        ])
        bars.arrange(RIGHT, buff=0.5, aligned_edge=DOWN).move_to(UP * 0.4)
        labels = VGroup()
        for r, nm in zip(bars, names):
            t = self.txt(nm, color=pal.TEXT)
            self._fit(t, 1.4)
            t.next_to(r, DOWN, buff=0.2)
            labels.add(t)
        self.play(LaggedStart(*[GrowFromEdge(r, DOWN) for r in bars],
                              lag_ratio=0.3), run_time=1.6)
        self.play(FadeIn(labels))
        avg = DashedLine(bars.get_corner(UL) + LEFT * 0.35,
                         bars.get_corner(UR) + RIGHT * 0.35,
                         color=pal.FORMULA, stroke_width=4)
        self.play(Create(avg))
        c1 = self.txt("Averaged over all possible tasks", color=pal.TEXT)
        c2 = self.txt("every algorithm has the same error", color=pal.FORMULA)
        caps = VGroup(c1, c2).arrange(DOWN, buff=0.3)
        self._fit(caps, W * 0.88)
        caps.to_edge(DOWN, buff=1.2)
        self.type_in(c1)
        self.type_in(c2)
        self.wait(1)
        self.dust_wipe([head, bars, labels, avg, caps])

        # ===== Scene 2: only over ALL distributions ======================
        head = self.txt("Fortunately...", color=pal.DISTRIBUTION)
        head.to_edge(UP, buff=0.9)
        self.type_in(head)

        big = Circle(radius=2.0, color=pal.DISTRIBUTION, stroke_width=5)
        big.move_to(UP * 0.2)
        small = Circle(radius=0.8, color=pal.OUTPUT, stroke_width=5)
        small.set_fill(pal.OUTPUT, opacity=0.3)
        small.move_to(big.get_center() + UP * 0.45)
        self.play(Create(big), run_time=1.4)
        self.play(Create(small), run_time=1.3)
        bl = self.txt("All possible distributions", color=pal.DISTRIBUTION)
        self._fit(bl, 3.2)
        bl.move_to(big.get_center() + DOWN * 1.15)
        sl = self.txt("Real world", color=pal.OUTPUT)
        self._fit(sl, 1.3)
        sl.move_to(small)
        self.type_in(bl)
        self.type_in(sl)
        c1 = self.txt("Assume what real data looks like,", color=pal.TEXT)
        c2 = self.txt("then design algorithms that do well", color=pal.OUTPUT)
        caps = VGroup(c1, c2).arrange(DOWN, buff=0.3)
        self._fit(caps, W * 0.88)
        caps.to_edge(DOWN, buff=1.2)
        self.type_in(c1)
        self.type_in(c2)
        self.wait(1)
        self.dust_wipe([head, big, small, bl, sl, caps])

        # ===== Scene 3: the goal of ML research ==========================
        head = self.txt("The goal of the field", color=pal.DISTRIBUTION)
        head.to_edge(UP, buff=0.9)
        self.type_in(head)

        uni = self.txt("A universal learning algorithm", color=pal.ERROR)
        self._fit(uni, W * 0.85)
        uni.move_to(UP * 1.7)
        self.type_in(uni)
        cross = Cross(uni, stroke_color=pal.ERROR, stroke_width=6)
        self.play(Create(cross))
        inst = self.txt("Instead, understand:", color=pal.TEXT)
        inst.move_to(UP * 0.6)
        self.type_in(inst)
        b1 = self.txt("which distributions the real world gives", color=pal.INPUT)
        b2 = self.txt("which algorithms do well on them", color=pal.OUTPUT)
        arr = Arrow(UP * 0.3, DOWN * 0.3, buff=0, color=pal.TEXT,
                    stroke_width=4)
        flow = VGroup(b1, arr, b2).arrange(DOWN, buff=0.3)
        self._fit(flow, W * 0.88)
        flow.move_to(DOWN * 1.2)
        self.type_in(b1)
        self.play(Create(arr))
        self.type_in(b2)
        self.wait(1)
        self.dust_wipe([head, uni, cross, inst, flow])

        # ===== Scene 4: 5.2.2 Regularization =============================
        head = self.txt("5.2.2 Regularization", color=pal.DISTRIBUTION)
        self._fit(head, W * 0.9)
        head.to_edge(UP, buff=0.9)
        self.type_in(head)

        s1 = self.txt("No free lunch theorem", color=pal.ERROR)
        s2 = self.txt("Build preferences into the algorithm", color=pal.FORMULA)
        s3 = self.txt("Aligned with the task = performs better", color=pal.OUTPUT)
        a1 = Arrow(UP * 0.3, DOWN * 0.3, buff=0, color=pal.TEXT, stroke_width=4)
        a2 = Arrow(UP * 0.3, DOWN * 0.3, buff=0, color=pal.TEXT, stroke_width=4)
        flow = VGroup(s1, a1, s2, a2, s3).arrange(DOWN, buff=0.35)
        self._fit(flow, W * 0.88)
        flow.move_to(DOWN * 0.1)
        self.type_in(s1)
        self.play(Create(a1))
        self.type_in(s2)
        self.play(Create(a2))
        self.type_in(s3)
        box = SurroundingRectangle(s2, color=pal.FORMULA, buff=0.2)
        self.play(Create(box))
        self.wait(1)
        self.dust_wipe([head, flow, box])

        # ===== Scene 5: hypothesis space =================================
        head = self.txt("Choosing the hypothesis space", color=pal.DISTRIBUTION)
        self._fit(head, W * 0.9)
        head.to_edge(UP, buff=0.9)
        self.type_in(head)

        ax = Axes(x_range=[0, 2 * PI, PI], y_range=[-1.5, 1.5, 1],
                  x_length=5.6, y_length=3.0, tips=False,
                  axis_config={"include_ticks": False, "include_numbers": False,
                               "color": pal.TEXT})
        ax.move_to(UP * 0.3)
        self.play(Create(ax))
        sn = ax.plot(lambda x: float(np.sin(x)), x_range=[0, 2 * PI],
                     color=pal.OUTPUT, stroke_width=5)
        self.play(Create(sn), run_time=1.5)
        gx = np.linspace(0, 2 * PI, 60)
        coef = np.polyfit(gx, np.sin(gx), 1)
        ln = ax.plot(lambda x: float(coef[0] * x + coef[1]),
                     x_range=[0, 2 * PI], color=pal.ERROR, stroke_width=5)
        self.play(Create(ln), run_time=1.3)
        c1 = self.txt("Linear regression: only linear functions", color=pal.INPUT)
        c2 = self.txt("It cannot predict sin(x) from x", color=pal.ERROR)
        caps = VGroup(c1, c2).arrange(DOWN, buff=0.3)
        self._fit(caps, W * 0.9)
        caps.to_edge(DOWN, buff=1.0)
        self.type_in(c1)
        self.type_in(c2)
        self.wait(1)
        self.dust_wipe([head, ax, sn, ln, caps])

        # ===== Scene 6: a preference between solutions ===================
        head = self.txt("Preferring one solution", color=pal.DISTRIBUTION)
        head.to_edge(UP, buff=0.9)
        self.type_in(head)

        ax = Axes(x_range=[0, 1, 1], y_range=[0, 1, 1], x_length=4.4,
                  y_length=3.4, tips=False,
                  axis_config={"include_ticks": False, "include_numbers": False,
                               "color": pal.TEXT})
        ax.move_to(UP * 0.3)
        self.play(Create(ax))
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.07, color=pal.INPUT)
                        for x, y in zip(XS, YS)])
        self.play(FadeIn(dots, lag_ratio=0.15))
        smooth = self.curve_for(ax, true_fn, pal.OUTPUT)
        wild = self.curve_for(ax, wild_fn, pal.ERROR)
        self.play(Create(wild), run_time=1.4)
        self.play(Create(smooth), run_time=1.4)
        self.play(wild.animate.set_opacity(0.3))
        c1 = self.txt("Many solutions fit the same data", color=pal.TEXT)
        c2 = self.txt("Give the algorithm a preference", color=pal.FORMULA)
        caps = VGroup(c1, c2).arrange(DOWN, buff=0.3)
        self._fit(caps, W * 0.88)
        caps.to_edge(DOWN, buff=1.1)
        self.type_in(c1)
        self.type_in(c2)
        self.wait(1)
        self.dust_wipe([head, ax, dots, smooth, wild, caps])

        # ===== Scene 7: takeaway =========================================
        t1 = self.txt("No universal best algorithm:", color=pal.TEXT)
        t2 = self.txt("build in the right preferences", color=pal.TEXT)
        take = VGroup(t1, t2).arrange(DOWN, buff=0.3)
        self._fit(take, W * 0.88)
        take.move_to(ORIGIN)
        self.type_in(t1)
        self.type_in(t2)
        underline = Line(take.get_corner(DL) + DOWN * 0.2,
                         take.get_corner(DR) + DOWN * 0.2,
                         color=pal.OUTPUT, stroke_width=5)
        self.play(Create(underline))
        self.zoom_pulse(VGroup(take, underline))
        self.wait(1)
