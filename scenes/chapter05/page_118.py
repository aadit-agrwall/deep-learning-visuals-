"""Page 118 - 5.3 Hyperparameters and Validation Sets, Figure 5.5 (weight decay)."""
import numpy as np
from manim import *

import common.palette as pal
from common.chapter5_style import Chapter5Scene
from common.sync_log import SyncLogMixin


XS = np.array([0.00, 0.36, 0.45, 0.86, 0.89, 0.93])


def true_fn(x):
    return 0.92 - 2.6 * (x - 0.42) ** 2


YS = true_fn(XS)
V9 = np.vander(XS, 10, increasing=True)


def ridge_fn(lam):
    """Degree-9 fit with weight decay lam on every coefficient except the bias."""
    S = np.eye(10)
    S[0, 0] = 0.0
    A = np.vstack([V9, np.sqrt(lam) * S])
    b = np.concatenate([YS, np.zeros(10)])
    w = np.linalg.lstsq(A, b, rcond=None)[0]
    return lambda x: float(np.polynomial.polynomial.polyval(x, w))


def pinv_fn():
    """lambda -> 0: Moore-Penrose pseudoinverse (as in Figure 5.2)."""
    w = np.linalg.pinv(V9) @ YS
    return lambda x: float(np.polynomial.polynomial.polyval(x, w))


def best_lambda():
    """The lambda whose fit best recovers the true quadratic shape."""
    grid = np.linspace(0, 1, 200)
    best = None
    for lam in 10 ** np.linspace(-6, 1, 40):
        f = ridge_fn(lam)
        err = float(np.mean([(f(x) - true_fn(x)) ** 2 for x in grid]))
        if best is None or err < best[0]:
            best = (err, lam)
    return best[1]


