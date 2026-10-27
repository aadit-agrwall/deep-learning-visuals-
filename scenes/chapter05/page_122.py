"""Page 122 - frequentist point estimates, function estimation, 5.4.2 Bias,
Bernoulli example. Sound design: ASMRSync cues only (SFX, no background music)."""

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


class Page_122(Chapter5Scene):
    PAGE_NO = "122"
    RNG_SEED = 122

    def construct(self):
        self.init_page()
        audio = ASMRSync(self, self.PAGE_NO)

        # 1. Frequentist view: theta fixed, theta-hat random. (~15 s)
        title1 = self.txt("Point estimates are random", 30, pal.TEXT, BOLD)
        self.fit_width(title1, 7.8)
        title1.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title1.text)):
            self.type_in(title1, run_time=1.6)
        cap1 = self.formula(r"\hat{\theta}=g(\text{data})", 38, pal.FORMULA).move_to(UP * 2.4)
        with audio.cue("draw"):
            self.play(Write(cap1), run_time=1.4)
        line1 = NumberLine(x_range=[0, 1, 0.1], length=6.2, include_numbers=False,
                           color=pal.TEXT_DIM, stroke_width=2).move_to(UP * 0.8)
        tick1 = Line(line1.n2p(0.6) + UP * 0.32, line1.n2p(0.6) + DOWN * 0.32,
                     color=pal.OUTPUT, stroke_width=5)
        theta1 = self.formula(r"\theta", 36, pal.OUTPUT).next_to(tick1, UP, buff=0.12)
        with audio.cue("draw"):
            self.play(Create(line1), Create(tick1), FadeIn(theta1), run_time=1.2)
        fixed1 = self.txt("true value: fixed, but unknown", 24, pal.OUTPUT)
        fixed1.next_to(line1, DOWN, buff=0.6)
        with audio.cue("type", glyphs=len(fixed1.text)):
            self.type_in(fixed1, run_time=1.4)
        vals1 = [0.47, 0.66, 0.55, 0.72, 0.51, 0.62]
        dots1 = VGroup(*[Dot(line1.n2p(v), radius=0.12, color=pal.FORMULA) for v in vals1])
        for i, d in enumerate(dots1):
            with audio.cue("grow", pan=-0.5 + 0.2 * i):
                self.play(FadeIn(d, scale=0.4), run_time=0.7, rate_func=smooth)
        note1 = self.txt("The data comes from a random process,\nso theta-hat is a random variable.", 26, pal.TEXT)
        self.fit_width(note1, 7.6)
        note1.move_to(DOWN * 2.3)
        with audio.cue("type", glyphs=len(note1.text)):
            self.type_in(note1, run_time=1.8)
        self.wait(1.0)
        with audio.cue("wipe"):
            self.dust_wipe([title1, cap1, line1, tick1, theta1, fixed1, dots1, note1], run_time=2.4)

        # 2. Function estimation. (~16 s)
        title2 = self.txt("Function estimation", 31, pal.TEXT, BOLD)
        title2.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title2.text)):
            self.type_in(title2, run_time=1.6)
        eq2 = self.formula(r"y=f(\mathbf{x})+\epsilon", 40, pal.FORMULA).move_to(UP * 2.5)
        with audio.cue("draw"):
            self.play(Write(eq2), run_time=1.4)
        axes2 = Axes(x_range=[0, 6, 1], y_range=[0, 4, 1], x_length=5.6, y_length=2.6,
                     axis_config={"color": pal.TEXT_DIM, "include_tip": False,
                                  "stroke_width": 1.5}).move_to(UP * 0.4)
        f_true = lambda t: 1.6 + 1.1 * np.sin(0.9 * t)
        f_est = lambda t: 1.55 + 1.0 * np.sin(0.9 * t + 0.12)
        curve2 = axes2.plot(f_true, x_range=[0.1, 5.9], color=pal.OUTPUT, stroke_width=4)
        with audio.cue("draw"):
            self.play(Create(axes2), Create(curve2), run_time=1.8)
        rng = np.random.default_rng(122)
        xs = np.linspace(0.4, 5.6, 12)
        ys = np.clip(f_true(xs) + rng.normal(0, 0.35, xs.size), 0.15, 3.85)
        dots2 = VGroup(*[Dot(axes2.c2p(x, y), radius=0.08, color=pal.INPUT) for x, y in zip(xs, ys)])
        with audio.cue("grow"):
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots2], lag_ratio=0.1), run_time=1.6)
        fest2 = DashedVMobject(axes2.plot(f_est, x_range=[0.1, 5.9], color=pal.FORMULA, stroke_width=4),
                               num_dashes=30)
        with audio.cue("slide", profile="converge"):
            self.play(Create(fest2), run_time=2.0, rate_func=smooth)
        legend2 = VGroup(
            VGroup(self.formula(r"f", 30, pal.OUTPUT), self.txt("true", 22, pal.TEXT)).arrange(RIGHT, buff=0.15),
            VGroup(self.formula(r"\hat{f}", 30, pal.FORMULA), self.txt("estimate", 22, pal.TEXT)).arrange(RIGHT, buff=0.15),
            VGroup(self.formula(r"\epsilon", 30, pal.INPUT), self.txt("unpredictable part", 22, pal.TEXT)).arrange(RIGHT, buff=0.15),
        ).arrange(RIGHT, buff=0.5)
        self.fit_width(legend2, 7.6)
        legend2.move_to(DOWN * 1.5)
        with audio.cue("grow"):
            self.play(FadeIn(legend2, shift=UP * 0.1), run_time=1.0)
        note2 = self.txt("A function estimator is simply\na point estimator in function space.", 26, pal.TEXT)
        self.fit_width(note2, 7.6)
        note2.move_to(DOWN * 2.7)
        with audio.cue("type", glyphs=len(note2.text)):
            self.type_in(note2, run_time=1.8)
        self.wait(1.0)
        with audio.cue("wipe"):
            self.dust_wipe([title2, eq2, axes2, curve2, dots2, fest2, legend2, note2], run_time=2.4)

        # 3. Two views of the same model. (~12 s)
        title3 = self.txt("Two views, one model", 31, pal.TEXT, BOLD)
        title3.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title3.text)):
            self.type_in(title3, run_time=1.6)
        cardL = RoundedRectangle(width=3.4, height=1.7, corner_radius=0.18, color=pal.INPUT).move_to(LEFT * 2.2 + UP * 1.3)
        symL = self.formula(r"\mathbf{w}", 42, pal.INPUT).move_to(cardL.get_center() + UP * 0.38)
        txtL = shrink(self.txt("estimate a parameter", 22, pal.TEXT), 3.0).move_to(cardL.get_center() + DOWN * 0.45)
        cardR = RoundedRectangle(width=3.4, height=1.7, corner_radius=0.18, color=pal.OUTPUT).move_to(RIGHT * 2.2 + UP * 1.3)
        symR = self.formula(r"\hat{f}:\ \mathbf{x}\to y", 36, pal.OUTPUT).move_to(cardR.get_center() + UP * 0.38)
        txtR = shrink(self.txt("estimate a function", 22, pal.TEXT), 3.0).move_to(cardR.get_center() + DOWN * 0.45)
        with audio.cue("grow", pan=-0.4):
            self.play(GrowFromCenter(cardL), Write(symL), FadeIn(txtL), run_time=1.5, rate_func=smooth)
        with audio.cue("grow", pan=0.4):
            self.play(GrowFromCenter(cardR), Write(symR), FadeIn(txtR), run_time=1.5, rate_func=smooth)
        both3 = DoubleArrow(cardL.get_right(), cardR.get_left(), buff=0.1, color=pal.FORMULA, stroke_width=4)
        with audio.cue("slide", profile="transfer"):
            self.play(GrowArrow(both3), run_time=1.0)
        reg3 = VGroup(self.txt("linear regression", 24, pal.TEXT), self.txt("polynomial regression", 24, pal.TEXT))
        reg3.arrange(RIGHT, buff=0.9)
        self.fit_width(reg3, 7.4)
        reg3.move_to(DOWN * 0.7)
        with audio.cue("type", glyphs=sum(len(t.text) for t in reg3)):
            self.play(FadeIn(reg3, shift=UP * 0.1), run_time=1.2)
        note3 = self.txt("Both can be read either way:\nparameter w, or function f-hat from x to y.", 25, pal.TEXT)
        self.fit_width(note3, 7.7)
        note3.move_to(DOWN * 2.4)
        with audio.cue("type", glyphs=len(note3.text)):
            self.type_in(note3, run_time=1.8)
        self.wait(1.0)
        with audio.cue("wipe"):
            self.dust_wipe([title3, cardL, symL, txtL, cardR, symR, txtR, both3, reg3, note3], run_time=2.4)

        # 4. 5.4.2 Bias. (~15 s)
        title4 = self.txt("5.4.2 Bias", 31, pal.TEXT, BOLD)
        title4.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title4.text)):
            self.type_in(title4, run_time=1.6)
        eq4 = self.formula(r"\mathrm{bias}(\hat{\theta}_m)=\mathbb{E}(\hat{\theta}_m)-\theta", 38, pal.FORMULA)
        self.fit_width(eq4, 7.4)
        eq4.move_to(UP * 2.5)
        num4 = self.txt("(5.20)", 22, pal.TEXT_DIM).next_to(eq4, DOWN, buff=0.2)
        with audio.cue("draw"):
            self.play(Write(eq4), FadeIn(num4), run_time=1.8)
        line4 = NumberLine(x_range=[0, 1, 0.1], length=6.2, include_numbers=False,
                           color=pal.TEXT_DIM, stroke_width=2).move_to(UP * 0.7)
        tick4 = Line(line4.n2p(0.62) + UP * 0.32, line4.n2p(0.62) + DOWN * 0.32,
                     color=pal.OUTPUT, stroke_width=5)
        theta4 = self.formula(r"\theta", 34, pal.OUTPUT).next_to(tick4, UP, buff=0.1)
        with audio.cue("draw"):
            self.play(Create(line4), Create(tick4), FadeIn(theta4), run_time=1.0)
        vals4 = [0.30, 0.38, 0.44, 0.36, 0.50, 0.41]
        dots4 = VGroup(*[Dot(line4.n2p(v), radius=0.11, color=pal.FORMULA) for v in vals4])
        with audio.cue("grow"):
            self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in dots4], lag_ratio=0.15), run_time=1.6)
        mean_v = float(np.mean(vals4))
        mpt = Triangle(color=pal.DISTRIBUTION, fill_color=pal.DISTRIBUTION, fill_opacity=1).scale(0.16)
        mpt.move_to(line4.n2p(mean_v) + DOWN * 0.38)
        mlab = self.formula(r"\mathbb{E}(\hat{\theta}_m)", 30, pal.DISTRIBUTION).next_to(mpt, DOWN, buff=0.12)
        with audio.cue("settle"):
            self.play(FadeIn(mpt, shift=UP * 0.1), FadeIn(mlab), run_time=1.0)
        gap4 = DoubleArrow(line4.n2p(mean_v) + DOWN * 1.15, line4.n2p(0.62) + DOWN * 1.15, buff=0,
                           color=pal.ERROR, stroke_width=5, tip_length=0.16)
        glab4 = self.txt("bias", 26, pal.ERROR).next_to(gap4, DOWN, buff=0.12)
        with audio.cue("slide", profile="transfer"):
            self.play(GrowFromCenter(gap4), FadeIn(glab4), run_time=1.2)
        note4 = self.txt("The expectation is over the data;\ntheta is the true underlying value.", 25, pal.TEXT)
        self.fit_width(note4, 7.6)
        note4.move_to(DOWN * 2.8)
        with audio.cue("type", glyphs=len(note4.text)):
            self.type_in(note4, run_time=1.8)
        self.wait(1.0)
        with audio.cue("wipe"):
            self.dust_wipe([title4, eq4, num4, line4, tick4, theta4, dots4, mpt, mlab, gap4, glab4, note4],
                           run_time=2.4)

        # 5. Unbiased and asymptotically unbiased. (~15 s)
        title5 = self.txt("Unbiased, asymptotically unbiased", 29, pal.TEXT, BOLD)
        self.fit_width(title5, 7.8)
        title5.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title5.text)):
            self.type_in(title5, run_time=1.6)
        un5 = self.formula(r"\text{unbiased: }\mathrm{bias}(\hat{\theta}_m)=0\ \Rightarrow\ \mathbb{E}(\hat{\theta}_m)=\theta",
                           32, pal.OUTPUT)
        self.fit_width(un5, 7.5)
        un5.move_to(UP * 2.5)
        asy5 = self.formula(r"\text{asymptotically unbiased: }\lim_{m\to\infty}\mathrm{bias}(\hat{\theta}_m)=0",
                            32, pal.FORMULA)
        self.fit_width(asy5, 7.5)
        asy5.move_to(UP * 1.5)
        with audio.cue("draw"):
            self.play(Write(un5), run_time=1.8)
        with audio.cue("draw"):
            self.play(Write(asy5), run_time=1.8)
        axes5 = Axes(x_range=[0, 10, 1], y_range=[0, 1, 1], x_length=5.6, y_length=1.9,
                     axis_config={"color": pal.TEXT_DIM, "include_tip": False,
                                  "stroke_width": 1.5}).move_to(DOWN * 0.7)
        curve5 = axes5.plot(lambda t: 0.9 / (1 + 1.4 * t), x_range=[0, 10], color=pal.ERROR, stroke_width=4)
        xlab5 = self.txt("number of samples m", 22, pal.TEXT_DIM).next_to(axes5, DOWN, buff=0.15)
        ylab5 = self.txt("bias", 22, pal.ERROR).next_to(axes5, LEFT, buff=0.2).shift(UP * 0.5)
        with audio.cue("draw"):
            self.play(Create(axes5), FadeIn(xlab5), FadeIn(ylab5), run_time=1.2)
        bead5 = Dot(axes5.c2p(0, 0.9), radius=0.1, color=pal.FORMULA)
        self.add(bead5)
        with audio.cue("slide", profile="converge"):
            self.play(Create(curve5), MoveAlongPath(bead5, curve5), run_time=3.0, rate_func=smooth)
        with audio.cue("settle"):
            self.play(bead5.animate.set_color(pal.OUTPUT), run_time=0.8)
        note5 = self.txt("The bias shrinks toward 0\nas the sample size grows.", 26, pal.TEXT)
        self.fit_width(note5, 7.6)
        note5.move_to(DOWN * 2.85)
        with audio.cue("type", glyphs=len(note5.text)):
            self.type_in(note5, run_time=1.6)
        self.wait(1.0)
        with audio.cue("wipe"):
            self.dust_wipe([title5, un5, asy5, axes5, curve5, xlab5, ylab5, bead5, note5], run_time=2.4)

        # 6. Example: Bernoulli distribution. (~12 s)
        title6 = self.txt("Example: Bernoulli samples", 30, pal.TEXT, BOLD)
        self.fit_width(title6, 7.8)
        title6.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title6.text)):
            self.type_in(title6, run_time=1.6)
        set6 = self.formula(r"\{x^{(1)},\dots,x^{(m)}\}\ \text{i.i.d.}", 36, pal.DISTRIBUTION)
        self.fit_width(set6, 7.2)
        set6.move_to(UP * 2.5)
        with audio.cue("draw"):
            self.play(Write(set6), run_time=1.6)
        bits = [1, 0, 1, 1, 0, 1, 0, 1]
        coins = VGroup()
        for b in bits:
            col = pal.OUTPUT if b else pal.ERROR
            c = Circle(radius=0.34, color=col, fill_color=col, fill_opacity=0.25, stroke_width=4)
            d = self.txt(str(b), 26, col).move_to(c)
            coins.add(VGroup(c, d))
        coins.arrange(RIGHT, buff=0.18).move_to(UP * 0.9)
        self.fit_width(coins, 7.6)
        with audio.cue("grow"):
            self.play(LaggedStart(*[GrowFromCenter(c) for c in coins], lag_ratio=0.12), run_time=2.0)
        dist6 = self.formula(r"x^{(i)}\sim\mathrm{Bernoulli}(\theta)", 38, pal.DISTRIBUTION).move_to(DOWN * 0.7)
        with audio.cue("draw"):
            self.play(Write(dist6), run_time=1.4)
        p6 = self.formula(r"P(x=1)=\theta", 34, pal.FORMULA).move_to(DOWN * 1.6)
        with audio.cue("draw"):
            self.play(Write(p6), run_time=1.2)
        note6 = self.txt("Each sample is 0 or 1,\nindependent and identically distributed.", 25, pal.TEXT)
        self.fit_width(note6, 7.6)
        note6.move_to(DOWN * 2.7)
        with audio.cue("type", glyphs=len(note6.text)):
            self.type_in(note6, run_time=1.8)
        self.wait(1.0)
        with audio.cue("wipe"):
            self.dust_wipe([title6, set6, coins, dist6, p6, note6], run_time=2.4)

        # 7. Closing thought and camera emphasis. (~10 s)
        final = self.txt("Estimates are random variables.\nBias is how far their average misses.", 30, pal.TEXT, BOLD)
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
    Page_122().render()
