"""Page 115 - Figure 5.4: effect of training set size on error and on the
optimal model capacity."""
import numpy as np
from manim import *

import common.palette as pal
from common.chapter5_style import Chapter5Scene


def bayes(u):
    return 0.2


def train_quad(u):
    return 0.27 * (1 - np.exp(-1.3 * u))


def test_quad(u):
    return 0.6 + 2.9 * np.exp(-1.5 * u)


def test_opt(u):
    return 0.22 + 3.28 * np.exp(-2.2 * u)


def train_opt(u):
    return 0.04 + 0.20 * (1 - np.exp(-0.9 * u))


def opt_degree(u):
    return 3 + 12 / (1 + np.exp(-1.6 * (u - 2.2)))


def true_poly(x):
    d = x - 0.5
    return 0.5 + 1.5 * d - 6 * d ** 3 + 12 * d ** 5


class Page_115(Chapter5Scene):
    PAGE_NO = "115"
    RNG_SEED = 1151

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
        with open("assets/audio/raw/page_115_events.json", "w") as f:
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

    def zoom_pulse(self, *args, **kwargs):
        t0 = self._now()
        r = super().zoom_pulse(*args, **kwargs)
        self._log("pulse", t0, self._now())
        return r

    def _fit(self, mob, w):
        if mob.width > w:
            self.fit_width(mob, w)

    def _axes(self, ymax, ylab, w=5.6, h=3.4):
        ax = Axes(x_range=[0, 5, 1], y_range=[0, ymax, 1], x_length=w,
                  y_length=h, tips=False,
                  axis_config={"include_ticks": False, "include_numbers": False,
                               "color": pal.TEXT})
        ax.move_to(UP * 0.35)
        ticks = VGroup()
        for u, lab in ((0, r"10^0"), (2.5, r"10^{2.5}"), (5, r"10^5")):
            t = self.formula(lab).scale(0.5)
            t.next_to(ax.c2p(u, 0), DOWN, buff=0.12)
            ticks.add(t)
        xl = self.txt("training examples", color=pal.TEXT)
        xl.scale(0.7).next_to(ax, DOWN, buff=0.5)
        yl = self.txt(ylab, color=pal.TEXT)
        yl.scale(0.7).rotate(PI / 2).next_to(ax, LEFT, buff=0.2)
        return ax, VGroup(ticks, xl, yl)

    def _curve(self, ax, fn, color, dashed=False):
        c = ax.plot(lambda u: float(fn(u)), x_range=[0.02, 5], color=color,
                    stroke_width=5)
        if dashed:
            c = DashedVMobject(c, num_dashes=30)
        return c

    def _bayes_line(self, ax):
        return DashedLine(ax.c2p(0, 0.2), ax.c2p(5, 0.2),
                          color=pal.DISTRIBUTION, stroke_width=4)

    def construct(self):
        self.init_page()
        W = config.frame_width

        # ===== Scene 1: the synthetic problem ============================
        head = self.txt("Figure 5.4: the setup", color=pal.DISTRIBUTION)
        self._fit(head, W * 0.9)
        head.to_edge(UP, buff=0.9)
        self.type_in(head)

        ax = Axes(x_range=[0, 1, 1], y_range=[0, 1, 1], x_length=4.6,
                  y_length=3.0, tips=False,
                  axis_config={"include_ticks": False, "include_numbers": False,
                               "color": pal.TEXT})
        ax.move_to(UP * 0.4)
        self.play(Create(ax))
        poly = ax.plot(lambda x: float(true_poly(x)), x_range=[0, 1],
                       color=pal.OUTPUT, stroke_width=5)
        self.play(Create(poly), run_time=1.2)
        rng = np.random.default_rng(115)
        dots = VGroup()
        for x in np.linspace(0.04, 0.96, 14):
            y = float(np.clip(true_poly(x) + rng.normal(0, 0.07), 0.02, 0.98))
            dots.add(Dot(ax.c2p(x, y), radius=0.07, color=pal.INPUT))
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots],
                              lag_ratio=0.08))
        c1 = self.txt("Degree-5 polynomial plus noise", color=pal.OUTPUT)
        c2 = self.txt("40 training sets per size, 95% error bars", color=pal.TEXT)
        caps = VGroup(c1, c2).arrange(DOWN, buff=0.3)
        self._fit(caps, W * 0.88)
        caps.to_edge(DOWN, buff=1.2)
        self.type_in(c1)
        self.type_in(c2)
        self.wait(1)
        self.dust_wipe([head, ax, poly, dots, caps])

        # ===== Scene 2: quadratic model ==================================
        head = self.txt("Fixed capacity: quadratic", color=pal.DISTRIBUTION)
        self._fit(head, W * 0.9)
        head.to_edge(UP, buff=0.9)
        self.type_in(head)

        ax, labs = self._axes(3.5, "error (MSE)")
        self.play(Create(ax), FadeIn(labs))
        bl = self._bayes_line(ax)
        self.play(Create(bl))
        trq = self._curve(ax, train_quad, pal.INPUT)
        teq = self._curve(ax, test_quad, pal.ERROR)
        self.play(Create(trq), run_time=1.3)
        self.play(Create(teq), run_time=1.3)
        c1 = self.txt("Train error rises: more data is harder to fit",
                      color=pal.INPUT)
        c2 = self.txt("Test error falls, but stalls high", color=pal.ERROR)
        caps = VGroup(c1, c2).arrange(DOWN, buff=0.3)
        self._fit(caps, W * 0.9)
        caps.to_edge(DOWN, buff=1.0)
        self.type_in(c1)
        self.type_in(c2)
        self.wait(1)
        self.dust_wipe([head, ax, labs, bl, trq, teq, caps])

        # ===== Scene 3: optimal capacity =================================
        head = self.txt("Optimal capacity", color=pal.DISTRIBUTION)
        head.to_edge(UP, buff=0.9)
        self.type_in(head)

        ax, labs = self._axes(3.5, "error (MSE)")
        self.play(Create(ax), FadeIn(labs))
        bl = self._bayes_line(ax)
        self.play(Create(bl))
        teo = self._curve(ax, test_opt, pal.OUTPUT)
        tro = self._curve(ax, train_opt, pal.FORMULA)
        self.play(Create(teo), run_time=1.3)
        self.play(Create(tro), run_time=1.3)
        c1 = self.txt("Test error reaches the Bayes error", color=pal.OUTPUT)
        c2 = self.txt("Train error can dip below it: memorizing",
                      color=pal.FORMULA)
        caps = VGroup(c1, c2).arrange(DOWN, buff=0.3)
        self._fit(caps, W * 0.9)
        caps.to_edge(DOWN, buff=1.0)
        self.type_in(c1)
        self.type_in(c2)
        self.wait(1)
        self.dust_wipe([head, ax, labs, bl, teo, tro, caps])

        # ===== Scene 4: fixed capacity limit =============================
        head = self.txt("Infinite data", color=pal.DISTRIBUTION)
        head.to_edge(UP, buff=0.9)
        self.type_in(head)

        ax, labs = self._axes(1.0, "train error", h=3.0)
        self.play(Create(ax), FadeIn(labs))
        bl = DashedLine(ax.c2p(0, 0.5), ax.c2p(5, 0.5), color=pal.DISTRIBUTION,
                        stroke_width=4)
        self.play(Create(bl))
        rise = ax.plot(lambda u: float(0.62 * (1 - np.exp(-0.9 * u))),
                       x_range=[0.02, 5], color=pal.INPUT, stroke_width=5)
        self.play(Create(rise), run_time=1.4)
        fm = self.formula(
            r"m \to \infty:\ \ \text{train error} \;\ge\; \text{Bayes error}")
        fm.set_color(pal.FORMULA)
        self._fit(fm, W * 0.9)
        fm.to_edge(DOWN, buff=1.7)
        self.play(Write(fm))
        cp = self.txt("True for any fixed-capacity model", color=pal.TEXT)
        self._fit(cp, W * 0.88)
        cp.next_to(fm, DOWN, buff=0.3)
        self.type_in(cp)
        self.wait(1)
        self.dust_wipe([head, ax, labs, bl, rise, fm, cp])

        # ===== Scene 5: optimal degree vs training set size ==============
        head = self.txt("Optimal capacity grows", color=pal.DISTRIBUTION)
        head.to_edge(UP, buff=0.9)
        self.type_in(head)

        ax, labs = self._axes(20, "optimal polynomial degree")
        self.play(Create(ax), FadeIn(labs))
        curve = ax.plot(lambda u: float(opt_degree(u)), x_range=[0.02, 5],
                        color=pal.OUTPUT, stroke_width=5)
        self.play(Create(curve), run_time=1.6)
        plat = DashedLine(ax.c2p(2.8, 15), ax.c2p(5, 15), color=pal.FORMULA,
                          stroke_width=4)
        self.play(Create(plat))
        c1 = self.txt("More data supports a higher degree", color=pal.OUTPUT)
        c2 = self.txt("Then it plateaus: complexity is enough", color=pal.FORMULA)
        caps = VGroup(c1, c2).arrange(DOWN, buff=0.3)
        self._fit(caps, W * 0.9)
        caps.to_edge(DOWN, buff=1.0)
        self.type_in(c1)
        self.type_in(c2)
        self.wait(1)
        self.dust_wipe([head, ax, labs, curve, plat, caps])

        # ===== Scene 6: takeaway =========================================
        t1 = self.txt("More data supports more capacity,", color=pal.TEXT)
        t2 = self.txt("down to the Bayes error", color=pal.TEXT)
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
