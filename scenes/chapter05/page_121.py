"""Page 121 - Algorithm 5.1 (k-fold cross-validation) and point estimators (5.19).
Sound design: ASMRSync cues only (SFX, no background music)."""

from manim import *
import numpy as np

from common.chapter5_style import Chapter5Scene
from common import palette as pal
from common.asmr_sync import ASMRSync


def shrink(mob, width):
    """Only ever shrink a mobject to fit; never enlarge it."""
    if mob.width > width:
        mob.scale(width / mob.width)
    return mob


class Page_121(Chapter5Scene):
    PAGE_NO = "121"
    RNG_SEED = 121

    def construct(self):
        self.init_page()
        audio = ASMRSync(self, self.PAGE_NO)

        # 1. A small test set gives a noisy estimate. (~12 s)
        title1 = self.txt("Why k-fold cross-validation?", 30, pal.TEXT, BOLD)
        self.fit_width(title1, 7.8)
        title1.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title1.text)):
            self.type_in(title1, run_time=1.6)
        cap1 = shrink(self.txt("mean loss L on a small test set", 26, pal.INPUT), 7.4).move_to(UP * 2.3)
        line1 = NumberLine(x_range=[0, 10, 1], length=6.4, include_numbers=False,
                           color=pal.TEXT_DIM, stroke_width=2).move_to(UP * 0.9)
        with audio.cue("draw"):
            self.play(FadeIn(cap1), Create(line1), run_time=1.2)
        dots1 = VGroup(*[Dot(line1.n2p(x), radius=0.15, color=pal.ERROR) for x in (2.6, 7.2, 4.3)])
        for i, d in enumerate(dots1):
            with audio.cue("grow", pan=-0.4 + 0.4 * i):
                self.play(FadeIn(d, scale=0.4), run_time=1.0, rate_func=smooth)
        spread1 = DoubleArrow(line1.n2p(2.6) + DOWN * 0.55, line1.n2p(7.2) + DOWN * 0.55,
                              buff=0, color=pal.FORMULA, stroke_width=4, tip_length=0.18)
        slab1 = self.txt("high variance", 26, pal.FORMULA).next_to(spread1, DOWN, buff=0.2)
        with audio.cue("settle"):
            self.play(GrowFromCenter(spread1), FadeIn(slab1), run_time=1.2)
        note1 = self.txt("A small split gives a noisy estimate\nof the generalization error.", 26, pal.TEXT)
        self.fit_width(note1, 7.6)
        note1.move_to(DOWN * 2.3)
        with audio.cue("type", glyphs=len(note1.text)):
            self.type_in(note1, run_time=1.8)
        self.wait(1.0)
        with audio.cue("wipe"):
            self.dust_wipe([title1, cap1, line1, dots1, spread1, slab1, note1], run_time=2.4)

        # 2. The four inputs of KFoldXV. (~14 s)
        title2 = self.txt("Algorithm 5.1: the inputs", 30, pal.TEXT, BOLD)
        self.fit_width(title2, 7.8)
        title2.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title2.text)):
            self.type_in(title2, run_time=1.6)
        specs = [
            (r"\mathbb{D}", "dataset of examples", pal.INPUT, (-2.0, 1.7)),
            (r"A", "learning algorithm", pal.OUTPUT, (2.0, 1.7)),
            (r"L", "loss function", pal.ERROR, (-2.0, -0.1)),
            (r"k", "number of folds", pal.DISTRIBUTION, (2.0, -0.1)),
        ]
        cards2 = VGroup()
        for sym, desc, col, (x, y) in specs:
            rect = RoundedRectangle(width=3.6, height=1.55, corner_radius=0.18, color=col).move_to([x, y, 0])
            s = self.formula(sym, 42, col).move_to(rect.get_center() + UP * 0.35)
            d = shrink(self.txt(desc, 22, pal.TEXT), 3.2).move_to(rect.get_center() + DOWN * 0.42)
            cards2.add(VGroup(rect, s, d))
            with audio.cue("grow", pan=-0.4 if x < 0 else 0.4):
                self.play(GrowFromCenter(rect), Write(s), FadeIn(d), run_time=1.4, rate_func=smooth)
        zf = self.formula(r"\mathbf{z}^{(i)}=(\mathbf{x}^{(i)},y^{(i)})\ \text{or}\ \mathbf{x}^{(i)}",
                          34, pal.FORMULA)
        self.fit_width(zf, 7.4)
        zf.move_to(DOWN * 1.75)
        with audio.cue("draw"):
            self.play(Write(zf), run_time=1.6)
        note2 = self.txt("supervised pair, or just an input", 25, pal.TEXT).move_to(DOWN * 2.7)
        with audio.cue("type", glyphs=len(note2.text)):
            self.type_in(note2, run_time=1.4)
        self.wait(1.0)
        with audio.cue("wipe"):
            self.dust_wipe([title2, cards2, zf, note2], run_time=2.4)

        # 3. Split D into k mutually exclusive subsets. (~13 s)
        title3 = self.txt("Split D into k folds", 31, pal.TEXT, BOLD)
        title3.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title3.text)):
            self.type_in(title3, run_time=1.6)
        whole3 = Rectangle(width=6.4, height=0.9, color=pal.INPUT, fill_color=pal.INPUT,
                           fill_opacity=0.25).move_to(UP * 1.7)
        wlab3 = self.formula(r"\mathbb{D}", 34, pal.INPUT).move_to(whole3)
        with audio.cue("grow"):
            self.play(GrowFromEdge(whole3, LEFT), FadeIn(wlab3), run_time=1.6, rate_func=smooth)
        self.wait(0.6)
        pieces3 = VGroup(*[Rectangle(width=1.15, height=0.9, color=pal.INPUT, fill_color=pal.INPUT,
                                     fill_opacity=0.3) for _ in range(5)])
        pieces3.arrange(RIGHT, buff=0.12).move_to(UP * 1.7)
        labs3 = VGroup(*[self.formula(r"\mathbb{D}_{%d}" % (i + 1), 28, pal.TEXT).move_to(p)
                         for i, p in enumerate(pieces3)])
        with audio.cue("slide", profile="transfer"):
            self.play(FadeOut(whole3), FadeOut(wlab3),
                      LaggedStart(*[GrowFromCenter(p) for p in pieces3], lag_ratio=0.15),
                      FadeIn(labs3), run_time=2.2)
        union3 = self.formula(r"\mathbb{D}=\mathbb{D}_1\cup\cdots\cup\mathbb{D}_k", 36, pal.FORMULA)
        self.fit_width(union3, 7.2)
        union3.move_to(UP * 0.1)
        with audio.cue("draw"):
            self.play(Write(union3), run_time=1.6)
        note3 = self.txt("Mutually exclusive subsets,\ntheir union is the whole dataset.", 26, pal.TEXT)
        self.fit_width(note3, 7.6)
        note3.move_to(DOWN * 2.2)
        with audio.cue("type", glyphs=len(note3.text)):
            self.type_in(note3, run_time=1.8)
        self.wait(1.0)
        with audio.cue("wipe"):
            self.dust_wipe([title3, pieces3, labs3, union3, note3], run_time=2.4)

        # 4. The loop: train on the rest, test on fold i, collect errors. (~16 s)
        title4 = self.txt("for i from 1 to k", 31, pal.TEXT, BOLD)
        title4.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title4.text)):
            self.type_in(title4, run_time=1.6)
        f_eq = self.formula(r"f_i=A(\mathbb{D}\setminus\mathbb{D}_i)", 36, pal.OUTPUT).move_to(UP * 2.5)
        e_eq = self.formula(r"e_j=L(f_i,\mathbf{z}^{(j)}),\ \ \mathbf{z}^{(j)}\in\mathbb{D}_i", 34, pal.ERROR)
        self.fit_width(e_eq, 7.4)
        e_eq.move_to(UP * 1.6)
        with audio.cue("draw"):
            self.play(Write(f_eq), run_time=1.4)
        with audio.cue("draw"):
            self.play(Write(e_eq), run_time=1.6)
        folds4 = VGroup(*[Rectangle(width=1.15, height=0.8, color=pal.INPUT, fill_color=pal.INPUT,
                                    fill_opacity=0.3) for _ in range(5)])
        folds4.arrange(RIGHT, buff=0.12).move_to(UP * 0.4)
        labs4 = VGroup(*[self.formula(r"\mathbb{D}_{%d}" % (i + 1), 26, pal.TEXT).move_to(f)
                         for i, f in enumerate(folds4)])
        base_y = -1.9
        base4 = Line(LEFT * 3.2, RIGHT * 3.2, color=pal.TEXT_DIM, stroke_width=2).move_to([0, base_y, 0])
        elab4 = self.formula(r"\mathbf{e}", 34, pal.ERROR).move_to([-3.65, base_y + 0.5, 0])
        with audio.cue("grow"):
            self.play(LaggedStart(*[GrowFromCenter(f) for f in folds4], lag_ratio=0.15),
                      FadeIn(labs4), Create(base4), FadeIn(elab4), run_time=1.4)
        rng = np.random.default_rng(121)
        heights = rng.uniform(0.35, 1.0, 15)
        bars4 = []
        for i in range(5):
            grp = VGroup()
            for k in range(3):
                h = float(heights[3 * i + k])
                b = Rectangle(width=0.26, height=h, color=pal.ERROR, fill_color=pal.ERROR, fill_opacity=0.4)
                b.move_to([folds4[i].get_center()[0] + (k - 1) * 0.34, base_y + h / 2, 0])
                grp.add(b)
            bars4.append(grp)
        marker = Triangle(color=pal.OUTPUT, fill_color=pal.OUTPUT, fill_opacity=1).scale(0.14).rotate(PI)
        marker.move_to(folds4[0].get_top() + UP * 0.25)
        for i in range(5):
            anims = []
            if i == 0:
                anims.append(FadeIn(marker))
            else:
                anims.append(folds4[i - 1].animate.set_fill(pal.INPUT, opacity=0.3).set_stroke(pal.INPUT))
                anims.append(marker.animate.move_to(folds4[i].get_top() + UP * 0.25))
            anims.append(folds4[i].animate.set_fill(pal.OUTPUT, opacity=0.55).set_stroke(pal.OUTPUT))
            anims += [GrowFromEdge(b, DOWN) for b in bars4[i]]
            with audio.cue("grow", pan=-0.5 + 0.25 * i):
                self.play(*anims, run_time=1.1, rate_func=smooth)
        note4 = self.txt("Return e: one error for every example.", 26, pal.TEXT)
        self.fit_width(note4, 7.6)
        note4.move_to(DOWN * 2.7)
        with audio.cue("type", glyphs=len(note4.text)):
            self.type_in(note4, run_time=1.6)
        self.wait(1.0)
        all_bars4 = VGroup(*[b for g in bars4 for b in g])
        with audio.cue("wipe"):
            self.dust_wipe([title4, f_eq, e_eq, folds4, labs4, base4, elab4, marker, all_bars4, note4],
                           run_time=2.4)

        # 5. Mean error and confidence intervals. (~13 s)
        title5 = self.txt("Mean error and intervals", 30, pal.TEXT, BOLD)
        self.fit_width(title5, 7.8)
        title5.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title5.text)):
            self.type_in(title5, run_time=1.6)
        mean5 = self.formula(r"\mathrm{mean}(\mathbf{e})\approx\text{generalization error}", 34, pal.FORMULA)
        self.fit_width(mean5, 7.4)
        mean5.move_to(UP * 2.5)
        with audio.cue("draw"):
            self.play(Write(mean5), run_time=1.6)
        line5 = NumberLine(x_range=[0, 10, 1], length=6.4, include_numbers=False,
                           color=pal.TEXT_DIM, stroke_width=2).move_to(DOWN * 0.9)
        elab5 = self.txt("error", 22, pal.TEXT_DIM).next_to(line5, DOWN, buff=0.15)
        with audio.cue("draw"):
            self.play(Create(line5), FadeIn(elab5), run_time=1.0)

        def X(v):
            return line5.n2p(v)[0]

        def ci_row(y, lo, hi, mean, col, name):
            bar = Line([X(lo), y, 0], [X(hi), y, 0], color=col, stroke_width=8)
            caps = VGroup(Line([X(lo), y - 0.18, 0], [X(lo), y + 0.18, 0], color=col, stroke_width=4),
                          Line([X(hi), y - 0.18, 0], [X(hi), y + 0.18, 0], color=col, stroke_width=4))
            dot = Dot([X(mean), y, 0], radius=0.11, color=pal.FORMULA)
            lab = self.formula(name, 32, col).move_to([-3.5, y, 0])
            return VGroup(bar, caps, dot, lab)

        rowA = ci_row(1.0, 2.0, 4.2, 3.1, pal.OUTPUT, "A")
        rowB = ci_row(0.0, 5.0, 7.4, 6.2, pal.DISTRIBUTION, "B")
        with audio.cue("grow", pan=-0.3):
            self.play(GrowFromCenter(rowA), run_time=1.4, rate_func=smooth)
        with audio.cue("grow", pan=0.3):
            self.play(GrowFromCenter(rowB), run_time=1.4, rate_func=smooth)
        gap5 = DoubleArrow([X(4.2), 0.5, 0], [X(5.0), 0.5, 0], buff=0, color=pal.FORMULA,
                           stroke_width=4, tip_length=0.15)
        with audio.cue("settle"):
            self.play(GrowFromCenter(gap5), run_time=1.0)
        note5 = self.txt("Declare A better only if its interval lies\nbelow B's and does not intersect it.", 25, pal.TEXT)
        self.fit_width(note5, 7.7)
        note5.move_to(DOWN * 2.5)
        with audio.cue("type", glyphs=len(note5.text)):
            self.type_in(note5, run_time=2.0)
        self.wait(1.0)
        with audio.cue("wipe"):
            self.dust_wipe([title5, mean5, line5, elab5, rowA, rowB, gap5, note5], run_time=2.4)

        # 6. Point estimator: any function of the data. (~14 s)
        title6 = self.txt("Point estimator: a statistic", 30, pal.TEXT, BOLD)
        self.fit_width(title6, 7.8)
        title6.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title6.text)):
            self.type_in(title6, run_time=1.6)
        eq6 = self.formula(r"\hat{\boldsymbol{\theta}}_m=g(\mathbf{x}^{(1)},\dots,\mathbf{x}^{(m)})", 38, pal.FORMULA)
        self.fit_width(eq6, 7.2)
        eq6.move_to(UP * 2.5)
        num6 = self.txt("(5.19)", 22, pal.TEXT_DIM).next_to(eq6, DOWN, buff=0.2)
        with audio.cue("draw"):
            self.play(Write(eq6), FadeIn(num6), run_time=1.6)
        pts = [(-3.2, 0.5), (-2.8, 0.1), (-3.0, -0.3), (-2.6, 0.35), (-3.3, -0.05)]
        dots6 = VGroup(*[Dot([x, y + 0.2, 0], radius=0.1, color=pal.DISTRIBUTION) for x, y in pts])
        with audio.cue("grow"):
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots6], lag_ratio=0.15), run_time=1.4)
        box6 = RoundedRectangle(width=1.4, height=1.2, corner_radius=0.15, color=pal.FORMULA).move_to([0, 0.2, 0])
        g6 = self.formula(r"g", 44, pal.FORMULA).move_to(box6)
        arr_in = Arrow([-2.2, 0.2, 0], box6.get_left(), buff=0.08, color=pal.TEXT_DIM, stroke_width=4)
        arr_out = Arrow(box6.get_right(), [2.0, 0.2, 0], buff=0.08, color=pal.TEXT_DIM, stroke_width=4)
        with audio.cue("draw"):
            self.play(GrowFromCenter(box6), FadeIn(g6), Create(arr_in), Create(arr_out), run_time=1.2)
        with audio.cue("slide", profile="transfer"):
            self.play(dots6.animate.move_to(box6.get_center()).set_opacity(0), run_time=1.6, rate_func=smooth)
        out6 = Dot([2.7, 0.2, 0], radius=0.14, color=pal.FORMULA)
        outlab6 = self.formula(r"\hat{\boldsymbol{\theta}}_m", 32, pal.FORMULA).next_to(out6, DOWN, buff=0.2)
        with audio.cue("settle"):
            self.play(FadeIn(out6, scale=0.4), FadeIn(outlab6), run_time=1.0)
        note6 = self.txt("Almost any function qualifies.\ng need not be close to the true value,\nor even share its range.", 25, pal.TEXT)
        self.fit_width(note6, 7.6)
        note6.move_to(DOWN * 2.3)
        with audio.cue("type", glyphs=len(note6.text)):
            self.type_in(note6, run_time=2.4)
        self.wait(1.0)
        with audio.cue("wipe"):
            self.dust_wipe([title6, eq6, num6, box6, g6, arr_in, arr_out, dots6, out6, outlab6, note6],
                           run_time=2.4)

        # 7. Closing thought and camera emphasis. (~10 s)
        final = self.txt("Split into folds, test each one,\naverage the errors.", 30, pal.TEXT, BOLD)
        self.fit_width(final, 7.6)
        final.move_to(ORIGIN)
        with audio.cue("type", glyphs=len(final.text)):
            self.type_in(final, run_time=2.4)
        underline = Underline(final, color=pal.INPUT, stroke_width=3, buff=0.22)
        with audio.cue("draw"):
            self.play(Create(underline), run_time=1.4)
        self.wait(0.8)
        with audio.cue("zoom"):
            self.zoom_pulse(final, zoom_scale=0.96, run_time_in=1.2, hold=0.6, run_time_out=1.2)
        self.wait(3.0)
        audio.finish()


if __name__ == "__main__":
    Page_121().render()
