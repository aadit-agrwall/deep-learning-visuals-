from manim import *
import numpy as np

# ============================================================
# PAGE 90 — NEWTON'S METHOD
# ============================================================

config.background_color = WHITE
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 60


class Page_90(Scene):

    def construct(self):

        BLACK = "#000000"
        BLUE = "#0047AB"
        WHITE_BG = "#FFFFFF"

        self.camera.background_color = WHITE_BG

        # --------------------------------------------------------
        # Helpers
        # --------------------------------------------------------

        def body(text, size=21, color=BLACK):
            obj = Text(
                text,
                font="DejaVu Serif",
                font_size=size,
                color=color,
            )
            return obj

        def bold(text, size=30, color=BLACK):
            obj = Text(
                text,
                font="DejaVu Serif",
                font_size=size,
                color=color,
                weight=BOLD,
            )

            # Hard safety limit for portrait frame.
            if obj.width > 7.4:
                obj.scale_to_fit_width(7.4)

            return obj

        def formula(tex, size=32, color=BLACK):
            return MathTex(
                tex,
                font_size=size,
                color=color,
            )

        def fit_width(obj, width=7.25):
            if obj.width > width:
                obj.scale_to_fit_width(width)
            return obj

        def clear_scene():
            mobs = list(self.mobjects)
            if mobs:
                self.play(
                    *[FadeOut(mob) for mob in mobs],
                    run_time=0.45,
                )
            self.wait(0.2)

        # ========================================================
        # SCENE 1 — NEWTON'S METHOD
        # ========================================================

        title = bold(
            "Newton's method",
            38,
        )
        title.to_edge(UP, buff=0.75)

        self.play(
            Write(title),
            run_time=0.8,
        )

        intro = body(
            "The Hessian can guide the search toward a critical point.",
            19,
        )
        fit_width(intro)
        intro.next_to(title, DOWN, buff=0.35)

        self.play(
            Write(intro),
            run_time=0.7,
        )

        # --------------------------------------------------------
        # Function curve
        # --------------------------------------------------------

        axes = Axes(
            x_range=[-3.8, 3.8, 1],
            y_range=[-0.5, 5.0, 1],
            x_length=7.0,
            y_length=4.8,
            axis_config={
                "color": BLACK,
                "stroke_width": 1.6,
                "include_numbers": False,
            },
        )

        axes.move_to(DOWN * 1.0)

        curve = axes.plot(
            lambda x: 0.55 * x**2 + 0.18 * x + 0.5,
            x_range=[-3.0, 3.0],
            color=BLUE,
            stroke_width=4,
        )

        self.play(
            Create(axes),
            Create(curve),
            run_time=1.3,
        )

        # Starting point
        x0 = -2.7
        y0 = 0.55 * x0**2 + 0.18 * x0 + 0.5

        start = Dot(
            axes.c2p(x0, y0),
            radius=0.09,
            color=BLACK,
        )

        start_label = body(
            "current point",
            16,
            BLACK,
        )
        start_label.next_to(
            start,
            UP,
            buff=0.15,
        )

        self.play(
            FadeIn(start),
            Write(start_label),
            run_time=0.6,
        )

        # Newton jump
        minimum_x = -0.18
        minimum_y = 0.55 * minimum_x**2 + 0.18 * minimum_x + 0.5

        target = Dot(
            axes.c2p(minimum_x, minimum_y),
            radius=0.10,
            color=BLUE,
        )

        target_label = body(
            "critical point",
            16,
            BLUE,
        )
        target_label.next_to(
            target,
            DOWN,
            buff=0.18,
        )

        jump = Arrow(
            axes.c2p(x0, y0),
            axes.c2p(minimum_x, minimum_y),
            color=BLUE,
            stroke_width=4,
            buff=0.08,
        )

        self.play(
            Create(jump),
            run_time=0.8,
        )

        self.play(
            FadeIn(target),
            Write(target_label),
            run_time=0.6,
        )

        equation = formula(
            r"x^{*}=x^{(0)}-H(f)(x^{(0)})^{-1}\nabla_x f(x^{(0)})",
            29,
            BLUE,
        )

        fit_width(equation, 7.3)
        equation.to_edge(DOWN, buff=0.7)

        self.play(
            Write(equation),
            run_time=1.0,
        )

        self.wait(1.4)
        clear_scene()

        # ========================================================
        # SCENE 2 — SECOND ORDER INFORMATION
        # ========================================================

        title = bold(
            "First-order vs second-order optimization",
            29,
        )
        title.to_edge(UP, buff=0.7)

        self.play(
            Write(title),
            run_time=0.8,
        )

        # --------------------------------------------------------
        # FIRST ORDER
        # --------------------------------------------------------

        first_box = RoundedRectangle(
            width=7.0,
            height=2.25,
            corner_radius=0.18,
            color=BLACK,
            stroke_width=2.5,
        )
        first_box.move_to(UP * 2.25)

        first_title = bold(
            "First-order",
            24,
            BLACK,
        )
        first_title.move_to(
            first_box.get_center() + UP * 0.55
        )

        first_formula = formula(
            r"\nabla_x f(x)",
            31,
            BLUE,
        )
        first_formula.move_to(
            first_box.get_center() + DOWN * 0.15
        )

        first_desc = body(
            "Uses the gradient.",
            17,
            BLACK,
        )
        first_desc.move_to(
            first_box.get_center() + DOWN * 0.72
        )

        self.play(
            Create(first_box),
            Write(first_title),
            Write(first_formula),
            Write(first_desc),
            run_time=1.0,
        )

        # Arrow
        arrow1 = Arrow(
            first_box.get_bottom(),
            first_box.get_bottom() + DOWN * 0.55,
            color=BLUE,
            stroke_width=3,
            buff=0.05,
        )

        self.play(
            Create(arrow1),
            run_time=0.45,
        )

        # --------------------------------------------------------
        # SECOND ORDER
        # --------------------------------------------------------

        second_box = RoundedRectangle(
            width=7.0,
            height=2.55,
            corner_radius=0.18,
            color=BLUE,
            stroke_width=2.5,
        )
        second_box.move_to(DOWN * 0.35)

        second_title = bold(
            "Second-order",
            24,
            BLUE,
        )
        second_title.move_to(
            second_box.get_center() + UP * 0.75
        )

        second_formula = formula(
            r"\nabla_x f(x),\quad H(f)(x)",
            28,
            BLUE,
        )
        second_formula.move_to(
            second_box.get_center() + DOWN * 0.02
        )

        second_desc = body(
            "Uses gradient + Hessian curvature.",
            17,
            BLACK,
        )
        fit_width(second_desc, 6.4)
        second_desc.move_to(
            second_box.get_center() + DOWN * 0.78
        )

        self.play(
            Create(second_box),
            Write(second_title),
            Write(second_formula),
            Write(second_desc),
            run_time=1.0,
        )

        arrow2 = Arrow(
            second_box.get_bottom(),
            second_box.get_bottom() + DOWN * 0.55,
            color=BLUE,
            stroke_width=3,
            buff=0.05,
        )

        self.play(
            Create(arrow2),
            run_time=0.45,
        )

        # --------------------------------------------------------
        # RESULT BOX
        # --------------------------------------------------------

        result_box = RoundedRectangle(
            width=7.0,
            height=1.75,
            corner_radius=0.18,
            color=BLACK,
            stroke_width=2.5,
        )
        result_box.move_to(DOWN * 3.05)

        result_text = body(
            "Curvature can guide a more direct step.",
            18,
            BLACK,
        )
        fit_width(result_text, 6.2)
        result_text.move_to(
            result_box.get_center()
        )

        self.play(
            Create(result_box),
            Write(result_text),
            run_time=0.9,
        )

        self.wait(1.4)
        clear_scene()

        # ========================================================
        # SCENE 3 — NEWTON UPDATE
        # ========================================================

        title = bold(
            "Newton update",
            35,
        )
        title.to_edge(UP, buff=0.75)

        self.play(
            Write(title),
            run_time=0.8,
        )

        equation = formula(
            r"x^{*}=x^{(0)}-H(f)(x^{(0)})^{-1}\nabla_x f(x^{(0)})",
            29,
            BLUE,
        )

        fit_width(equation, 7.25)
        equation.next_to(
            title,
            DOWN,
            buff=0.75,
        )

        self.play(
            Write(equation),
            run_time=1.0,
        )

        explanation = body(
            "The inverse Hessian adjusts the step using local curvature.",
            19,
            BLACK,
        )

        fit_width(explanation, 7.2)
        explanation.next_to(
            equation,
            DOWN,
            buff=0.55,
        )

        self.play(
            Write(explanation),
            run_time=0.8,
        )

        # --------------------------------------------------------
        # Visual decomposition
        # --------------------------------------------------------

        grad_box = RoundedRectangle(
            width=6.8,
            height=1.55,
            corner_radius=0.16,
            color=BLACK,
            stroke_width=2.3,
        )
        grad_box.move_to(UP * 0.9)

        grad_text = body(
            "Gradient  →  search direction",
            19,
            BLACK,
        )
        fit_width(grad_text, 6.0)
        grad_text.move_to(
            grad_box.get_center()
        )

        self.play(
            Create(grad_box),
            Write(grad_text),
            run_time=0.8,
        )

        curvature_box = RoundedRectangle(
            width=6.8,
            height=1.55,
            corner_radius=0.16,
            color=BLUE,
            stroke_width=2.3,
        )
        curvature_box.move_to(DOWN * 1.05)

        curvature_text = body(
            "Hessian  →  curvature correction",
            19,
            BLUE,
        )
        fit_width(curvature_text, 6.0)
        curvature_text.move_to(
            curvature_box.get_center()
        )

        self.play(
            Create(curvature_box),
            Write(curvature_text),
            run_time=0.8,
        )

        result = bold(
            "Together → a curvature-aware step",
            22,
            BLUE,
        )
        fit_width(result, 7.0)
        result.to_edge(DOWN, buff=0.9)

        self.play(
            Write(result),
            run_time=0.8,
        )

        self.wait(1.4)
        clear_scene()

        # ========================================================
        # SCENE 4 — NEWTON VS GRADIENT DESCENT
        # ========================================================

        title = bold(
            "Why Newton's method can be faster",
            29,
        )
        title.to_edge(UP, buff=0.7)

        self.play(
            Write(title),
            run_time=0.8,
        )

        # --------------------------------------------------------
        # Gradient descent side
        # --------------------------------------------------------

        left_title = bold(
            "Gradient descent",
            23,
            BLACK,
        )
        left_title.move_to(
            LEFT * 2.25 + UP * 2.8
        )

        self.play(
            Write(left_title),
            run_time=0.6,
        )

        left_curve = Axes(
            x_range=[-2.5, 2.5, 1],
            y_range=[-0.2, 3.5, 1],
            x_length=3.0,
            y_length=3.1,
            axis_config={
                "color": BLACK,
                "stroke_width": 1.2,
                "include_ticks": False,
                "include_numbers": False,
            },
        )
        left_curve.move_to(
            LEFT * 2.25 + DOWN * 0.25
        )

        curve1 = left_curve.plot(
            lambda x: 0.55 * x**2 + 0.3,
            x_range=[-2.1, 2.1],
            color=BLUE,
            stroke_width=3,
        )

        self.play(
            Create(left_curve),
            Create(curve1),
            run_time=0.8,
        )

        left_steps = VGroup()

        xs = [-1.8, -1.0, -1.35, -0.55, -0.75, -0.20, -0.30, 0.0]

        for a, b in zip(xs[:-1], xs[1:]):
            ya = 0.55 * a**2 + 0.3
            yb = 0.55 * b**2 + 0.3

            left_steps.add(
                Line(
                    left_curve.c2p(a, ya),
                    left_curve.c2p(b, yb),
                    color=BLACK,
                    stroke_width=3,
                )
            )

        for segment in left_steps:
            self.play(
                Create(segment),
                run_time=0.18,
            )

        left_caption = body(
            "Repeated small steps",
            16,
            BLACK,
        )
        left_caption.next_to(
            left_curve,
            DOWN,
            buff=0.25,
        )

        self.play(
            Write(left_caption),
            run_time=0.5,
        )

        # --------------------------------------------------------
        # Newton side
        # --------------------------------------------------------

        right_title = bold(
            "Newton's method",
            23,
            BLUE,
        )
        right_title.move_to(
            RIGHT * 2.25 + UP * 2.8
        )

        self.play(
            Write(right_title),
            run_time=0.6,
        )

        right_curve = Axes(
            x_range=[-2.5, 2.5, 1],
            y_range=[-0.2, 3.5, 1],
            x_length=3.0,
            y_length=3.1,
            axis_config={
                "color": BLACK,
                "stroke_width": 1.2,
                "include_ticks": False,
                "include_numbers": False,
            },
        )
        right_curve.move_to(
            RIGHT * 2.25 + DOWN * 0.25
        )

        curve2 = right_curve.plot(
            lambda x: 0.55 * x**2 + 0.3,
            x_range=[-2.1, 2.1],
            color=BLUE,
            stroke_width=3,
        )

        self.play(
            Create(right_curve),
            Create(curve2),
            run_time=0.8,
        )

        newton_arrow = Arrow(
            right_curve.c2p(-1.8, 0.55 * (-1.8)**2 + 0.3),
            right_curve.c2p(0, 0.3),
            color=BLUE,
            stroke_width=4,
            buff=0.05,
        )

        self.play(
            Create(newton_arrow),
            run_time=0.9,
        )

        minimum = Dot(
            right_curve.c2p(0, 0.3),
            radius=0.09,
            color=BLUE,
        )

        self.play(
            FadeIn(minimum),
            run_time=0.4,
        )

        right_caption = body(
            "Curvature-aware jump",
            16,
            BLUE,
        )
        right_caption.next_to(
            right_curve,
            DOWN,
            buff=0.25,
        )

        self.play(
            Write(right_caption),
            run_time=0.5,
        )

        self.wait(1.4)
        clear_scene()

        # ========================================================
        # SCENE 5 — LIPSCHITZ CONTINUITY
        # ========================================================

        title = bold(
            "Lipschitz continuity",
            34,
        )
        title.to_edge(UP, buff=0.75)

        self.play(
            Write(title),
            run_time=0.8,
        )

        intro = body(
            "A Lipschitz condition bounds how rapidly a function can change.",
            19,
            BLACK,
        )
        fit_width(intro, 7.2)
        intro.next_to(
            title,
            DOWN,
            buff=0.35,
        )

        self.play(
            Write(intro),
            run_time=0.8,
        )

        lipschitz = formula(
            r"\forall x,y,\quad |f(x)-f(y)|\leq \mathcal{L}\|x-y\|_2",
            30,
            BLUE,
        )
        fit_width(lipschitz, 7.3)
        lipschitz.next_to(
            intro,
            DOWN,
            buff=0.65,
        )

        self.play(
            Write(lipschitz),
            run_time=1.0,
        )

        # --------------------------------------------------------
        # Input change
        # --------------------------------------------------------

        input_box = RoundedRectangle(
            width=6.9,
            height=1.55,
            corner_radius=0.16,
            color=BLACK,
            stroke_width=2.3,
        )
        input_box.move_to(UP * 0.8)

        input_text = body(
            "Small change in input",
            20,
            BLACK,
        )
        input_text.move_to(
            input_box.get_center()
        )

        self.play(
            Create(input_box),
            Write(input_text),
            run_time=0.8,
        )

        arrow = Arrow(
            input_box.get_bottom(),
            input_box.get_bottom() + DOWN * 0.55,
            color=BLUE,
            stroke_width=3,
            buff=0.04,
        )

        self.play(
            Create(arrow),
            run_time=0.45,
        )

        output_box = RoundedRectangle(
            width=6.9,
            height=1.55,
            corner_radius=0.16,
            color=BLUE,
            stroke_width=2.3,
        )
        output_box.move_to(DOWN * 1.0)

        output_text = body(
            "Bounded change in output",
            20,
            BLUE,
        )
        output_text.move_to(
            output_box.get_center()
        )

        self.play(
            Create(output_box),
            Write(output_text),
            run_time=0.8,
        )

        final = bold(
            "The constant 𝓛 controls the bound.",
            21,
            BLACK,
        )
        fit_width(final, 7.0)
        final.to_edge(DOWN, buff=0.9)

        self.play(
            Write(final),
            run_time=0.8,
        )

        self.wait(2.0)


if __name__ == "__main__":
    Page_90().render()
