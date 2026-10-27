import numpy as np
from manim import *

from common import palette as pal
from common.chapter5_style import Chapter5Scene


class Page_110(Chapter5Scene):
    PAGE_NO = "110"
    RNG_SEED = 1100

    # ---- layout helper: fit a whole scene inside the 1:1 frame ----
    def _fit(self, group):
        max_w = config.frame_width * 0.82
        max_h = config.frame_height * 0.74
        if group.width > max_w:
            group.scale_to_fit_width(max_w)
        if group.height > max_h:
            group.scale_to_fit_height(max_h)
        group.move_to([0, config.frame_height * 0.03, 0])
        return group

    def _card(self, line1, line2, color):
        a = self.txt(line1, color=pal.TEXT)
        b = self.txt(line2, color=color)
        inner = VGroup(a, b).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        box = RoundedRectangle(corner_radius=0.2, width=inner.width + 0.8,
                               height=inner.height + 0.6, color=color)
        inner.move_to(box)
        return VGroup(box, inner)

    def _fit_panel(self, degree, label, color):
        """Mini plot: noisy points + polynomial fit of the given degree."""
        xs = np.linspace(-1, 1, 10)
        noise = np.array([0.12, -0.10, 0.08, -0.12, 0.10, -0.08, 0.12, -0.10, 0.09, -0.11])
        ys = 1.2 * xs ** 2 - 0.3 + noise
        coef = np.polyfit(xs, ys, degree)

        axes = Axes(x_range=[-1.2, 1.2, 1], y_range=[-0.6, 1.2, 1],
                    x_length=3.0, y_length=2.6, tips=False,
                    axis_config={"color": pal.TEXT, "stroke_width": 2,
                                 "include_ticks": False})
        dots = VGroup(*[Dot(axes.c2p(x, y), radius=0.06, color=pal.INPUT)
                        for x, y in zip(xs, ys)])
        curve = axes.plot(lambda x: float(np.clip(np.polyval(coef, x), -0.6, 1.2)),
                          x_range=[-1.1, 1.1, 0.01], color=color, stroke_width=4)
        lbl = self.txt(label, color=color).scale(0.8).next_to(axes, DOWN, buff=0.25)
        return VGroup(axes, dots, curve, lbl), dots, curve

    def construct(self):
        self.init_page()

        # ---------- Scene 1: capacity ----------
        s1_title = self.txt("Control the risk with\nmodel capacity", color=pal.TEXT)
        s1_def = self.txt("Capacity: ability to fit\na wide variety of functions", color=pal.FORMULA)
        low = self._card("Low capacity", "struggles to fit training set  ->  underfit", pal.ERROR)
        high = self._card("High capacity", "memorizes the training set  ->  overfit", pal.DISTRIBUTION)
        cards = VGroup(low, high).arrange(DOWN, buff=0.5)
        s1 = VGroup(s1_title, s1_def, cards).arrange(DOWN, buff=0.7)
        self._fit(s1)

        self.type_in(s1_title)
        self.type_in(s1_def)
        self.play(FadeIn(low, shift=RIGHT * 0.3))
        self.play(FadeIn(high, shift=RIGHT * 0.3))
        self.wait(1.0)
        self.dust_wipe([s1_title, s1_def, low, high])

        # ---------- Scene 2: hypothesis space ----------
        s2_title = self.txt("Hypothesis space:\nfunctions the algorithm may pick", color=pal.TEXT)
        e1 = Ellipse(width=3.0, height=1.6, color=pal.INPUT, fill_color=pal.INPUT, fill_opacity=0.25)
        e2 = Ellipse(width=4.8, height=3.0, color=pal.OUTPUT, fill_color=pal.OUTPUT, fill_opacity=0.15)
        e3 = Ellipse(width=6.6, height=4.4, color=pal.DISTRIBUTION,
                     fill_color=pal.DISTRIBUTION, fill_opacity=0.10)
        for e in (e1, e2, e3):
            e.move_to(ORIGIN)
        l1 = self.txt("linear", color=pal.INPUT).scale(0.7).move_to(e1)
        l2 = self.txt("+ quadratic", color=pal.OUTPUT).scale(0.7).move_to(e2.get_top() + DOWN * 0.35)
        l3 = self.txt("+ ... degree 9", color=pal.DISTRIBUTION).scale(0.7).move_to(e3.get_top() + DOWN * 0.35)
        rings = VGroup(e3, e2, e1, l1, l2, l3)
        s2_note = self.txt("Bigger space = more capacity", color=pal.FORMULA)
        s2 = VGroup(s2_title, rings, s2_note).arrange(DOWN, buff=0.6)
        self._fit(s2)

        self.type_in(s2_title)
        self.play(FadeIn(e1), FadeIn(l1))
        self.play(FadeIn(e2), FadeIn(l2))
        self.play(FadeIn(e3), FadeIn(l3))
        self.type_in(s2_note)
        self.wait(1.0)
        self.dust_wipe([s2_title, e1, e2, e3, l1, l2, l3, s2_note])

        # ---------- Scene 3: degree 1 -> degree 2 ----------
        s3_title = self.txt("Add features, add capacity", color=pal.TEXT)
        f1 = self.formula(r"\hat{y} = b + w x", color=pal.FORMULA)
        f1_tag = self.txt("degree 1: linear regression", color=pal.INPUT).scale(0.75)
        f2 = self.formula(r"\hat{y} = b + w_1 x + w_2 x^2", color=pal.FORMULA)
        f2_tag = self.txt("degree 2: new feature x^2", color=pal.OUTPUT).scale(0.75)
        note = self.txt("Quadratic in x, but still linear\nin the parameters: normal equations work",
                        color=pal.TEXT).scale(0.8)
        row1 = VGroup(f1, f1_tag).arrange(DOWN, buff=0.25)
        row2 = VGroup(f2, f2_tag).arrange(DOWN, buff=0.25)
        s3 = VGroup(s3_title, row1, row2, note).arrange(DOWN, buff=0.7)
        self._fit(s3)

        self.type_in(s3_title)
        self.play(Write(f1), FadeIn(f1_tag))
        self.play(Write(f2), FadeIn(f2_tag))
        self.type_in(note)
        self.wait(1.0)
        self.dust_wipe([s3_title, f1, f1_tag, f2, f2_tag, note])

        # ---------- Scene 4: degree 9 ----------
        s4_title = self.txt("Keep adding powers of x", color=pal.TEXT)
        f9 = self.formula(r"\hat{y} = b + \sum_{i=1}^{9} w_i x^i", color=pal.FORMULA)
        s4_tag = self.txt("degree 9: 10 parameters\nto bend the curve", color=pal.DISTRIBUTION)
        s4 = VGroup(s4_title, f9, s4_tag).arrange(DOWN, buff=0.8)
        self._fit(s4)

        self.type_in(s4_title)
        self.play(Write(f9))
        self.type_in(s4_tag)
        self.wait(1.0)
        self.dust_wipe([s4_title, f9, s4_tag])

        # ---------- Scene 5: Figure 5.2 idea ----------
        s5_title = self.txt("Match capacity to\nthe true task", color=pal.TEXT)
        p1, d1, c1 = self._fit_panel(1, "linear: underfit", pal.ERROR)
        p2, d2, c2 = self._fit_panel(2, "quadratic: just right", pal.OUTPUT)
        p3, d3, c3 = self._fit_panel(9, "degree 9: overfit", pal.DISTRIBUTION)
        panels = VGroup(p1, p2, p3).arrange(RIGHT, buff=0.5)
        s5 = VGroup(s5_title, panels).arrange(DOWN, buff=0.7)
        self._fit(s5)

        self.type_in(s5_title)
        self.play(FadeIn(p1[0]), FadeIn(p2[0]), FadeIn(p3[0]),
                  FadeIn(d1), FadeIn(d2), FadeIn(d3))
        self.play(Create(c1), Create(c2), Create(c3))
        self.play(FadeIn(p1[3]), FadeIn(p2[3]), FadeIn(p3[3]))
        self.wait(1.5)
        self.dust_wipe([s5_title, p1, p2, p3])

        # ---------- Scene 6: takeaway ----------
        take = self.txt("Right capacity for\nthe task and the data.", color=pal.OUTPUT)
        underline = Line(take.get_corner(DL) + DOWN * 0.2,
                         take.get_corner(DR) + DOWN * 0.2, color=pal.OUTPUT)
        s6 = VGroup(take, underline)
        self._fit(s6)

        self.type_in(take)
        self.play(Create(underline))
        self.zoom_pulse(s6)
        self.wait(1.0)
