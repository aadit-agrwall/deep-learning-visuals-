"""Page 123 - Bernoulli estimator is unbiased (5.21-5.28), Gaussian sample mean
(5.29, 5.30). Sound design: ASMRSync cues only (SFX, no background music)."""

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


class Page_123(Chapter5Scene):
    PAGE_NO = "123"
    RNG_SEED = 123

    def construct(self):
        self.init_page()
        audio = ASMRSync(self, self.PAGE_NO)

        # 1. Bernoulli distribution (5.21). (~13 s)
        title1 = self.txt("Example: Bernoulli distribution", 29, pal.TEXT, BOLD)
        self.fit_width(title1, 7.8)
        title1.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title1.text)):
            self.type_in(title1, run_time=1.6)
        eq1 = self.formula(r"P(x^{(i)};\theta)=\theta^{x^{(i)}}(1-\theta)^{(1-x^{(i)})}", 36, pal.FORMULA)
        self.fit_width(eq1, 7.2)
        eq1.move_to(UP * 2.4)
        num1 = self.txt("(5.21)", 22, pal.TEXT_DIM).next_to(eq1, DOWN, buff=0.2)
        with audio.cue("draw"):
            self.play(Write(eq1), FadeIn(num1), run_time=2.0)
        floor1 = Line(LEFT * 3.0, RIGHT * 3.0, color=pal.TEXT_DIM, stroke_width=2).move_to(DOWN * 1.0)
        bar0 = Rectangle(width=1.4, height=1.2, color=pal.ERROR, fill_color=pal.ERROR,
                         fill_opacity=0.3).move_to([-1.5, -1.0 + 0.6, 0])
        bar1 = Rectangle(width=1.4, height=1.8, color=pal.OUTPUT, fill_color=pal.OUTPUT,
                         fill_opacity=0.3).move_to([1.5, -1.0 + 0.9, 0])
        x0 = self.formula(r"x=0", 28, pal.TEXT).move_to([-1.5, -1.4, 0])
        x1 = self.formula(r"x=1", 28, pal.TEXT).move_to([1.5, -1.4, 0])
        p0 = self.formula(r"1-\theta", 30, pal.ERROR).move_to(bar0)
        p1 = self.formula(r"\theta", 32, pal.OUTPUT).move_to(bar1)
        with audio.cue("grow", pan=-0.3):
            self.play(Create(floor1), GrowFromEdge(bar0, DOWN), FadeIn(x0), FadeIn(p0),
                      run_time=1.6, rate_func=smooth)
        with audio.cue("grow", pan=0.3):
            self.play(GrowFromEdge(bar1, DOWN), FadeIn(x1), FadeIn(p1),
                      run_time=1.6, rate_func=smooth)
        note1 = self.txt("Each sample is 0 or 1;\nthe mean of the distribution is theta.", 26, pal.TEXT)
        self.fit_width(note1, 7.6)
        note1.move_to(DOWN * 2.7)
        with audio.cue("type", glyphs=len(note1.text)):
            self.type_in(note1, run_time=1.8)
        self.wait(1.0)
        with audio.cue("wipe"):
            self.dust_wipe([title1, eq1, num1, floor1, bar0, bar1, x0, x1, p0, p1, note1], run_time=2.4)

        # 2. The estimator: mean of the training samples (5.22). (~12 s)
        title2 = self.txt("A common estimator: the mean", 30, pal.TEXT, BOLD)
        self.fit_width(title2, 7.8)
        title2.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title2.text)):
            self.type_in(title2, run_time=1.6)
        bits = [1, 0, 1, 1, 0, 1, 0, 1]
        coins = VGroup()
        for b in bits:
            col = pal.OUTPUT if b else pal.ERROR
            c = Circle(radius=0.34, color=col, fill_color=col, fill_opacity=0.25, stroke_width=4)
            coins.add(VGroup(c, self.txt(str(b), 26, col).move_to(c)))
        coins.arrange(RIGHT, buff=0.18).move_to(UP * 2.0)
        self.fit_width(coins, 7.6)
        with audio.cue("grow"):
            self.play(LaggedStart(*[GrowFromCenter(c) for c in coins], lag_ratio=0.12), run_time=1.8)
        eq2 = self.formula(r"\hat{\theta}_m=\frac{1}{m}\sum_{i=1}^{m}x^{(i)}", 40, pal.FORMULA)
        self.fit_width(eq2, 6.4)
        eq2.move_to(UP * 0.3)
        num2 = self.txt("(5.22)", 22, pal.TEXT_DIM).next_to(eq2, DOWN, buff=0.2)
        with audio.cue("draw"):
            self.play(Write(eq2), FadeIn(num2), run_time=2.0)
        val2 = self.formula(r"\hat{\theta}_m=\frac{5}{8}=0.625", 36, pal.OUTPUT).move_to(DOWN * 1.4)
        with audio.cue("settle"):
            self.play(Write(val2), run_time=1.4)
        note2 = self.txt("Average the training samples.", 26, pal.TEXT).move_to(DOWN * 2.8)
        with audio.cue("type", glyphs=len(note2.text)):
            self.type_in(note2, run_time=1.4)
        self.wait(1.0)
        with audio.cue("wipe"):
            self.dust_wipe([title2, coins, eq2, num2, val2, note2], run_time=2.4)

        # 3. Is it biased? Part 1: 5.23 - 5.25. (~15 s)
        title3 = self.txt("Is it biased? Substitute", 30, pal.TEXT, BOLD)
        self.fit_width(title3, 7.8)
        title3.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title3.text)):
            self.type_in(title3, run_time=1.6)
        rows3 = [
            (r"\mathrm{bias}(\hat{\theta}_m)=\mathbb{E}[\hat{\theta}_m]-\theta", "(5.23)"),
            (r"=\mathbb{E}\left[\frac{1}{m}\sum_{i=1}^{m}x^{(i)}\right]-\theta", "(5.24)"),
            (r"=\frac{1}{m}\sum_{i=1}^{m}\mathbb{E}\left[x^{(i)}\right]-\theta", "(5.25)"),
        ]
        ys3 = [1.9, 0.4, -1.1]
        objs3 = []
        for (tex, tag), y in zip(rows3, ys3):
            f = self.formula(tex, 34, pal.FORMULA)
            shrink(f, 6.4)
            f.move_to([-0.3, y, 0])
            t = self.txt(tag, 22, pal.TEXT_DIM).move_to([3.5, y, 0])
            objs3.append(VGroup(f, t))
            with audio.cue("draw"):
                self.play(Write(f), FadeIn(t), run_time=2.0)
        hl3 = SurroundingRectangle(objs3[2][0], color=pal.OUTPUT, buff=0.15)
        with audio.cue("settle"):
            self.play(Create(hl3), run_time=0.8)
        note3 = self.txt("Expectation is linear:\nit moves inside the sum.", 26, pal.TEXT)
        self.fit_width(note3, 7.6)
        note3.move_to(DOWN * 2.6)
        with audio.cue("type", glyphs=len(note3.text)):
            self.type_in(note3, run_time=1.6)
        self.wait(1.0)
        with audio.cue("wipe"):
            self.dust_wipe([title3, *objs3, hl3, note3], run_time=2.4)

        # 4. Part 2: 5.26 - 5.28. (~16 s)
        title4 = self.txt("Evaluate the expectation", 30, pal.TEXT, BOLD)
        self.fit_width(title4, 7.8)
        title4.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title4.text)):
            self.type_in(title4, run_time=1.6)
        rows4 = [
            (r"=\frac{1}{m}\sum_{i=1}^{m}\sum_{x^{(i)}=0}^{1}\left(x^{(i)}\theta^{x^{(i)}}(1-\theta)^{(1-x^{(i)})}\right)-\theta", "(5.26)", 28),
            (r"=\frac{1}{m}\sum_{i=1}^{m}(\theta)-\theta", "(5.27)", 34),
            (r"=\theta-\theta=0", "(5.28)", 38),
        ]
        ys4 = [1.8, 0.2, -1.3]
        objs4 = []
        for (tex, tag, size), y in zip(rows4, ys4):
            col = pal.OUTPUT if tag == "(5.28)" else pal.FORMULA
            f = self.formula(tex, size, col)
            shrink(f, 6.5)
            f.move_to([-0.3, y, 0])
            t = self.txt(tag, 22, pal.TEXT_DIM).move_to([3.55, y, 0])
            objs4.append(VGroup(f, t))
            with audio.cue("draw"):
                self.play(Write(f), FadeIn(t), run_time=2.2)
        box4 = SurroundingRectangle(objs4[2][0], color=pal.OUTPUT, buff=0.18)
        with audio.cue("settle"):
            self.play(Create(box4), run_time=0.9)
        note4 = self.txt("The sum over x = 0, 1 of x times P(x)\nis exactly theta.", 25, pal.TEXT)
        self.fit_width(note4, 7.7)
        note4.move_to(DOWN * 2.7)
        with audio.cue("type", glyphs=len(note4.text)):
            self.type_in(note4, run_time=1.8)
        self.wait(1.0)
        with audio.cue("wipe"):
            self.dust_wipe([title4, *objs4, box4, note4], run_time=2.4)

        # 5. The estimator is unbiased. (~10 s)
        title5 = self.txt("The estimator is unbiased", 30, pal.TEXT, BOLD)
        self.fit_width(title5, 7.8)
        title5.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title5.text)):
            self.type_in(title5, run_time=1.6)
        line5 = NumberLine(x_range=[-1, 1, 0.5], length=5.6, include_numbers=False,
                           color=pal.TEXT_DIM, stroke_width=2).move_to(UP * 0.9)
        zero5 = Line(line5.n2p(0) + UP * 0.3, line5.n2p(0) + DOWN * 0.3, color=pal.OUTPUT, stroke_width=5)
        zlab5 = self.formula(r"0", 30, pal.OUTPUT).next_to(zero5, DOWN, buff=0.12)
        with audio.cue("draw"):
            self.play(Create(line5), Create(zero5), FadeIn(zlab5), run_time=1.2)
        dot5 = Dot(line5.n2p(0.8), radius=0.13, color=pal.ERROR)
        blab5 = self.txt("bias", 24, pal.ERROR).next_to(dot5, UP, buff=0.15)
        with audio.cue("grow"):
            self.play(FadeIn(dot5, scale=0.4), FadeIn(blab5), run_time=0.9)
        with audio.cue("slide", profile="converge"):
            self.play(dot5.animate.move_to(line5.n2p(0)), blab5.animate.next_to(line5.n2p(0), UP, buff=0.45),
                      run_time=2.6, rate_func=smooth)
        with audio.cue("settle"):
            self.play(dot5.animate.set_color(pal.OUTPUT), run_time=0.8)
        res5 = self.formula(r"\mathrm{bias}(\hat{\theta})=0\ \Rightarrow\ \hat{\theta}\ \text{is unbiased}", 34, pal.OUTPUT)
        self.fit_width(res5, 7.4)
        res5.move_to(DOWN * 1.2)
        with audio.cue("draw"):
            self.play(Write(res5), run_time=1.6)
        self.wait(1.2)
        with audio.cue("wipe"):
            self.dust_wipe([title5, line5, zero5, zlab5, dot5, blab5, res5], run_time=2.4)

        # 6. Gaussian density (5.29). (~13 s)
        title6 = self.txt("Example: Gaussian mean", 30, pal.TEXT, BOLD)
        self.fit_width(title6, 7.8)
        title6.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title6.text)):
            self.type_in(title6, run_time=1.6)
        axes6 = Axes(x_range=[-3.5, 3.5, 1], y_range=[0, 0.5, 0.1], x_length=5.4, y_length=2.2,
                     axis_config={"color": pal.TEXT_DIM, "include_tip": False,
                                  "stroke_width": 1.5}).move_to(UP * 1.5)
        pdf = lambda t: float(np.exp(-0.5 * t * t) / np.sqrt(2 * np.pi))
        curve6 = axes6.plot(pdf, x_range=[-3.3, 3.3], color=pal.DISTRIBUTION, stroke_width=5)
        mu6 = DashedLine(axes6.c2p(0, 0), axes6.c2p(0, pdf(0)), color=pal.FORMULA, stroke_width=4)
        mulab6 = self.formula(r"\mu", 32, pal.FORMULA).next_to(axes6.c2p(0, 0), DOWN, buff=0.15)
        with audio.cue("draw"):
            self.play(Create(axes6), Create(curve6), run_time=1.8)
        with audio.cue("grow"):
            self.play(Create(mu6), FadeIn(mulab6), run_time=1.0)
        eq6 = self.formula(r"p(x^{(i)};\mu,\sigma^2)=\frac{1}{\sqrt{2\pi\sigma^2}}\exp\left(-\frac{1}{2}\frac{(x^{(i)}-\mu)^2}{\sigma^2}\right)",
                           30, pal.FORMULA)
        self.fit_width(eq6, 7.5)
        eq6.move_to(DOWN * 1.1)
        num6 = self.txt("(5.29)", 22, pal.TEXT_DIM).next_to(eq6, DOWN, buff=0.2)
        with audio.cue("draw"):
            self.play(Write(eq6), FadeIn(num6), run_time=2.4)
        note6 = self.txt("Samples are i.i.d. N(x; mu, sigma squared).", 25, pal.TEXT)
        self.fit_width(note6, 7.7)
        note6.move_to(DOWN * 2.7)
        with audio.cue("type", glyphs=len(note6.text)):
            self.type_in(note6, run_time=1.6)
        self.wait(1.0)
        with audio.cue("wipe"):
            self.dust_wipe([title6, axes6, curve6, mu6, mulab6, eq6, num6, note6], run_time=2.4)

        # 7. The sample mean (5.30). (~13 s)
        title7 = self.txt("The sample mean", 31, pal.TEXT, BOLD)
        title7.to_edge(UP, buff=0.6)
        with audio.cue("type", glyphs=len(title7.text)):
            self.type_in(title7, run_time=1.6)
        line7 = NumberLine(x_range=[-3, 3, 1], length=6.0, include_numbers=False,
                           color=pal.TEXT_DIM, stroke_width=2).move_to(UP * 1.3)
        samples = [-1.4, -0.6, 0.3, 0.9, 1.6, -0.2, 0.7]
        dots7 = VGroup(*[Dot(line7.n2p(s), radius=0.11, color=pal.INPUT) for s in samples])
        with audio.cue("grow"):
            self.play(Create(line7), LaggedStart(*[FadeIn(d, scale=0.5) for d in dots7], lag_ratio=0.15),
                      run_time=2.0)
        mean7 = float(np.mean(samples))
        mark7 = Triangle(color=pal.FORMULA, fill_color=pal.FORMULA, fill_opacity=1).scale(0.17)
        mark7.move_to(line7.n2p(-2.6) + DOWN * 0.4)
        mlab7 = self.formula(r"\hat{\mu}_m", 32, pal.FORMULA).next_to(mark7, DOWN, buff=0.1)
        self.add(mark7, mlab7)
        dx7 = line7.n2p(mean7)[0] - line7.n2p(-2.6)[0]
        with audio.cue("slide", profile="converge"):
            self.play(mark7.animate.shift(RIGHT * dx7), mlab7.animate.shift(RIGHT * dx7),
                      run_time=2.6, rate_func=smooth)
        eq7 = self.formula(r"\hat{\mu}_m=\frac{1}{m}\sum_{i=1}^{m}x^{(i)}", 40, pal.FORMULA)
        self.fit_width(eq7, 6.4)
        eq7.move_to(DOWN * 0.6)
        num7 = self.txt("(5.30)", 22, pal.TEXT_DIM).next_to(eq7, DOWN, buff=0.2)
        with audio.cue("draw"):
            self.play(Write(eq7), FadeIn(num7), run_time=1.8)
        note7 = self.txt("A common estimator of the Gaussian mean\nis known as the sample mean.", 25, pal.TEXT)
        self.fit_width(note7, 7.7)
        note7.move_to(DOWN * 2.6)
        with audio.cue("type", glyphs=len(note7.text)):
            self.type_in(note7, run_time=1.8)
        self.wait(1.0)
        with audio.cue("wipe"):
            self.dust_wipe([title7, line7, dots7, mark7, mlab7, eq7, num7, note7], run_time=2.4)

        # 8. Closing thought and camera emphasis. (~10 s)
        final = self.txt("The Bernoulli sample mean is unbiased:\nits expectation is exactly theta.", 29, pal.TEXT, BOLD)
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
    Page_123().render()
