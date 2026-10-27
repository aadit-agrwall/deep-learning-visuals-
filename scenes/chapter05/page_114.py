"""Page 114 - wrapping parametric models, Bayes error, data size,
5.2.1 The No Free Lunch Theorem."""
import numpy as np
from manim import *

import common.palette as pal
from common.chapter5_style import Chapter5Scene


class Page_114(Chapter5Scene):
    PAGE_NO = "114"
    RNG_SEED = 1141

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
        with open("assets/audio/raw/page_114_events.json", "w") as f:
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

    def _dot_grid(self):
        g = VGroup(*[Dot(radius=0.12, color=pal.INPUT) for _ in range(20)])
        g.arrange_in_grid(rows=4, cols=5, buff=0.45)
        return g

    def construct(self):
        self.init_page()
        W = config.frame_width

        # ===== Scene 1: wrapping a parametric model =====================
        head = self.txt("Wrapping a parametric model", color=pal.DISTRIBUTION)
        self._fit(head, W * 0.9)
        head.to_edge(UP, buff=0.9)
        self.type_in(head)

        cells = VGroup()
        for lab in ["deg 1", "deg 2", "deg 3", "deg n"]:
            r = RoundedRectangle(width=1.5, height=1.1, corner_radius=0.15,
                                 color=pal.INPUT)
            t = self.txt(lab, color=pal.TEXT)
            self._fit(t, 1.3)
            t.move_to(r)
            cells.add(VGroup(r, t))
        cells.arrange(RIGHT, buff=0.45).move_to(UP * 0.5)
        arrows = VGroup(*[
            Arrow(cells[i].get_right(), cells[i + 1].get_left(), buff=0.05,
                  tip_length=0.12, stroke_width=3, color=pal.TEXT)
            for i in range(3)
        ])
        outer = SurroundingRectangle(VGroup(cells, arrows),
                                     color=pal.DISTRIBUTION, buff=0.3)
        self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.3))
        self.play(Create(arrows))
        self.play(Create(outer))

        c1 = self.txt("Outer loop adds parameters as needed",
                      color=pal.DISTRIBUTION)
        c2 = self.txt("e.g. it raises the polynomial degree", color=pal.TEXT)
        caps = VGroup(c1, c2).arrange(DOWN, buff=0.3)
        self._fit(caps, W * 0.88)
        caps.to_edge(DOWN, buff=1.2)
        self.type_in(c1)
        self.type_in(c2)
        self.wait(1)
        self.dust_wipe([head, cells, arrows, outer, caps])

        # ===== Scene 2: Bayes error =====================================
        head = self.txt("Bayes error", color=pal.DISTRIBUTION)
        head.to_edge(UP, buff=0.9)
        self.type_in(head)

        axes = Axes(x_range=[0, 1, 1], y_range=[0, 1, 1], x_length=5.4,
                    y_length=3.4, tips=False,
                    axis_config={"include_ticks": False,
                                 "include_numbers": False,
                                 "color": pal.TEXT})
        axes.move_to(UP * 0.3)
        self.play(Create(axes))
        curve = axes.plot(lambda x: 0.5 + 0.28 * np.sin(5 * x),
                          x_range=[0, 1], color=pal.OUTPUT, stroke_width=5)
        self.play(Create(curve), run_time=1.2)
        rng = np.random.default_rng(114)
        xs = np.linspace(0.05, 0.95, 12)
        dots = VGroup()
        for x in xs:
            y = float(np.clip(0.5 + 0.28 * np.sin(5 * x)
                              + rng.normal(0, 0.09), 0.03, 0.97))
            dots.add(Dot(axes.c2p(x, y), radius=0.07, color=pal.INPUT))
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots],
                              lag_ratio=0.1))

        c1 = self.txt("Oracle knows the true p(x, y)", color=pal.OUTPUT)
        c2 = self.txt("Noise still causes some error", color=pal.ERROR)
        caps = VGroup(c1, c2).arrange(DOWN, buff=0.3)
        self._fit(caps, W * 0.88)
        caps.to_edge(DOWN, buff=1.1)
        self.type_in(c1)
        self.type_in(c2)
        bayes = self.txt("Bayes error", color=pal.FORMULA)
        bayes.scale(0.8).next_to(axes, UP, buff=0.2)
        bbox = SurroundingRectangle(bayes, color=pal.FORMULA, buff=0.12)
        self.type_in(bayes)
        self.play(Create(bbox))
        self.wait(1)
        self.dust_wipe([head, axes, curve, dots, caps, bayes, bbox])

        # ===== Scene 3: error vs training set size ======================
        head = self.txt("More data, lower error", color=pal.DISTRIBUTION)
        self._fit(head, W * 0.9)
        head.to_edge(UP, buff=0.9)
        self.type_in(head)

        axes = Axes(x_range=[0, 1, 1], y_range=[0, 1, 1], x_length=5.4,
                    y_length=3.4, tips=False,
                    axis_config={"include_ticks": False,
                                 "include_numbers": False,
                                 "color": pal.TEXT})
        axes.move_to(UP * 0.3)
        xl = self.txt("training examples", color=pal.TEXT)
        xl.scale(0.75).next_to(axes, DOWN, buff=0.2)
        yl = self.txt("generalization error", color=pal.TEXT)
        yl.scale(0.75).rotate(PI / 2).next_to(axes, LEFT, buff=0.2)
        self.play(Create(axes), FadeIn(xl), FadeIn(yl))
        floor = DashedLine(axes.c2p(0, 0.2), axes.c2p(1, 0.2),
                           color=pal.FORMULA)
        fl = self.txt("Bayes error", color=pal.FORMULA)
        fl.scale(0.7).next_to(floor, DOWN, buff=0.12).align_to(floor, RIGHT)
        self.play(Create(floor), FadeIn(fl))
        par = axes.plot(lambda x: 0.5 + 0.45 * np.exp(-5 * x),
                        x_range=[0.01, 1], color=pal.ERROR, stroke_width=5)
        non = axes.plot(lambda x: 0.2 + 0.7 * np.exp(-3 * x),
                        x_range=[0.01, 1], color=pal.OUTPUT, stroke_width=5)
        self.play(Create(par), run_time=1.3)
        self.play(Create(non), run_time=1.3)

        k1 = self.txt("Fixed parametric: stalls above Bayes", color=pal.ERROR)
        k2 = self.txt("Nonparametric: reaches Bayes error", color=pal.OUTPUT)
        keys = VGroup(k1, k2).arrange(DOWN, buff=0.25)
        self._fit(keys, W * 0.88)
        keys.to_edge(DOWN, buff=0.95)
        self.type_in(k1)
        self.type_in(k2)
        self.wait(1)
        self.dust_wipe([head, axes, xl, yl, floor, fl, par, non, keys])

        # ===== Scene 4: induction is not logically valid =================
        head = self.txt("The No Free Lunch Theorem", color=pal.DISTRIBUTION)
        self._fit(head, W * 0.9)
        head.to_edge(UP, buff=0.9)
        self.type_in(head)

        grid = self._dot_grid().move_to(UP * 0.5)
        grid.set_opacity(0.25)
        self.play(FadeIn(grid))
        picks = [2, 6, 11, 17]
        self.play(*[grid[i].animate.set_color(pal.OUTPUT).set_opacity(1)
                    for i in picks])
        l1 = self.txt("A finite set of examples", color=pal.OUTPUT)
        self.type_in(l1.to_edge(DOWN, buff=2.4))
        box = SurroundingRectangle(grid, color=pal.ERROR, buff=0.3)
        self.play(Create(box))
        l2 = self.txt("Rule for every member?", color=pal.ERROR)
        l3 = self.txt("Induction is not logically valid", color=pal.TEXT)
        stack = VGroup(l1, l2, l3).arrange(DOWN, buff=0.25)
        self._fit(stack, W * 0.88)
        stack.to_edge(DOWN, buff=0.9)
        l1.move_to(l1.get_center())
        self.type_in(l2)
        self.type_in(l3)
        self.wait(1)
        self.dust_wipe([head, grid, box, stack])

        # ===== Scene 5: probabilistic rules ==============================
        head = self.txt("Probabilistic rules", color=pal.DISTRIBUTION)
        head.to_edge(UP, buff=0.9)
        self.type_in(head)

        grid = self._dot_grid().move_to(UP * 0.5)
        self.play(FadeIn(grid))
        self.play(*[grid[i].animate.set_color(pal.OUTPUT)
                    for i in range(20) if i not in (4, 9, 15)],
                  *[grid[i].animate.set_color(pal.ERROR) for i in (4, 9, 15)])
        l1 = self.txt("Rules that are probably correct", color=pal.TEXT)
        l2 = self.txt("about most members of the set", color=pal.OUTPUT)
        stack = VGroup(l1, l2).arrange(DOWN, buff=0.3)
        self._fit(stack, W * 0.88)
        stack.to_edge(DOWN, buff=1.2)
        self.type_in(l1)
        self.type_in(l2)
        self.wait(1)
        self.dust_wipe([head, grid, stack])

        # ===== Scene 6: the theorem statement ============================
        head = self.txt("Wolpert, 1996", color=pal.DISTRIBUTION)
        head.to_edge(UP, buff=0.9)
        self.type_in(head)

        t1 = self.txt("Averaged over all possible", color=pal.TEXT)
        t2 = self.txt("data-generating distributions,", color=pal.TEXT)
        t3 = self.txt("every classification algorithm", color=pal.FORMULA)
        t4 = self.txt("has the...", color=pal.FORMULA)
        st = VGroup(t1, t2, t3, t4).arrange(DOWN, buff=0.35).move_to(UP * 0.4)
        self._fit(st, W * 0.88)
        for ln in st:
            self.type_in(ln)
            self.wait(0.2)
        lunch = self.txt("free lunch", color=pal.ERROR)
        lunch.to_edge(DOWN, buff=1.4)
        self.type_in(lunch)
        cross = Cross(lunch, stroke_color=pal.ERROR, stroke_width=6)
        self.play(Create(cross))
        self.wait(1)
        self.dust_wipe([head, st, lunch, cross])

        # ===== Scene 7: takeaway =========================================
        t1 = self.txt("More data shrinks the gap,", color=pal.TEXT)
        t2 = self.txt("but cannot beat the Bayes error", color=pal.TEXT)
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
