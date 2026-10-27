"""Page 113 - Figure 5.3 (U-shaped generalization curve), parametric vs
nonparametric models, nearest neighbor regression."""
import numpy as np
from manim import *

import common.palette as pal
from common.chapter5_style import Chapter5Scene


def train_err(x):
    return 0.10 + 0.80 * np.exp(-7 * x)


def gen_err(x):
    return 0.22 + 0.75 * np.exp(-9 * x) + 0.9 * max(0.0, x - 0.35) ** 2


class Page_113(Chapter5Scene):
    PAGE_NO = "113"
    RNG_SEED = 1131

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
        with open("assets/audio/raw/page_113_events.json", "w") as f:
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

        # ===== Scene 1: the two error curves =============================
        head = self.txt("Capacity vs error", color=pal.DISTRIBUTION)
        head.to_edge(UP, buff=0.9)
        self.type_in(head)

        axes = Axes(x_range=[0, 1, 1], y_range=[0, 1, 1],
                    x_length=5.6, y_length=4.0, tips=False,
                    axis_config={"include_ticks": False,
                                 "include_numbers": False,
                                 "color": pal.TEXT})
        axes.move_to(DOWN * 0.1)
        xl = self.txt("capacity", color=pal.TEXT)
        xl.scale(0.8).next_to(axes, DOWN, buff=0.25)
        yl = self.txt("error", color=pal.TEXT)
        yl.scale(0.8).rotate(PI / 2).next_to(axes, LEFT, buff=0.25)
        self.play(Create(axes), FadeIn(xl), FadeIn(yl))

        tr = axes.plot(lambda x: train_err(x), x_range=[0.01, 1],
                       color=pal.INPUT, stroke_width=5)
        ge = axes.plot(lambda x: gen_err(x), x_range=[0.01, 1],
                       color=pal.OUTPUT, stroke_width=5)
        self.play(Create(tr), run_time=1.4)
        self.play(Create(ge), run_time=1.4)

        k1 = self.txt("Training error", color=pal.INPUT)
        k2 = self.txt("Generalization error", color=pal.OUTPUT)
        key = VGroup(k1, k2).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        self.fit_width(key, W * 0.55)
        key.to_edge(DOWN, buff=1.1)
        self.type_in(k1)
        self.type_in(k2)
        self.wait(1)

        # ===== Scene 1b: zones, optimal capacity, gap (same axes) ========
        opt = DashedLine(axes.c2p(0.35, 0), axes.c2p(0.35, 1), color=pal.ERROR,
                         stroke_width=4)
        self.play(Create(opt))
        zl = self.txt("Underfitting", color=pal.ERROR)
        zr = self.txt("Overfitting", color=pal.ERROR)
        zl.scale(0.7).move_to(axes.c2p(0.17, 0.9))
        zr.scale(0.7).move_to(axes.c2p(0.68, 0.9))
        self.type_in(zl)
        self.type_in(zr)

        gap = DoubleArrow(axes.c2p(0.85, train_err(0.85)),
                          axes.c2p(0.85, gen_err(0.85)),
                          buff=0, color=pal.FORMULA, stroke_width=4,
                          tip_length=0.18)
        gl = self.txt("Gap", color=pal.FORMULA)
        gl.scale(0.7).next_to(gap, LEFT, buff=0.15)
        self.play(Create(gap))
        self.type_in(gl)
        self.wait(1)
        self.dust_wipe([head, axes, xl, yl, tr, ge, key, opt, zl, zr, gap, gl])

        # ===== Scene 2: U-shape takeaway =================================
        head = self.txt("The U-shaped curve", color=pal.DISTRIBUTION)
        head.to_edge(UP, buff=0.9)
        self.type_in(head)
        a = self.txt("Training error keeps falling", color=pal.INPUT)
        b = self.txt("The gap keeps growing", color=pal.FORMULA)
        c = self.txt("Generalization error turns up", color=pal.OUTPUT)
        st = VGroup(a, b, c).arrange(DOWN, buff=0.7)
        self.fit_width(st, W * 0.85)
        st.move_to(ORIGIN)
        for ln in st:
            self.type_in(ln)
            self.wait(0.3)
        box = SurroundingRectangle(c, color=pal.OUTPUT, buff=0.25)
        self.play(Create(box))
        self.wait(1)
        self.dust_wipe([head, st, box])

        # ===== Scene 3: parametric vs nonparametric ======================
        head = self.txt("Nonparametric models", color=pal.DISTRIBUTION)
        self.fit_width(head, W * 0.9)
        head.to_edge(UP, buff=0.9)
        self.type_in(head)

        par = VGroup(RoundedRectangle(width=3.6, height=2.6, corner_radius=0.2,
                                      color=pal.INPUT))
        pt = self.txt("Parametric", color=pal.INPUT)
        pd = self.txt("fixed-size vector", color=pal.TEXT)
        pd.scale(0.8)
        VGroup(pt, pd).arrange(DOWN, buff=0.25).move_to(par[0])
        non = VGroup(RoundedRectangle(width=3.6, height=2.6, corner_radius=0.2,
                                      color=pal.OUTPUT))
        nt = self.txt("Nonparametric", color=pal.OUTPUT)
        nd = self.txt("no such limit", color=pal.TEXT)
        nd.scale(0.8)
        VGroup(nt, nd).arrange(DOWN, buff=0.25).move_to(non[0])
        grp = VGroup(par, non).arrange(RIGHT, buff=0.5).move_to(UP * 0.3)
        # re-center labels after arrange
        VGroup(pt, pd).arrange(DOWN, buff=0.25).move_to(par[0])
        VGroup(nt, nd).arrange(DOWN, buff=0.25).move_to(non[0])
        self.play(Create(par[0]), Create(non[0]))
        self.type_in(pt)
        self.type_in(pd)
        self.type_in(nt)
        self.type_in(nd)

        cap = self.txt("Complexity can grow with the training set",
                       color=pal.TEXT)
        self.fit_width(cap, W * 0.88)
        cap.to_edge(DOWN, buff=1.3)
        self.type_in(cap)
        self.wait(1)
        self.dust_wipe([head, grp, pt, pd, nt, nd, cap])

        # ===== Scene 4: nearest neighbor regression ======================
        head = self.txt("Nearest neighbor regression", color=pal.DISTRIBUTION)
        self.fit_width(head, W * 0.9)
        head.to_edge(UP, buff=0.9)
        self.type_in(head)

        rng = np.random.default_rng(113)
        pts = rng.uniform([-2.6, -1.4], [2.6, 1.4], size=(9, 2))
        q = np.array([0.4, 0.2])
        dots = VGroup(*[Dot([p[0], p[1] - 0.2, 0], radius=0.11, color=pal.INPUT)
                        for p in pts])
        self.play(FadeIn(dots, lag_ratio=0.1))
        stored = self.txt("Stores X and y", color=pal.INPUT)
        stored.scale(0.9).next_to(dots, UP, buff=0.35)
        self.type_in(stored)

        qd = Dot([q[0], q[1] - 0.2, 0], radius=0.15, color=pal.FORMULA)
        self.play(FadeIn(qd, scale=0.4))
        d = np.linalg.norm(pts - q, axis=1)
        j = int(np.argmin(d))
        near = dots[j]
        link = Line(qd.get_center(), near.get_center(), color=pal.OUTPUT,
                    stroke_width=5)
        ring = Circle(radius=0.25, color=pal.OUTPUT).move_to(near)
        self.play(Create(link), Create(ring))

        fm = self.formula(
            r"\hat{y} = y_i,\quad i=\arg\min_i \|X_{i,:}-x\|_2^2")
        fm.set_color(pal.FORMULA)
        self.fit_width(fm, W * 0.9)
        fm.to_edge(DOWN, buff=1.3)
        self.play(Write(fm))
        self.wait(1)
        self.dust_wipe([head, dots, stored, qd, link, ring, fm])

        # ===== Scene 5: ties and minimum training error ==================
        head = self.txt("Ties and training error", color=pal.DISTRIBUTION)
        self.fit_width(head, W * 0.9)
        head.to_edge(UP, buff=0.9)
        self.type_in(head)

        tq = Dot(ORIGIN + DOWN * 0.2, radius=0.15, color=pal.FORMULA)
        t1 = Dot(LEFT * 1.6 + DOWN * 0.2, radius=0.11, color=pal.INPUT)
        t2 = Dot(RIGHT * 1.6 + DOWN * 0.2, radius=0.11, color=pal.INPUT)
        l1 = Line(tq.get_center(), t1.get_center(), color=pal.OUTPUT,
                  stroke_width=5)
        l2 = Line(tq.get_center(), t2.get_center(), color=pal.OUTPUT,
                  stroke_width=5)
        self.play(FadeIn(tq), FadeIn(t1), FadeIn(t2))
        self.play(Create(l1), Create(l2))
        eq = self.txt("Equally near: average their y values", color=pal.TEXT)
        self.fit_width(eq, W * 0.88)
        eq.next_to(tq, UP, buff=1.0)
        self.type_in(eq)
        res = self.txt("Reaches the minimum training error", color=pal.OUTPUT)
        self.fit_width(res, W * 0.88)
        res.to_edge(DOWN, buff=1.3)
        self.type_in(res)
        self.wait(1)
        self.dust_wipe([head, tq, t1, t2, l1, l2, eq, res])

        # ===== Scene 6: takeaway =========================================
        t1 = self.txt("Too much capacity widens the gap", color=pal.TEXT)
        t2 = self.txt("Nonparametric = unlimited capacity", color=pal.TEXT)
        take = VGroup(t1, t2).arrange(DOWN, buff=0.3)
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
