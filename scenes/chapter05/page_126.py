"""Page 126 — Standard error, confidence intervals, and estimator variance.

Adapted from Page 125's horizontal text-strip animation and ASMRSync workflow.
Square 1:1 video, white background, black typography.
"""

from manim import *
import numpy as np
from pathlib import Path
from PIL import Image

from common.chapter5_style import Chapter5Scene
from common.asmr_sync import ASMRSync


PAGE_SRC = Path("assets/bookpage/page_126.png")
BAND_DIR = Path("assets/bookpage/page_126_bands")

WHITE_BG = "#FFFFFF"
BLACK = "#000000"
DARK_GRAY = "#404040"


def shrink(mob, width):
    """Shrink a mobject only when it exceeds the specified width."""
    if mob.width > width:
        mob.scale(width / mob.width)
    return mob


class ZoomFade(Animation):
    """Uniformly scale a mobject around a point while controlling opacity."""

    def __init__(
        self,
        mobject,
        point,
        s0,
        s1,
        a0=None,
        a1=None,
        **kwargs,
    ):
        self.point = np.array(point, dtype=float)
        self.s0 = s0
        self.s1 = s1
        self.a0 = a0
        self.a1 = a1
        self.cur = 1.0

        super().__init__(mobject, **kwargs)

    def interpolate_mobject(self, alpha):
        t = self.rate_func(alpha)

        scale = max(
            self.s0 + (self.s1 - self.s0) * t,
            1e-3,
        )

        self.mobject.scale(
            scale / self.cur,
            about_point=self.point,
        )
        self.cur = scale

        if self.a0 is not None and self.a1 is not None:
            opacity = self.a0 + (self.a1 - self.a0) * t
            self.mobject.set_opacity(
                max(0.0, min(1.0, opacity))
            )


def build_bands():
    """Split the original book page into horizontal text-line strips."""

    if not PAGE_SRC.exists():
        raise FileNotFoundError(
            f"Missing page image: {PAGE_SRC}"
        )

    image = Image.open(PAGE_SRC).convert("RGB")

    width, height = image.size

    # Match the small-margin crop used by Page 125.
    image = image.crop(
        (6, 6, width - 6, height - 6)
    )

    width, height = image.size
    arr = np.asarray(image)

    # Detect rows containing dark text or printed content.
    ink = (arr[:, 14:-14].min(axis=2) < 235).any(axis=1)

    ink[:3] = False
    ink[-6:] = False

    BAND_DIR.mkdir(parents=True, exist_ok=True)

    # Prevent stale strips from earlier renders.
    for old in BAND_DIR.glob("band_*.png"):
        old.unlink()

    bands = []
    y = 0

    while y < height:
        if not ink[y]:
            y += 1
            continue

        start = y

        while y < height and ink[y]:
            y += 1

        top = max(0, start - 2)
        bottom = min(height, y + 2)

        path = BAND_DIR / f"band_{len(bands):03d}.png"

        # Each strip retains the original pixels and white background.
        image.crop(
            (0, top, width, bottom)
        ).save(path)

        bands.append(
            (str(path), top, bottom)
        )

    if not bands:
        raise ValueError(
            "No text strips were detected in page_126.png."
        )

    print(f"Detected {len(bands)} horizontal page strips.")

    return width, height, bands


