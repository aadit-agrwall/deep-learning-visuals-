import numpy as np
from manim import *

from common.connectors import smart_arrow, connector_chain
from common.layouts import flow_row, flow_column, fit_in_frame
from common.animations import staggered_fade_in, emphasize_then_settle
from common.components import titled_box


# ================================================================
# PAGE 86 — CHAPTER 4: NUMERICAL COMPUTATION
# Native 9:16 composition
# Background: white
# Palette: black + rgb(0,71,171) blue only
# ================================================================

config.pixel_width = 1440
config.pixel_height = 2560
config.frame_width = 9
config.frame_height = 16


class Page_86(Scene):

    def construct(self):

        BG = "#FFFFFF"
        BLACK = "#000000"
        BLUE = "#0047AB"

        self.camera.background_color = BG

        # ------------------------------------------------------------
        # Helpers
        # ------------------------------------------------------------

        def txt(text, size=28, color=BLACK, weight=NORMAL):
            return Text(
                text,
                font="CMU Serif",
                font_size=size,
                color=color,
                weight=weight,
            )

        def show(obj, time=0.7):
            self.play(
                Write(obj),
                run_time=time,
            )

        def clear_scene():
            if self.mobjects:
                self.play(
                    *[
                        FadeOut(obj)
                        for obj in list(self.mobjects)
                    ],
                    run_time=0.5,
                )
            self.wait(0.3)

        # ============================================================
        # SCENE 1 — SECTION TITLE
        # ============================================================

        chapter = txt(
            "CHAPTER 4",
            27,
            BLUE,
            BOLD,
        )

        heading = txt(
            "Numerical Computation",
            40,
            BLACK,
            BOLD,
        )

        section = txt(
            "Beyond the Gradient",
            29,
            BLUE,
            BOLD,
        )

        chapter.to_edge(
            UP,
            buff=0.68,
        )

        heading.next_to(
            chapter,
            DOWN,
            buff=0.28,
        )

        section.next_to(
            heading,
            DOWN,
            buff=0.34,
        )

        fit_in_frame(
            VGroup(chapter, heading, section),
            margin=0.55,
        )

        show(chapter, 0.5)
        show(heading, 0.75)
        show(section, 0.6)

        self.wait(1.3)
        clear_scene()

        # ============================================================
        # SCENE 2 — DIRECTIONAL SECOND DERIVATIVE
        # ============================================================

        title = txt(
            "Second derivative in a direction",
            29,
            BLACK,
            BOLD,
        )

        title.to_edge(
            UP,
            buff=0.62,
        )

        fit_in_frame(title, margin=0.45)
        show(title, 0.8)

        vector = MathTex(
            r"\mathbf{d}^{\mathsf T}H\mathbf{d}",
            font_size=48,
            color=BLUE,
        )

        vector.move_to(
            UP * 1.65
        )

        show(vector, 0.9)

        condition = txt(
            "For a unit direction d, this measures\n"
            "the second derivative along that direction.",
            21,
            BLACK,
        )

        condition.next_to(
            vector,
            DOWN,
            buff=0.42,
        )

        fit_in_frame(condition, margin=0.5)
        show(condition, 0.85)

        # Direction vector diagram
        origin = ORIGIN + DOWN * 0.95

        horizontal = Arrow(
            origin + LEFT * 2.4,
            origin + RIGHT * 2.4,
            color=BLACK,
            stroke_width=3,
        )

        direction = Arrow(
            origin,
            origin + RIGHT * 1.55 + UP * 1.05,
            color=BLUE,
            stroke_width=6,
        )

        origin_dot = Dot(
            origin,
            radius=0.10,
            color=BLACK,
        )

        d_label = MathTex(
            r"\mathbf{d}",
            font_size=32,
            color=BLUE,
        )

        d_label.next_to(
            direction,
            UP,
            buff=0.12,
        )

        self.play(
            Create(horizontal),
            FadeIn(origin_dot),
            run_time=0.55,
        )

        self.play(
            Create(direction),
            run_time=0.75,
        )

        show(d_label, 0.5)

        eig_note = txt(
            "If d is an eigenvector of H,\n"
            "dᵀHd equals its corresponding eigenvalue.",
            19,
            BLACK,
        )

        eig_note.to_edge(
            DOWN,
            buff=0.62,
        )

        fit_in_frame(eig_note, margin=0.45)
        show(eig_note, 0.8)

        self.wait(1.6)
        clear_scene()

        # ============================================================
        # SCENE 3 — WEIGHTED EIGENVALUE VIEW
        # ============================================================

        title = txt(
            "Curvature depends on direction",
            29,
            BLACK,
            BOLD,
        )

        title.to_edge(
            UP,
            buff=0.62,
        )

        show(title, 0.8)

        eigenvalues = MathTex(
            r"\lambda_{\min}"
            r"\;\leq\;"
            r"\mathbf{d}^{\mathsf T}H\mathbf{d}"
            r"\;\leq\;"
            r"\lambda_{\max}",
            font_size=38,
            color=BLUE,
        )

        eigenvalues.move_to(
            UP * 1.65
        )

        fit_in_frame(eigenvalues, margin=0.45)
        show(eigenvalues, 0.9)

        explanation = txt(
            "Other directions behave like weighted combinations\n"
            "of the Hessian's eigenvalues.",
            20,
            BLACK,
        )

        explanation.next_to(
            eigenvalues,
            DOWN,
            buff=0.40,
        )

        fit_in_frame(explanation, margin=0.45)
        show(explanation, 0.8)

        # Eigenvalue number line
        line = NumberLine(
            x_range=[-3, 3, 1],
            length=6.6,
            include_numbers=True,
            font_size=18,
            color=BLACK,
        )

        line.move_to(
            DOWN * 0.45
        )

        self.play(
            Create(line),
            run_time=0.7,
        )

        min_dot = Dot(
            line.n2p(-2.1),
            radius=0.13,
            color=BLUE,
        )

        mid_dot = Dot(
            line.n2p(0.55),
            radius=0.13,
            color=BLUE,
        )

        max_dot = Dot(
            line.n2p(2.15),
            radius=0.13,
            color=BLUE,
        )

        min_label = MathTex(
            r"\lambda_{\min}",
            font_size=25,
            color=BLACK,
        )

        mid_label = MathTex(
            r"\mathbf{d}^{\mathsf T}H\mathbf{d}",
            font_size=25,
            color=BLUE,
        )

        max_label = MathTex(
            r"\lambda_{\max}",
            font_size=25,
            color=BLACK,
        )

        min_label.next_to(
            min_dot,
            DOWN,
            buff=0.20,
        )

        mid_label.next_to(
            mid_dot,
            UP,
            buff=0.20,
        )

        max_label.next_to(
            max_dot,
            DOWN,
            buff=0.20,
        )

        self.play(
            FadeIn(min_dot),
            FadeIn(mid_dot),
            FadeIn(max_dot),
            run_time=0.7,
        )

        show(min_label, 0.45)
        show(mid_label, 0.55)
        show(max_label, 0.45)

        result = txt(
            "The largest eigenvalue gives maximum curvature.\n"
            "The smallest gives minimum curvature.",
            19,
            BLACK,
        )

        result.to_edge(
            DOWN,
            buff=0.62,
        )

        fit_in_frame(result, margin=0.45)
        show(result, 0.8)

        self.wait(1.6)
        clear_scene()

        # ============================================================
        # SCENE 4 — SECOND-ORDER TAYLOR APPROXIMATION
        # ============================================================

        title = txt(
            "Second-order Taylor approximation",
            28,
            BLACK,
            BOLD,
        )

        title.to_edge(
            UP,
            buff=0.62,
        )

        fit_in_frame(title, margin=0.45)
        show(title, 0.8)

        intro = txt(
            "Around the current point x⁽⁰⁾, include both slope and curvature.",
            19,
            BLACK,
        )

        intro.next_to(
            title,
            DOWN,
            buff=0.32,
        )

        fit_in_frame(intro, margin=0.45)
        show(intro, 0.7)

        equation = MathTex(
            r"f(\mathbf{x}) \approx f(\mathbf{x}^{(0)})"
            r" + (\mathbf{x}-\mathbf{x}^{(0)})^{\mathsf{T}}\mathbf{g}"
            r" + \frac{1}{2}(\mathbf{x}-\mathbf{x}^{(0)})^{\mathsf{T}}"
            r"H(\mathbf{x}-\mathbf{x}^{(0)})",
            font_size=28,
            color=BLUE,
        )

        equation.move_to(
            UP * 0.55
        )

        fit_in_frame(
            equation,
            margin=0.48,
        )

        show(
            equation,
            1.15,
        )

        eqnum = txt(
            "(4.8)",
            19,
            BLACK,
        )

        eqnum.to_edge(
            RIGHT,
            buff=0.62,
        )

        eqnum.move_to(
            eqnum.get_center() + UP * 0.15
        )

        show(eqnum, 0.4)

        # Three-term decomposition
        terms = VGroup(
            MathTex(
                r"f(\mathbf{x}^{(0)})",
                font_size=29,
                color=BLACK,
            ),
            MathTex(
                r"(\mathbf{x}-\mathbf{x}^{(0)})^{\mathsf T}\mathbf{g}",
                font_size=27,
                color=BLUE,
            ),
            MathTex(
                r"\frac{1}{2}"
                r"(\mathbf{x}-\mathbf{x}^{(0)})^{\mathsf T}"
                r"H"
                r"(\mathbf{x}-\mathbf{x}^{(0)})",
                font_size=25,
                color=BLACK,
            ),
        )

        terms.arrange(
            DOWN,
            buff=0.42,
        )

        terms.move_to(
            DOWN * 1.45
        )

        fit_in_frame(
            terms,
            margin=0.55,
        )

        labels = VGroup(
            txt("original value", 17, BLACK),
            txt("gradient contribution", 17, BLUE),
            txt("curvature correction", 17, BLACK),
        )

        for label, term in zip(labels, terms):
            label.next_to(
                term,
                RIGHT,
                buff=0.28,
            )

        fit_in_frame(
            VGroup(terms, labels),
            margin=0.42,
        )

        self.play(
            Write(terms[0]),
            run_time=0.55,
        )

        show(labels[0], 0.45)

        self.play(
            Write(terms[1]),
            run_time=0.65,
        )

        show(labels[1], 0.45)

        self.play(
            Write(terms[2]),
            run_time=0.75,
        )

        show(labels[2], 0.45)

        self.wait(1.6)
        clear_scene()

        # ============================================================
        # SCENE 5 — SUBSTITUTING THE GRADIENT STEP
        # ============================================================

        title = txt(
            "Substitute the gradient-descent step",
            28,
            BLACK,
            BOLD,
        )

        title.to_edge(
            UP,
            buff=0.62,
        )

        show(title, 0.8)

        step = MathTex(
            r"\mathbf{x}"
            r"="
            r"\mathbf{x}^{(0)}-\epsilon\mathbf{g}",
            font_size=41,
            color=BLUE,
        )

        step.move_to(
            UP * 1.85
        )

        show(step, 0.8)

        arrow = Arrow(
            UP * 1.20,
            UP * 0.72,
            color=BLUE,
            stroke_width=5,
        )

        self.play(
            Create(arrow),
            run_time=0.55,
        )

        result = MathTex(
            r"f(\mathbf{x}^{(0)}-\epsilon\mathbf{g})"
            r" \approx "
            r"f(\mathbf{x}^{(0)})-\epsilon\mathbf{g}^{\mathsf{T}}\mathbf{g}"
            r"+\frac{1}{2}\epsilon^2\mathbf{g}^{\mathsf{T}}H\mathbf{g}",
            font_size=27,
            color=BLUE,
        )

        result.move_to(
            DOWN * 0.10
        )

        fit_in_frame(
            result,
            margin=0.50,
        )

        show(
            result,
            1.1,
        )

        eqnum = txt(
            "(4.9)",
            19,
            BLACK,
        )

        eqnum.to_edge(
            RIGHT,
            buff=0.60,
        )

        show(
            eqnum,
            0.4,
        )

        terms_title = txt(
            "Three contributions",
            21,
            BLACK,
            BOLD,
        )

        terms_title.to_edge(
            DOWN,
            buff=2.15,
        )

        show(
            terms_title,
            0.6,
        )

        contributions = VGroup(
            txt("1. original value", 18, BLACK),
            txt("2. improvement from the gradient", 18, BLUE),
            txt("3. curvature correction", 18, BLACK),
        )

        contributions.arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.22,
        )

        contributions.next_to(
            terms_title,
            DOWN,
            buff=0.25,
        )

        fit_in_frame(
            contributions,
            margin=0.50,
        )

        staggered_fade_in(
            self,
            list(contributions),
            run_time=1.0,
            lag_ratio=0.22,
        )

        self.wait(1.6)
        clear_scene()

        # ============================================================
        # SCENE 6 — OPTIMAL STEP SIZE
        # ============================================================

        title = txt(
            "Optimal step size from the quadratic approximation",
            25,
            BLACK,
            BOLD,
        )

        title.to_edge(
            UP,
            buff=0.60,
        )

        fit_in_frame(title, margin=0.42)
        show(title, 0.8)

        condition = MathTex(
            r"\mathbf{g}^{\mathsf T}H\mathbf{g}>0",
            font_size=38,
            color=BLUE,
        )

        condition.move_to(
            UP * 1.75
        )

        show(
            condition,
            0.75,
        )

        description = txt(
            "When curvature is positive, choose ε\n"
            "that minimizes the Taylor approximation.",
            20,
            BLACK,
        )

        description.next_to(
            condition,
            DOWN,
            buff=0.35,
        )

        fit_in_frame(description, margin=0.45)
        show(description, 0.8)

        optimal = MathTex(
            r"\epsilon^{*}"
            r"="
            r"\frac{\mathbf{g}^{\mathsf T}\mathbf{g}}"
            r"{\mathbf{g}^{\mathsf T}H\mathbf{g}}",
            font_size=46,
            color=BLUE,
        )

        optimal.move_to(
            DOWN * 0.35
        )

        fit_in_frame(
            optimal,
            margin=0.55,
        )

        show(
            optimal,
            1.0,
        )

        eqnum = txt(
            "(4.10)",
            19,
            BLACK,
        )

        eqnum.to_edge(
            RIGHT,
            buff=0.62,
        )

        show(
            eqnum,
            0.4,
        )

        # Visual fraction interpretation
        numerator = MathTex(
            r"\mathbf{g}^{\mathsf T}\mathbf{g}",
            font_size=28,
            color=BLACK,
        )

        denominator = MathTex(
            r"\mathbf{g}^{\mathsf T}H\mathbf{g}",
            font_size=28,
            color=BLUE,
        )

        num_label = txt(
            "gradient magnitude",
            17,
            BLACK,
        )

        den_label = txt(
            "curvature along gradient",
            17,
            BLUE,
        )

        numerator.move_to(
            DOWN * 1.65 + LEFT * 1.55
        )

        denominator.move_to(
            DOWN * 2.30 + LEFT * 1.55
        )

        num_label.next_to(
            numerator,
            RIGHT,
            buff=0.22,
        )

        den_label.next_to(
            denominator,
            RIGHT,
            buff=0.22,
        )

        fit_in_frame(
            VGroup(
                numerator,
                denominator,
                num_label,
                den_label,
            ),
            margin=0.48,
        )

        show(numerator, 0.55)
        show(num_label, 0.45)
        show(denominator, 0.55)
        show(den_label, 0.45)

        self.wait(1.6)
        clear_scene()

        # ============================================================
        # SCENE 7 — MAXIMUM EIGENVALUE LIMIT
        # ============================================================

        title = txt(
            "Eigenvalues control the learning-rate scale",
            27,
            BLACK,
            BOLD,
        )

        title.to_edge(
            UP,
            buff=0.62,
        )

        fit_in_frame(title, margin=0.45)
        show(title, 0.8)

        worst = txt(
            "Worst case:",
            23,
            BLACK,
            BOLD,
        )

        worst.move_to(
            UP * 1.75
        )

        show(
            worst,
            0.6,
        )

        alignment = MathTex(
            r"\mathbf{g}"
            r"\parallel"
            r"\mathbf{v}_{\max}",
            font_size=40,
            color=BLUE,
        )

        alignment.next_to(
            worst,
            DOWN,
            buff=0.32,
        )

        show(
            alignment,
            0.7,
        )

        lambda_eq = MathTex(
            r"\epsilon^{*}"
            r"="
            r"\frac{1}{\lambda_{\max}}",
            font_size=48,
            color=BLUE,
        )

        lambda_eq.move_to(
            DOWN * 0.20
        )

        show(
            lambda_eq,
            0.9,
        )

        # Visual reciprocal relation
        number_line = NumberLine(
            x_range=[0, 4, 1],
            length=6.0,
            include_numbers=True,
            font_size=18,
            color=BLACK,
        )

        number_line.move_to(
            DOWN * 1.35
        )

        self.play(
            Create(number_line),
            run_time=0.65,
        )

        lam_dot = Dot(
            number_line.n2p(3.0),
            radius=0.12,
            color=BLUE,
        )

        eps_dot = Dot(
            number_line.n2p(1.0 / 3.0),
            radius=0.12,
            color=BLUE,
        )

        lam_label = MathTex(
            r"\lambda_{\max}",
            font_size=28,
            color=BLUE,
        )

        eps_label = MathTex(
            r"\epsilon^{*}",
            font_size=28,
            color=BLUE,
        )

        lam_label.next_to(
            lam_dot,
            UP,
            buff=0.18,
        )

        eps_label.next_to(
            eps_dot,
            DOWN,
            buff=0.18,
        )

        self.play(
            FadeIn(lam_dot),
            FadeIn(eps_dot),
            run_time=0.6,
        )

        show(
            lam_label,
            0.45,
        )

        show(
            eps_label,
            0.45,
        )

        conclusion = txt(
            "Larger maximum curvature means a smaller safe step.",
            19,
            BLACK,
            BOLD,
        )

        conclusion.to_edge(
            DOWN,
            buff=0.62,
        )

        fit_in_frame(conclusion, margin=0.45)
        show(conclusion, 0.8)

        self.wait(1.6)
        clear_scene()

        # ============================================================
        # SCENE 8 — CRITICAL POINT CLASSIFICATION
        # ============================================================

        title = txt(
            "Second derivatives also classify critical points",
            26,
            BLACK,
            BOLD,
        )

        title.to_edge(
            UP,
            buff=0.62,
        )

        fit_in_frame(title, margin=0.42)
        show(title, 0.8)

        critical = MathTex(
            r"f'(x)=0",
            font_size=42,
            color=BLUE,
        )

        critical.move_to(
            UP * 1.75
        )

        show(
            critical,
            0.75,
        )

        description = txt(
            "At a critical point, the first derivative gives no direction.\n"
            "The second derivative supplies curvature information.",
            19,
            BLACK,
        )

        description.next_to(
            critical,
            DOWN,
            buff=0.35,
        )

        fit_in_frame(description, margin=0.42)
        show(description, 0.8)

        # Classification cards
        min_box = VGroup(
            RoundedRectangle(
                width=6.2,
                height=1.45,
                corner_radius=0.16,
                color=BLUE,
                stroke_width=3,
            ),
            MathTex(
                r"f''(x)>0",
                font_size=31,
                color=BLUE,
            ),
            txt(
                "local minimum",
                20,
                BLACK,
                BOLD,
            ),
        )

        max_box = VGroup(
            RoundedRectangle(
                width=6.2,
                height=1.45,
                corner_radius=0.16,
                color=BLACK,
                stroke_width=3,
            ),
            MathTex(
                r"f''(x)<0",
                font_size=31,
                color=BLUE,
            ),
            txt(
                "local maximum",
                20,
                BLACK,
                BOLD,
            ),
        )

        saddle_box = VGroup(
            RoundedRectangle(
                width=6.2,
                height=1.45,
                corner_radius=0.16,
                color=BLUE,
                stroke_width=3,
            ),
            MathTex(
                r"f''(x)=0",
                font_size=31,
                color=BLUE,
            ),
            txt(
                "second derivative alone is inconclusive",
                17,
                BLACK,
            ),
        )

        for box in [min_box, max_box, saddle_box]:
            box[1].move_to(
                box[0].get_center() + LEFT * 1.55
            )
            box[2].move_to(
                box[0].get_center() + RIGHT * 1.25
            )

        cards = VGroup(
            min_box,
            max_box,
            saddle_box,
        )

        cards.arrange(
            DOWN,
            buff=0.28,
        )

        cards.move_to(
            DOWN * 1.25
        )

        fit_in_frame(
            cards,
            margin=0.48,
        )

        staggered_fade_in(
            self,
            list(cards),
            run_time=1.25,
            lag_ratio=0.25,
        )

        self.wait(1.6)
        clear_scene()

        # ============================================================
        # FINAL TAKEAWAY
        # ============================================================

        final = txt(
            "The Hessian connects curvature,\n"
            "learning-rate scale, and critical-point behavior.",
            25,
            BLACK,
            BOLD,
        )

        final.move_to(
            ORIGIN + UP * 0.05
        )

        fit_in_frame(
            final,
            margin=0.58,
        )

        self.play(
            Write(final),
            run_time=1.15,
        )

        self.wait(0.45)

        line = Underline(
            final,
            color=BLUE,
            stroke_width=5,
            buff=0.20,
        )

        self.play(
            Create(line),
            run_time=0.55,
        )

        self.wait(2.4)


if __name__ == "__main__":
    Page_86().render()