class Page_118(SyncLogMixin, Chapter5Scene):
    PAGE_NO = "118"
    RNG_SEED = 1181

    # ---- diagram helpers (text helpers are inherited) -----------------
    def _panel(self, width=4.0, height=3.4):
        axes = Axes(x_range=[0, 1, 1], y_range=[0, 1, 1], x_length=width,
                    y_length=height, tips=False,
                    axis_config={"include_ticks": False,
                                 "include_numbers": False,
                                 "color": pal.TEXT})
        frame = SurroundingRectangle(axes, buff=0, color=pal.TEXT,
                                     stroke_width=3)
        dots = VGroup(*[Dot(axes.c2p(x, y), radius=0.07, color=pal.INPUT)
                        for x, y in zip(XS, YS)])
        return axes, frame, dots

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

    def _slider(self, frac):
        line = Line(LEFT * 2.2, RIGHT * 2.2, color=pal.TEXT, stroke_width=4)
        lo = self.txt("small", color=pal.TEXT).scale(0.6)
        lo.next_to(line.get_left(), DOWN, buff=0.15)
        hi = self.txt("large", color=pal.TEXT).scale(0.6)
        hi.next_to(line.get_right(), DOWN, buff=0.15)
        lam = self.txt("λ", color=pal.FORMULA)
        lam.next_to(line.get_left(), LEFT, buff=0.3)
        dot = Dot(line.point_from_proportion(frac), radius=0.14,
                  color=pal.FORMULA)
        return VGroup(line, lo, hi, lam), dot

    def _knob(self):
        c = Circle(radius=0.3, color=pal.FORMULA, stroke_width=4)
        t = Line(c.get_center(), c.get_center() + UP * 0.3,
                 color=pal.FORMULA, stroke_width=4)
        return VGroup(c, t)

    def _panel_scene(self, title, color, fn, start, end, cap1, cap2):
        W = config.frame_width
        head = self.txt(title, color=color)
        self._fit(head, W * 0.9)
        head.to_edge(UP, buff=0.9)
        self.type_in(head)

        axes, frame, dots = self._panel()
        panel = VGroup(axes, frame, dots).move_to(UP * 0.6)
        self.play(Create(axes), Create(frame), FadeIn(dots))
        curve = self.curve_for(axes, fn, color)
        self.play(Create(curve), run_time=1.4)

        sl, dot = self._slider(start)
        both = VGroup(sl, dot).move_to(DOWN * 1.75)
        self.play(FadeIn(sl), FadeIn(dot))
        self.play(dot.animate.move_to(sl[0].point_from_proportion(end)),
                  run_time=1.0)

        caps = VGroup(self.txt(cap1, color=color),
                      self.txt(cap2, color=pal.TEXT)).arrange(DOWN, buff=0.25)
        self._fit(caps, W * 0.9)
        caps.to_edge(DOWN, buff=0.9)
        self.type_in(caps[0])
        self.type_in(caps[1])
        self.wait(1)
        self.dust_wipe([head, panel, curve, sl, dot, caps])

    # ---- scenes -----------------------------------------------------------
    def construct(self):
        self.init_page()
        W = config.frame_width

        # ===== Scene 1: hyperparameters ==================================
        head = self.txt("5.3 Hyperparameters", color=pal.DISTRIBUTION)
        self._fit(head, W * 0.9)
        head.to_edge(UP, buff=0.9)
        self.type_in(head)

        hp = self.txt("Hyperparameters: set by us", color=pal.FORMULA)
        hp.scale(0.8)
        k1, k2 = self._knob(), self._knob()
        knobs = VGroup(k1, k2).arrange(RIGHT, buff=1.4)
        box = RoundedRectangle(width=4.6, height=2.0, corner_radius=0.25,
                               color=pal.INPUT)
        bl = self.txt("Learning algorithm", color=pal.INPUT)
        five = VGroup(*[Dot(radius=0.12, color=pal.OUTPUT) for _ in range(5)])
        five.arrange(RIGHT, buff=0.35)
        wl = self.txt("Parameters: learned", color=pal.OUTPUT).scale(0.8)
        inner = VGroup(bl, five, wl).arrange(DOWN, buff=0.22)
        self._fit(inner, 4.0)
        stack = VGroup(hp, knobs, box).arrange(DOWN, buff=0.5)
        stack.move_to(UP * 0.3)
        inner.move_to(box)
        arrows = VGroup(*[
            Arrow(k.get_bottom(), [k.get_center()[0], box.get_top()[1], 0],
                  buff=0.08, color=pal.FORMULA, stroke_width=4)
            for k in (k1, k2)
        ])

        self.play(Create(box))
        self.type_in(bl)
        self.play(FadeIn(five, lag_ratio=0.2))
        self.type_in(wl)
        self.play(FadeIn(knobs))
        self.type_in(hp)
        self.play(Create(arrows))
        self.play(Rotate(k1[1], angle=PI / 2, about_point=k1[0].get_center()),
                  Rotate(k2[1], angle=-PI / 3, about_point=k2[0].get_center()),
                  run_time=1.2)

        c1 = self.txt("Not adapted by the algorithm itself", color=pal.TEXT)
        c2 = self.txt("(a nested procedure could learn them)", color=pal.FORMULA)
        caps = VGroup(c1, c2).arrange(DOWN, buff=0.25)
        self._fit(caps, W * 0.9)
        caps.to_edge(DOWN, buff=0.9)
        self.type_in(c1)
        self.type_in(c2)
        self.wait(1)
        self.dust_wipe([head, hp, knobs, box, inner, arrows, caps])

        # ===== Scene 2: two examples =====================================
        head = self.txt("Two examples", color=pal.DISTRIBUTION)
        head.to_edge(UP, buff=0.9)
        self.type_in(head)

        r1 = RoundedRectangle(width=3.4, height=3.2, corner_radius=0.2,
                              color=pal.INPUT)
        t1 = self.txt("Degree", color=pal.INPUT)
        s1 = self.txt("capacity hyperparameter", color=pal.TEXT).scale(0.7)
        f1 = self.formula(r"d \in \{1, \dots, 9\}").set_color(pal.FORMULA)
        g1 = VGroup(t1, s1, f1).arrange(DOWN, buff=0.35)
        self._fit(g1, 3.0)
        r2 = RoundedRectangle(width=3.4, height=3.2, corner_radius=0.2,
                              color=pal.OUTPUT)
        t2 = self.txt("λ", color=pal.OUTPUT)
        s2 = self.txt("weight decay strength", color=pal.TEXT).scale(0.7)
        f2 = self.formula(r"\lambda\, w^{\top} w").set_color(pal.FORMULA)
        g2 = VGroup(t2, s2, f2).arrange(DOWN, buff=0.35)
        self._fit(g2, 3.0)
        cards = VGroup(r1, r2).arrange(RIGHT, buff=0.4).move_to(UP * 0.3)
        self._fit(cards, W * 0.9)
        g1.move_to(r1)
        g2.move_to(r2)

        self.play(Create(r1), Create(r2))
        self.type_in(t1)
        self.type_in(s1)
        self.play(Write(f1))
        self.type_in(t2)
        self.type_in(s2)
        self.play(Write(f2))
        c1 = self.txt("Both control how complex the fit can be", color=pal.TEXT)
        self._fit(c1, W * 0.9)
        c1.to_edge(DOWN, buff=1.2)
        self.type_in(c1)
        self.wait(1)
        self.dust_wipe([head, cards, g1, g2, c1])

        # ===== Scenes 3-5: Figure 5.5 ====================================
        self._panel_scene("Excessive λ", pal.ERROR, ridge_fn(1e4), 0.5, 1.0,
                          "No slope at all: a constant function",
                          "Underfits")
        self._panel_scene("Medium λ", pal.OUTPUT, ridge_fn(best_lambda()),
                          1.0, 0.5,
                          "Smaller coefficients, simpler function",
                          "Recovers the right general shape")
        self._panel_scene("λ → 0", pal.ERROR, pinv_fn(), 0.5, 0.0,
                          "Pseudoinverse, minimal regularization",
                          "Degree 9 overfits")

        # ===== Scene 6: takeaway =========================================
        t1 = self.txt("Weight decay λ is a hyperparameter:", color=pal.TEXT)
        t2 = self.txt("too large underfits, too small overfits", color=pal.TEXT)
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
