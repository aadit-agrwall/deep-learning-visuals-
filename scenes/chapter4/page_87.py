from manim import *

# ============================================================
# CHAPTER 4 — PAGE 87
# Native 9:16 composition
# White background + Black + #0047AB only
# ============================================================

config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1440
config.pixel_height = 2560
config.frame_rate = 60


class Page_87(Scene):

    def construct(self):

        BG = "#FFFFFF"
        BLACK = "#000000"
        BLUE = "#0047AB"

        self.camera.background_color = BG

        # ----------------------------------------------------
        # Helpers
        # ----------------------------------------------------

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
                    run_time=0.55,
                )
            self.wait(0.3)

        def safe_math(expression, size=32, color=BLACK):
            # Every equation is passed as a complete LaTeX string.
            return MathTex(
                expression,
                font_size=size,
                color=color,
            )

        # ====================================================
        # SCENE 1 — SECOND DERIVATIVE TEST
        # ====================================================

        chapter = txt(
            "CHAPTER 4",
            24,
            BLUE,
            BOLD,
        )
        heading = txt(
            "Numerical Computation",
            39,
            BLACK,
            BOLD,
        )
        section = txt(
            "4.2  Second-Derivative Test",
            29,
            BLUE,
            BOLD,
        )

        chapter.to_edge(UP, buff=0.55)
        heading.next_to(
            chapter,
            DOWN,
            buff=0.25,
        )
        section.next_to(
            heading,
            DOWN,
            buff=0.35,
        )

        show(chapter, 0.45)
        show(heading, 0.7)
        show(section, 0.6)

        self.wait(0.9)
        clear_scene()

        # ====================================================
        # SCENE 2 — f'(x)=0 AND f''(x)
        # ====================================================

        title = txt(
            "At a critical point",
            31,
            BLACK,
            BOLD,
        )
        title.to_edge(
            UP,
            buff=0.65,
        )
        show(title, 0.65)

        critical = safe_math(
            r"f'(x)=0",
            40,
            BLUE,
        )
        critical.next_to(
            title,
            DOWN,
            buff=0.65,
        )
        show(critical, 0.8)

        self.wait(0.4)

        # Minimum
        minimum_box = RoundedRectangle(
            width=7.25,
            height=2.45,
            corner_radius=0.18,
            stroke_color=BLUE,
            stroke_width=3,
            fill_color=WHITE,
            fill_opacity=1,
        )

        min_label = txt(
            "LOCAL MINIMUM",
            25,
            BLACK,
            BOLD,
        )

        min_formula = safe_math(
            r"f''(x)>0",
            37,
            BLUE,
        )

        min_arrow = Arrow(
            start=DOWN * 0.15,
            end=DOWN * 0.65,
            color=BLUE,
            stroke_width=4,
            buff=0,
        )

        min_group = VGroup(
            minimum_box,
            min_label,
            min_formula,
        )

        min_label.move_to(
            minimum_box.get_top()
            + DOWN * 0.55
        )

        min_formula.move_to(
            minimum_box.get_center()
            + DOWN * 0.18
        )

        min_group.next_to(
            critical,
            DOWN,
            buff=0.65,
        )

        min_arrow.next_to(
            critical,
            DOWN,
            buff=0.15,
        )

        show(min_arrow, 0.45)
        self.play(
            Create(minimum_box),
            run_time=0.55,
        )
        show(min_label, 0.55)
        show(min_formula, 0.65)

        self.wait(0.5)

        # Maximum
        maximum_box = RoundedRectangle(
            width=7.25,
            height=2.45,
            corner_radius=0.18,
            stroke_color=BLACK,
            stroke_width=3,
            fill_color=WHITE,
            fill_opacity=1,
        )

        max_label = txt(
            "LOCAL MAXIMUM",
            25,
            BLACK,
            BOLD,
        )

        max_formula = safe_math(
            r"f''(x)<0",
            37,
            BLUE,
        )

        maximum_box.next_to(
            minimum_box,
            DOWN,
            buff=0.45,
        )

        max_label.move_to(
            maximum_box.get_top()
            + DOWN * 0.55
        )

        max_formula.move_to(
            maximum_box.get_center()
            + DOWN * 0.18
        )

        show(maximum_box, 0.55)
        show(max_label, 0.55)
        show(max_formula, 0.65)

        self.wait(0.5)

        # Inconclusive
        inconclusive = txt(
            "f''(x) = 0  →  test is inconclusive",
            25,
            BLACK,
        )

        inconclusive.next_to(
            maximum_box,
            DOWN,
            buff=0.45,
        )

        show(inconclusive, 0.7)

        self.wait(1.5)
        clear_scene()

        # ====================================================
        # SCENE 3 — HESSIAN EIGENVALUE TEST
        # ====================================================

        title = txt(
            "Multiple dimensions",
            31,
            BLACK,
            BOLD,
        )
        title.to_edge(
            UP,
            buff=0.65,
        )
        show(title, 0.65)

        critical = safe_math(
            r"\nabla_x f(x)=0",
            34,
            BLUE,
        )
        critical.next_to(
            title,
            DOWN,
            buff=0.55,
        )
        show(critical, 0.75)

        hessian = safe_math(
            r"H(f)(x)",
            42,
            BLUE,
        )
        hessian.next_to(
            critical,
            DOWN,
            buff=0.6,
        )
        show(hessian, 0.75)

        eigen_text = txt(
            "Examine the eigenvalues of the Hessian",
            25,
            BLACK,
            BOLD,
        )
        eigen_text.next_to(
            hessian,
            DOWN,
            buff=0.45,
        )
        show(eigen_text, 0.8)

        # Eigenvalue spectrum
        axis = NumberLine(
            x_range=[-3, 3, 1],
            length=7.1,
            color=BLACK,
            include_numbers=True,
            font_size=20,
        )
        axis.next_to(
            eigen_text,
            DOWN,
            buff=0.55,
        )

        zero = Dot(
            axis.n2p(0),
            radius=0.075,
            color=BLACK,
        )

        axis_label = txt(
            "eigenvalue λ",
            22,
            BLACK,
        )
        axis_label.next_to(
            axis,
            DOWN,
            buff=0.25,
        )

        show(axis, 0.8)
        self.play(
            FadeIn(zero),
            run_time=0.4,
        )
        show(axis_label, 0.55)

        # Three classification regions
        min_region = txt(
            "all λ > 0",
            25,
            BLUE,
            BOLD,
        )
        min_region.next_to(
            axis,
            DOWN,
            buff=0.85,
        )

        min_result = txt(
            "local minimum",
            27,
            BLACK,
            BOLD,
        )
        min_result.next_to(
            min_region,
            DOWN,
            buff=0.2,
        )

        max_region = txt(
            "all λ < 0",
            25,
            BLUE,
            BOLD,
        )
        max_result = txt(
            "local maximum",
            27,
            BLACK,
            BOLD,
        )

        saddle_region = txt(
            "mixed signs",
            25,
            BLUE,
            BOLD,
        )
        saddle_result = txt(
            "saddle point",
            27,
            BLACK,
            BOLD,
        )

        classification = VGroup(
            VGroup(min_region, min_result),
            VGroup(max_region, max_result),
            VGroup(saddle_region, saddle_result),
        )

        classification.arrange(
            DOWN,
            buff=0.35,
        )

        classification.next_to(
            axis_label,
            DOWN,
            buff=0.45,
        )

        show(min_region, 0.45)
        show(min_result, 0.5)
        show(max_region, 0.45)
        show(max_result, 0.5)
        show(saddle_region, 0.45)
        show(saddle_result, 0.5)

        self.wait(1.5)
        clear_scene()

        # ====================================================
        # SCENE 4 — THREE-DIRECTION HESSIAN CLASSIFICATION
        # ====================================================

        title = txt(
            "What the eigenvalues tell us",
            30,
            BLACK,
            BOLD,
        )
        title.to_edge(
            UP,
            buff=0.65,
        )
        show(title, 0.65)

        # Three compact diagrams
        def parabola_up():
            ax = Axes(
                x_range=[-2, 2, 1],
                y_range=[-1, 3, 1],
                x_length=2.45,
                y_length=2.05,
                axis_config={
                    "color": BLACK,
                    "stroke_width": 2,
                },
                tips=False,
            )

            curve = ax.plot(
                lambda x: x**2,
                x_range=[-1.45, 1.45],
                color=BLUE,
                stroke_width=4,
            )

            point = Dot(
                ax.c2p(0, 0),
                radius=0.075,
                color=BLACK,
            )

            return VGroup(ax, curve, point)

        def parabola_down():
            ax = Axes(
                x_range=[-2, 2, 1],
                y_range=[-3, 1, 1],
                x_length=2.45,
                y_length=2.05,
                axis_config={
                    "color": BLACK,
                    "stroke_width": 2,
                },
                tips=False,
            )

            curve = ax.plot(
                lambda x: -x**2,
                x_range=[-1.45, 1.45],
                color=BLUE,
                stroke_width=4,
            )

            point = Dot(
                ax.c2p(0, 0),
                radius=0.075,
                color=BLACK,
            )

            return VGroup(ax, curve, point)

        def saddle_curve():
            ax = Axes(
                x_range=[-2, 2, 1],
                y_range=[-2, 2, 1],
                x_length=2.45,
                y_length=2.05,
                axis_config={
                    "color": BLACK,
                    "stroke_width": 2,
                },
                tips=False,
            )

            curve = ax.plot(
                lambda x: x**3,
                x_range=[-1.2, 1.2],
                color=BLUE,
                stroke_width=4,
            )

            point = Dot(
                ax.c2p(0, 0),
                radius=0.075,
                color=BLACK,
            )

            return VGroup(ax, curve, point)

        min_graph = parabola_up()
        max_graph = parabola_down()
        saddle_graph = saddle_curve()

        graphs = VGroup(
            min_graph,
            max_graph,
            saddle_graph,
        )

        graphs.arrange(
            DOWN,
            buff=0.75,
        )

        fit_width = 7.4
        if graphs.width > fit_width:
            graphs.scale(
                fit_width / graphs.width
            )

        graphs.next_to(
            title,
            DOWN,
            buff=0.55,
        )

        labels = VGroup(
            txt("λ > 0  →  minimum", 24, BLACK, BOLD),
            txt("λ < 0  →  maximum", 24, BLACK, BOLD),
            txt("mixed λ  →  saddle", 24, BLACK, BOLD),
        )

        labels.arrange(
            DOWN,
            buff=0.35,
        )

        labels.next_to(
            graphs,
            DOWN,
            buff=0.4,
        )

        self.play(
            FadeIn(min_graph),
            run_time=0.7,
        )
        show(labels[0], 0.55)

        self.play(
            FadeIn(max_graph),
            run_time=0.7,
        )
        show(labels[1], 0.55)

        self.play(
            FadeIn(saddle_graph),
            run_time=0.7,
        )
        show(labels[2], 0.55)

        self.wait(1.5)
        clear_scene()

        # ====================================================
        # SCENE 5 — POOR CONDITIONING / UNEQUAL CURVATURE
        # ====================================================

        title = txt(
            "Poor conditioning",
            31,
            BLACK,
            BOLD,
        )
        title.to_edge(
            UP,
            buff=0.65,
        )
        show(title, 0.65)

        intro = txt(
            "Different directions can have very different curvature.",
            24,
            BLACK,
        )
        intro.next_to(
            title,
            DOWN,
            buff=0.4,
        )
        show(intro, 0.7)

        # Elliptical contour map
        center = ORIGIN + DOWN * 0.3

        ellipses = VGroup()

        for rx, ry in [
            (3.15, 1.25),
            (2.55, 0.95),
            (1.95, 0.68),
            (1.35, 0.43),
            (0.72, 0.23),
        ]:
            ellipse = Ellipse(
                width=rx * 2,
                height=ry * 2,
                color=BLUE,
                stroke_width=3,
            )
            ellipse.move_to(center)
            ellipses.add(ellipse)

        ellipses.scale(0.88)

        show(ellipses[0], 0.5)
        show(ellipses[1], 0.45)
        show(ellipses[2], 0.45)
        show(ellipses[3], 0.45)
        show(ellipses[4], 0.45)

        center_dot = Dot(
            center,
            radius=0.09,
            color=BLACK,
        )

        self.play(
            FadeIn(center_dot),
            run_time=0.4,
        )

        # Steep direction
        vertical_line = Line(
            center + UP * 1.45,
            center + DOWN * 1.45,
            color=BLACK,
            stroke_width=3,
        )

        # Flat direction
        horizontal_line = Line(
            center + LEFT * 3.1,
            center + RIGHT * 3.1,
            color=BLUE,
            stroke_width=3,
        )

        self.play(
            Create(vertical_line),
            run_time=0.6,
        )

        self.play(
            Create(horizontal_line),
            run_time=0.6,
        )

        steep_label = txt(
            "strong curvature",
            22,
            BLACK,
            BOLD,
        )
        steep_label.next_to(
            vertical_line,
            RIGHT,
            buff=0.25,
        )

        flat_label = txt(
            "weak curvature",
            22,
            BLUE,
            BOLD,
        )
        flat_label.next_to(
            horizontal_line,
            DOWN,
            buff=0.25,
        )

        show(steep_label, 0.6)
        show(flat_label, 0.6)

        conditioning = safe_math(
            r"\kappa(H)=\frac{|\lambda_{\max}|}{|\lambda_{\min}|}",
            31,
            BLUE,
        )
        conditioning.next_to(
            ellipses,
            DOWN,
            buff=0.65,
        )
        show(conditioning, 0.9)

        warning = txt(
            "Large condition number  →  gradient descent must use cautious steps",
            21,
            BLACK,
            BOLD,
        )
        warning.next_to(
            conditioning,
            DOWN,
            buff=0.4,
        )

        fit_width = 7.8
        if warning.width > fit_width:
            warning.scale(
                fit_width / warning.width
            )

        show(warning, 0.8)

        self.wait(1.6)
        clear_scene()

        # ====================================================
        # SCENE 6 — CONCEPTUAL SUMMARY
        # ====================================================

        title = txt(
            "Curvature guides optimization",
            30,
            BLACK,
            BOLD,
        )
        title.to_edge(
            UP,
            buff=0.7,
        )
        show(title, 0.7)

        point = safe_math(
            r"\nabla f(x)=0",
            35,
            BLUE,
        )
        point.next_to(
            title,
            DOWN,
            buff=0.6,
        )
        show(point, 0.7)

        hessian = safe_math(
            r"H(f)(x)",
            40,
            BLUE,
        )
        hessian.next_to(
            point,
            DOWN,
            buff=0.45,
        )
        show(hessian, 0.7)

        arrow1 = Arrow(
            point.get_bottom(),
            hessian.get_top(),
            color=BLACK,
            stroke_width=3,
            buff=0.1,
        )

        # Create rather than GrowArrow: compatible with installed Manim.
        self.play(
            Create(arrow1),
            run_time=0.5,
        )

        summary = VGroup(
            txt(
                "positive curvature",
                24,
                BLACK,
                BOLD,
            ),
            txt(
                "→ minimum",
                24,
                BLUE,
                BOLD,
            ),
            txt(
                "negative curvature",
                24,
                BLACK,
                BOLD,
            ),
            txt(
                "→ maximum",
                24,
                BLUE,
                BOLD,
            ),
            txt(
                "mixed curvature",
                24,
                BLACK,
                BOLD,
            ),
            txt(
                "→ saddle",
                24,
                BLUE,
                BOLD,
            ),
        )

        summary.arrange(
            DOWN,
            buff=0.28,
        )

        summary.next_to(
            hessian,
            DOWN,
            buff=0.65,
        )

        for item in summary:
            show(item, 0.45)
            self.wait(0.15)

        self.wait(1.5)
        clear_scene()

        # ====================================================
        # FINAL TAKEAWAY — NO CLEAR
        # ====================================================

        final = txt(
            "The Hessian reveals curvature in every direction.",
            27,
            BLACK,
            BOLD,
        )

        final.move_to(
            ORIGIN + UP * 0.15
        )

        if final.width > 7.8:
            final.scale(
                7.8 / final.width
            )

        self.play(
            Write(final),
            run_time=1.0,
        )

        self.wait(0.35)

        underline = Underline(
            final,
            color=BLUE,
            stroke_width=4,
            buff=0.18,
        )

        self.play(
            Create(underline),
            run_time=0.55,
        )

        self.wait(2.2)


if __name__ == "__main__":
    Page_87().render()