class Page_126(Chapter5Scene):

    HIGHLIGHT_BLUE = "#0066FF"
    HIGHLIGHT_GREEN = "#008000"
    HIGHLIGHT_RED = "#E53935"

    PAGE_NO = "126"
    RNG_SEED = 126

    # ---------------------------------------------------------
    # PAGE IMAGE
    # ---------------------------------------------------------

    def make_page(self, width, height, bands):
        """Reconstruct the original page without distorting its typography."""

        aspect = width / height

        page_height = min(
            config.frame_height - 1.3,
            (config.frame_width - 0.4) / aspect,
        )

        page_width = page_height * aspect
        scale = page_width / width

        center = np.array([0.0, 0.1, 0.0])

        paper = Rectangle(
            width=page_width,
            height=page_height,
            stroke_width=0,
            fill_color=WHITE_BG,
            fill_opacity=1,
        )

        paper.move_to(center)
        paper.set_z_index(0)

        page_top = center[1] + page_height / 2
        strips = []

        for path, top, bottom in bands:
            strip = ImageMobject(path)

            # Preserve the strip's aspect ratio.
            strip.scale_to_fit_width(page_width)

            strip.move_to(
                [
                    center[0],
                    page_top - ((top + bottom) / 2) * scale,
                    0,
                ]
            )

            strip.set_z_index(1)
            strips.append(strip)

        return paper, strips

    # ---------------------------------------------------------
    # PAGE-TEXT ANIMATION — ADAPTED FROM PAGE 125
    # ---------------------------------------------------------

    def zoom_out_text(self, strips, center):
        return LaggedStart(
            *[
                ZoomFade(
                    strip,
                    center,
                    1.0,
                    0.12,
                    1.0,
                    0.0,
                    rate_func=rush_into,
                    remover=True,
                    run_time=1.2,
                )
                for strip in strips
            ],
            lag_ratio=0.025,
        )

    def zoom_in_text(self, strips, center):
        return LaggedStart(
            *[
                ZoomFade(
                    strip,
                    center,
                    0.12,
                    1.0,
                    0.0,
                    1.0,
                    rate_func=smooth,
                    run_time=1.4,
                )
                for strip in strips
            ],
            lag_ratio=0.025,
        )

    # ---------------------------------------------------------
    # TEXT AND EQUATION HELPERS
    # ---------------------------------------------------------

    def heading(self, text):
        mob = self.txt(
            text,
            29,
            BLACK,
            BOLD,
        )

        self.fit_width(mob, 7.8)
        mob.to_edge(UP, buff=0.45)

        return mob

    def show_formula(self, audio, tex, y, size=36):
        mob = self.formula(
            tex,
            size,
            BLACK,
        )

        self.fit_width(mob, 7.4)
        mob.move_to([0, y, 0])

        with audio.cue("draw"):
            self.play(
                Write(mob),
                run_time=1.5,
            )

        return mob

    def clear_section(self, audio, items):
        """Fade out the current section before introducing the next one."""
        items = [item for item in items if item is not None]
        if not items:
            return

        with audio.cue("wipe"):
            self.play(
                *[FadeOut(item, shift=ORIGIN) for item in items],
                run_time=0.55,
                rate_func=smooth,
            )

    def construct(self):
        # Use the existing square canvas and white page style.
        self.camera.background_color = WHITE_BG
        config.background_color = WHITE_BG

        audio = ASMRSync(
            self,
            self.PAGE_NO,
        )

        width, height, band_info = build_bands()

        # =====================================================
        # OPENING — ORIGINAL BOOK PAGE
        # =====================================================

        paper, strips = self.make_page(
            width,
            height,
            band_info,
        )

        page_center = paper.get_center()

        with audio.cue("grow"):
            self.play(
                FadeIn(paper),
                *[
                    FadeIn(strip)
                    for strip in strips
                ],
                run_time=1.4,
            )

        self.wait(1.2)

        # The original text moves toward the center.
        # Individual strips preserve the page's typography.
        with audio.cue("zoom"):
            self.play(
                self.zoom_out_text(
                    strips,
                    page_center,
                )
            )

        self.wait(0.3)

        with audio.cue("wipe"):
            self.play(
                FadeOut(paper, shift=ORIGIN),
                run_time=0.55,
                rate_func=smooth,
            )

        # =====================================================
        # SECTION 1 — STANDARD ERROR
        # =====================================================

        h1 = self.heading(
            "Standard Error of the Mean"
        )

        with audio.cue(
            "type",
            glyphs=len(h1.text),
        ):
            self.type_in(
                h1,
                run_time=1.3,
            )

        eq1 = self.show_formula(
            audio,
            r"\mathrm{SE}(\hat{\mu}_m)=\frac{\sigma}{\sqrt{m}}",
            1.9,
            39,
        )

        # A simple visual showing the effect of sample size.
        axis = NumberLine(
            x_range=[0, 10, 1],
            length=5.8,
            include_numbers=False,
            color=BLACK,
            stroke_width=2,
        )

        axis.move_to(DOWN * 0.15)

        axis_label = self.txt(
            "Increasing sample size",
            22,
            BLACK,
        )

        axis_label.next_to(
            axis,
            UP,
            buff=0.35,
        )

        marker = Dot(
            axis.n2p(1),
            color=BLACK,
            radius=0.09,
        )

        with audio.cue("draw"):
            self.play(
                Create(axis),
                FadeIn(axis_label),
                FadeIn(marker),
                run_time=1.2,
            )

        for n in [2, 4, 7, 10]:
            target = Dot(
                axis.n2p(n),
                color=BLACK,
                radius=0.09,
            )

            with audio.cue("slide"):
                self.play(
                    Transform(marker, target),
                    run_time=0.65,
                )

        note1 = self.txt(
            "More samples reduce uncertainty in the sample mean.",
            20,
            BLACK,
        )

        self.fit_width(note1, 7.5)
        note1.move_to(DOWN * 2.45)

        with audio.cue(
            "type",
            glyphs=len(note1.text),
        ):
            self.type_in(
                note1,
                run_time=1.5,
            )

        self.wait(0.8)

        self.clear_section(
            audio,
            [
                h1,
                eq1,
                axis,
                axis_label,
                marker,
                note1,
            ],
        )

        # =====================================================
        # SECTION 2 — 95% CONFIDENCE INTERVAL
        # =====================================================

        h2 = self.heading(
            "The 95% Confidence Interval"
        )

        with audio.cue(
            "type",
            glyphs=len(h2.text),
        ):
            self.type_in(
                h2,
                run_time=1.3,
            )

        eq2 = self.show_formula(
            audio,
            r"\hat{\mu}_m\pm1.96\,\mathrm{SE}(\hat{\mu}_m)",
            1.9,
            34,
        )

        axis2 = NumberLine(
            x_range=[-3, 3, 1],
            length=6.0,
            include_numbers=False,
            color=BLACK,
            stroke_width=2,
        )

        axis2.move_to(UP * 0.15)

        center_dot = Dot(
            axis2.n2p(0),
            color=BLACK,
            radius=0.11,
        )

        left_point = axis2.n2p(-1.96)
        right_point = axis2.n2p(1.96)

        interval = Line(
            left_point,
            right_point,
            color=BLACK,
            stroke_width=6,
        )

        left_tick = Line(
            left_point + UP * 0.22,
            left_point + DOWN * 0.22,
            color=BLACK,
            stroke_width=2,
        )

        right_tick = Line(
            right_point + UP * 0.22,
            right_point + DOWN * 0.22,
            color=BLACK,
            stroke_width=2,
        )

        center_label = self.formula(
            r"\hat{\mu}_m",
            25,
            BLACK,
        )

        center_label.next_to(
            center_dot,
            UP,
            buff=0.2,
        )

        lower_label = self.txt(
            "Lower bound",
            18,
            BLACK,
        )

        lower_label.next_to(
            left_tick,
            DOWN,
            buff=0.25,
        )

        upper_label = self.txt(
            "Upper bound",
            18,
            BLACK,
        )

        upper_label.next_to(
            right_tick,
            DOWN,
            buff=0.25,
        )

        with audio.cue("draw"):
            self.play(
                Create(axis2),
                FadeIn(center_dot),
                Write(center_label),
                run_time=1.1,
            )

        with audio.cue(
            "slide",
            profile="transfer",
        ):
            self.play(
                Create(interval),
                Create(left_tick),
                Create(right_tick),
                FadeIn(lower_label),
                FadeIn(upper_label),
                run_time=1.4,
            )

        note2 = self.txt(
            "Estimate ± 1.96 × standard error",
            24,
            BLACK,
        )

        note2.move_to(DOWN * 1.5)

        note2b = self.txt(
            "The interval communicates uncertainty about the true mean.",
            19,
            DARK_GRAY,
        )

        self.fit_width(note2b, 7.6)
        note2b.move_to(DOWN * 2.45)

        with audio.cue(
            "type",
            glyphs=len(note2.text),
        ):
            self.type_in(
                note2,
                run_time=1.3,
            )

        with audio.cue(
            "type",
            glyphs=len(note2b.text),
        ):
            self.type_in(
                note2b,
                run_time=1.4,
            )

        self.wait(0.8)

        self.clear_section(
            audio,
            [
                h2,
                eq2,
                axis2,
                center_dot,
                interval,
                left_tick,
                right_tick,
                center_label,
                lower_label,
                upper_label,
                note2,
                note2b,
            ],
        )

        # =====================================================
        # SECTION 3 — BERNOULLI DISTRIBUTION
        # =====================================================

        h3 = self.heading(
            "Bernoulli Distribution"
        )

        with audio.cue(
            "type",
            glyphs=len(h3.text),
        ):
            self.type_in(
                h3,
                run_time=1.3,
            )

        eq3 = self.show_formula(
            audio,
            r"P(x;\theta)=\theta^{x}(1-\theta)^{1-x}",
            1.9,
            34,
        )

        zero_circle = Circle(
            radius=0.48,
            color=BLACK,
            stroke_width=3,
        )

        zero_circle.move_to(
            LEFT * 1.8 + UP * 0.15
        )

        one_circle = Circle(
            radius=0.48,
            color=BLACK,
            stroke_width=3,
        )

        one_circle.move_to(
            RIGHT * 1.8 + UP * 0.15
        )

        zero_text = self.txt(
            "0",
            34,
            self.HIGHLIGHT_RED,
        ).move_to(zero_circle)

        one_text = self.txt(
            "1",
            34,
            self.HIGHLIGHT_GREEN,
        ).move_to(one_circle)

        zero_label = self.txt(
            "Failure",
            20,
            BLACK,
        )

        zero_label.next_to(
            zero_circle,
            DOWN,
            buff=0.2,
        )

        one_label = self.txt(
            "Success",
            20,
            BLACK,
        )

        one_label.next_to(
            one_circle,
            DOWN,
            buff=0.2,
        )

        with audio.cue("grow", pan=-0.3):
            self.play(
                GrowFromCenter(zero_circle),
                Write(zero_text),
                FadeIn(zero_label),
                run_time=1.0,
            )

        with audio.cue("grow", pan=0.3):
            self.play(
                GrowFromCenter(one_circle),
                Write(one_text),
                FadeIn(one_label),
                run_time=1.0,
            )

        eq3b = self.show_formula(
            audio,
            r"P(x=1)=\theta,\qquad P(x=0)=1-\theta",
            -1.25,
            29,
        )

        self.wait(0.8)

        self.clear_section(
            audio,
            [
                h3,
                eq3,
                zero_circle,
                one_circle,
                zero_text,
                one_text,
                zero_label,
                one_label,
                eq3b,
            ],
        )

        # =====================================================
        # SECTION 4 — VARIANCE OF THE ESTIMATOR
        # =====================================================

        h4 = self.heading(
            "Variance of the Estimator"
        )

        with audio.cue(
            "type",
            glyphs=len(h4.text),
        ):
            self.type_in(
                h4,
                run_time=1.3,
            )

        eq4 = self.show_formula(
            audio,
            r"\mathrm{Var}(\hat{\theta}_m)="
            r"\mathrm{Var}\left("
            r"\frac{1}{m}\sum_{i=1}^{m}x^{(i)}"
            r"\right)",
            1.9,
            30,
        )

        rng = np.random.default_rng(
            self.RNG_SEED
        )

        outcomes = rng.binomial(
            1,
            0.6,
            12,
        )

        dots = VGroup()

        for i, outcome in enumerate(outcomes):
            x = -3.25 + i * 0.59

            dot = Dot(
                [x, 0.2, 0],
                radius=0.12,
                color=WHITE_BG if outcome == 0 else BLACK,
                stroke_color=BLACK,
                stroke_width=1.5,
            )

            dots.add(dot)

        sample_label = self.txt(
            "Independent Bernoulli samples",
            21,
            BLACK,
        )

        sample_label.move_to(
            UP * 0.85
        )

        with audio.cue("grow"):
            self.play(
                FadeIn(sample_label),
                LaggedStart(
                    *[
                        GrowFromCenter(dot)
                        for dot in dots
                    ],
                    lag_ratio=0.08,
                ),
                run_time=1.8,
            )

        successes = int(outcomes.sum())

        mean_eq = self.formula(
            rf"\hat{{\theta}}_m=\frac{{{successes}}}{{12}}"
            rf"={successes / 12:.2f}",
            34,
            BLACK,
        )
        mean_eq.set_color_by_tex(
            f"{successes / 12:.2f}",
            self.HIGHLIGHT_GREEN,
        )

        mean_eq.move_to(
            DOWN * 0.8
        )

        with audio.cue("draw"):
            self.play(
                Write(mean_eq),
                run_time=1.4,
            )

        variance_eq = self.show_formula(
            audio,
            r"\mathrm{Var}(\hat{\theta}_m)"
            r"=\frac{\theta(1-\theta)}{m}",
            -1.8,
            31,
        )

        note4 = self.txt(
            "More independent samples reduce estimator variance.",
            20,
            BLACK,
        )

        self.fit_width(note4, 7.5)
        note4.move_to(
            DOWN * 2.8
        )

        with audio.cue(
            "type",
            glyphs=len(note4.text),
        ):
            self.type_in(
                note4,
                run_time=1.4,
            )

        self.wait(1.0)

        self.clear_section(
            audio,
            [
                h4,
                eq4,
                dots,
                sample_label,
                mean_eq,
                variance_eq,
                note4,
            ],
        )

        # =====================================================
        # ENDING — ORIGINAL PAGE RETURNS
        # =====================================================

        paper2, strips2 = self.make_page(
            width,
            height,
            band_info,
        )

        page_center2 = paper2.get_center()

        with audio.cue("grow"):
            self.play(
                FadeIn(paper2),
                run_time=1.2,
            )

        with audio.cue(
            "type",
            glyphs=max(60, len(strips2) * 14),
        ):
            self.play(
                self.zoom_in_text(
                    strips2,
                    page_center2,
                )
            )

        self.wait(0.6)

        everything = [
            paper2,
            *strips2,
        ]

        with audio.cue("zoom"):
            self.play(
                *[
                    ZoomFade(
                        mob,
                        page_center2,
                        1.0,
                        1.04,
                        run_time=1.2,
                        rate_func=smooth,
                    )
                    for mob in everything
                ]
            )

            self.play(
                *[
                    ZoomFade(
                        mob,
                        page_center2,
                        1.0,
                        1 / 1.04,
                        run_time=1.2,
                        rate_func=smooth,
                    )
                    for mob in everything
                ]
            )

        self.wait(1.5)

        # Required by the audio post-processing pipeline.
        audio.finish()


if __name__ == "__main__":
    Page_126().render()
