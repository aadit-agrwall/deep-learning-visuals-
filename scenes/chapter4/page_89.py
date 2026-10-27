from manim import *
import numpy as np

# ============================================================
# PAGE 89
# Native 9:16 portrait composition
# White background
# Black + blue only
# ============================================================

config.background_color = "#FFFFFF"
config.frame_width = 9
config.frame_height = 16
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 60


class Page_89(Scene):

    def construct(self):

        BLACK = "#000000"
        BLUE = "#0047AB"
        WHITE = "#FFFFFF"

        self.camera.background_color = WHITE

        # ========================================================
        # TYPOGRAPHY
        # ========================================================

        # Body/book text — NOT bold.
        def txt(text, size=23, color=BLACK):
            return Text(
                text,
                font="DejaVu Serif",
                font_size=size,
                color=color,
            )

        # Headings — bold only.
        def heading(text, size=32, color=BLACK):
            obj = Text(
                text,
                font="DejaVu Serif",
                font_size=size,
                color=color,
                weight=BOLD,
            )

            # Never allow a heading to leave the portrait frame.
            if obj.width > 7.7:
                obj.scale_to_fit_width(7.7)

            return obj

        def math(tex, size=30, color=BLACK):
            return MathTex(
                tex,
                font_size=size,
                color=color,
            )

        def show(obj, time=0.7):
            self.play(
                Write(obj),
                run_time=time,
            )

        def clear_scene():
            mobs = list(self.mobjects)
            if mobs:
                self.play(
                    *[FadeOut(mob) for mob in mobs],
                    run_time=0.45,
                )
            self.wait(0.25)

        # ========================================================
        # SCENE 1 — INTRODUCTION
        # ========================================================

        chapter = txt(
            "CHAPTER 4.  NUMERICAL COMPUTATION",
            19,
            BLACK,
        )
        chapter.to_edge(UP, buff=0.45)

        top_line = Line(
            LEFT * 3.85 + UP * 0.05,
            RIGHT * 3.85 + UP * 0.05,
            color=BLACK,
            stroke_width=1.3,
        )

        self.play(
            Write(chapter),
            Create(top_line),
            run_time=0.8,
        )

        title = heading(
            "Hessian curvature and gradient descent",
            30,
        )
        title.next_to(chapter, DOWN, buff=0.55)

        show(title, 0.8)

        subtitle = txt(
            "A poorly conditioned valley can make gradient descent inefficient.",
            18,
            BLACK,
        )

        if subtitle.width > 7.3:
            subtitle.scale_to_fit_width(7.3)

        subtitle.next_to(title, DOWN, buff=0.3)

        show(subtitle, 0.7)

        self.wait(1.0)
        clear_scene()

        # ========================================================
        # SCENE 2 — UNEQUAL CURVATURE
        # ========================================================

        title = heading(
            "Unequal curvature",
            34,
        )
        title.to_edge(UP, buff=0.65)

        show(title, 0.7)

        explanation = txt(
            "The Hessian has much more curvature in one direction.",
            19,
            BLACK,
        )

        if explanation.width > 7.2:
            explanation.scale_to_fit_width(7.2)

        explanation.next_to(title, DOWN, buff=0.3)

        show(explanation, 0.7)

        graph = Axes(
            x_range=[-5.8, 5.8, 1],
            y_range=[-5.8, 5.8, 1],
            x_length=6.8,
            y_length=6.8,
            axis_config={
                "color": BLACK,
                "stroke_width": 1.5,
                "include_ticks": False,
                "include_numbers": False,
            },
        )

        graph.move_to(DOWN * 0.15)

        theta = -0.42

        contours = VGroup()

        radii = [
            (0.45, 0.20),
            (0.85, 0.34),
            (1.25, 0.49),
            (1.70, 0.67),
            (2.20, 0.88),
            (2.80, 1.10),
            (3.50, 1.34),
            (4.30, 1.62),
            (5.15, 1.92),
        ]

        for rx, ry in radii:

            def ellipse_point(t, rx=rx, ry=ry):
                x = rx * np.cos(t)
                y = ry * np.sin(t)

                xr = x * np.cos(theta) - y * np.sin(theta)
                yr = x * np.sin(theta) + y * np.cos(theta)

                return graph.c2p(xr, yr)

            contours.add(
                ParametricFunction(
                    ellipse_point,
                    t_range=[0, TAU],
                    color=BLUE,
                    stroke_width=2.1,
                )
            )

        minimum = Dot(
            graph.c2p(0, 0),
            radius=0.08,
            color=BLACK,
        )

        minimum_label = txt(
            "minimum",
            17,
            BLACK,
        )
        minimum_label.next_to(
            minimum,
            DOWN,
            buff=0.16,
        )

        self.play(
            Create(graph),
            run_time=0.6,
        )

        self.play(
            LaggedStart(
                *[Create(c) for c in contours],
                lag_ratio=0.07,
            ),
            run_time=2.0,
        )

        self.play(
            FadeIn(minimum),
            Write(minimum_label),
            run_time=0.6,
        )

        steep_direction = Arrow(
            graph.c2p(-3.1, 2.8),
            graph.c2p(-1.0, 0.85),
            color=BLUE,
            stroke_width=3.5,
            buff=0,
        )

        shallow_direction = Arrow(
            graph.c2p(-3.3, -0.55),
            graph.c2p(-1.15, -0.18),
            color=BLACK,
            stroke_width=3,
            buff=0,
        )

        steep_label = txt(
            "high curvature",
            16,
            BLUE,
        )
        steep_label.next_to(
            steep_direction.get_start(),
            UP,
            buff=0.12,
        )

        shallow_label = txt(
            "low curvature",
            16,
            BLACK,
        )
        shallow_label.next_to(
            shallow_direction.get_start(),
            DOWN,
            buff=0.12,
        )

        self.play(
            Create(steep_direction),
            Write(steep_label),
            run_time=0.7,
        )

        self.play(
            Create(shallow_direction),
            Write(shallow_label),
            run_time=0.7,
        )

        self.wait(1.2)
        clear_scene()

        # ========================================================
        # SCENE 3 — GRADIENT DESCENT PATH
        # ========================================================

        title = heading(
            "Gradient descent across the valley",
            29,
        )
        title.to_edge(UP, buff=0.65)

        show(title, 0.8)

        subtitle = txt(
            "The steepest direction is not always the most useful search direction.",
            17,
            BLACK,
        )

        if subtitle.width > 7.2:
            subtitle.scale_to_fit_width(7.2)

        subtitle.next_to(title, DOWN, buff=0.28)

        show(subtitle, 0.7)

        graph = Axes(
            x_range=[-5.8, 5.8, 1],
            y_range=[-5.8, 5.8, 1],
            x_length=6.8,
            y_length=6.8,
            axis_config={
                "color": BLACK,
                "stroke_width": 1.4,
                "include_ticks": False,
                "include_numbers": False,
            },
        )

        graph.move_to(DOWN * 0.15)

        contours = VGroup()

        for rx, ry in radii:

            def ellipse_point(t, rx=rx, ry=ry):
                x = rx * np.cos(t)
                y = ry * np.sin(t)

                xr = x * np.cos(theta) - y * np.sin(theta)
                yr = x * np.sin(theta) + y * np.cos(theta)

                return graph.c2p(xr, yr)

            contours.add(
                ParametricFunction(
                    ellipse_point,
                    t_range=[0, TAU],
                    color=BLUE,
                    stroke_width=1.7,
                )
            )

        self.play(
            Create(graph),
            run_time=0.6,
        )

        self.play(
            LaggedStart(
                *[Create(c) for c in contours],
                lag_ratio=0.06,
            ),
            run_time=1.6,
        )

        path_points = np.array([
            [-4.2, 3.7],
            [-2.8, 2.35],
            [-3.55, 1.20],
            [-1.95, 0.65],
            [-2.45, -0.10],
            [-1.15, 0.10],
            [-1.55, -0.32],
            [-0.62, 0.02],
            [-0.82, -0.20],
            [-0.30, 0.02],
            [-0.38, -0.08],
            [0.0, 0.0],
        ])

        path = VGroup()

        for i in range(len(path_points) - 1):
            path.add(
                Line(
                    graph.c2p(*path_points[i]),
                    graph.c2p(*path_points[i + 1]),
                    color=BLACK,
                    stroke_width=4,
                )
            )

        dots = VGroup(
            *[
                Dot(
                    graph.c2p(*p),
                    radius=0.055,
                    color=BLACK,
                )
                for p in path_points
            ]
        )

        for segment in path:
            self.play(
                Create(segment),
                run_time=0.25,
            )

        self.play(
            LaggedStart(
                *[FadeIn(d) for d in dots],
                lag_ratio=0.04,
            ),
            run_time=0.6,
        )

        label = txt(
            "gradient descent path",
            17,
            BLACK,
        )

        label.next_to(
            graph,
            DOWN,
            buff=0.22,
        )

        show(label, 0.6)

        self.wait(1.1)
        clear_scene()

        # ========================================================
        # SCENE 4 — NO EMPTY BOXES
        # ========================================================

        title = heading(
            "Why the path becomes inefficient",
            29,
        )
        title.to_edge(UP, buff=0.65)

        show(title, 0.8)

        # --------------------------------------------------------
        # BOX 1
        # --------------------------------------------------------

        box1 = RoundedRectangle(
            width=7.1,
            height=1.65,
            corner_radius=0.18,
            color=BLACK,
            stroke_width=2.5,
        )

        box1.move_to(UP * 2.25)

        box1_text = txt(
            "Large curvature in one direction",
            21,
            BLACK,
        )

        box1_text.move_to(
            box1.get_center()
        )

        self.play(
            Create(box1),
            run_time=0.5,
        )

        self.play(
            Write(box1_text),
            run_time=0.7,
        )

        # --------------------------------------------------------
        # ARROW 1
        # --------------------------------------------------------

        arrow1 = Arrow(
            box1.get_bottom(),
            box1.get_bottom() + DOWN * 0.55,
            color=BLUE,
            stroke_width=3,
            buff=0.05,
        )

        self.play(
            Create(arrow1),
            run_time=0.45,
        )

        # --------------------------------------------------------
        # BOX 2
        # --------------------------------------------------------

        box2 = RoundedRectangle(
            width=7.1,
            height=1.65,
            corner_radius=0.18,
            color=BLUE,
            stroke_width=2.5,
        )

        box2.move_to(ORIGIN)

        box2_text = txt(
            "Step size must stay small",
            21,
            BLUE,
        )

        box2_text.move_to(
            box2.get_center()
        )

        self.play(
            Create(box2),
            run_time=0.5,
        )

        self.play(
            Write(box2_text),
            run_time=0.7,
        )

        # --------------------------------------------------------
        # ARROW 2
        # --------------------------------------------------------

        arrow2 = Arrow(
            box2.get_bottom(),
            box2.get_bottom() + DOWN * 0.55,
            color=BLUE,
            stroke_width=3,
            buff=0.05,
        )

        self.play(
            Create(arrow2),
            run_time=0.45,
        )

        # --------------------------------------------------------
        # BOX 3
        # --------------------------------------------------------

        box3 = RoundedRectangle(
            width=7.1,
            height=1.65,
            corner_radius=0.18,
            color=BLACK,
            stroke_width=2.5,
        )

        box3.move_to(DOWN * 2.25)

        box3_text = txt(
            "Progress becomes slow in the shallow direction",
            18,
            BLACK,
        )

        if box3_text.width > 6.4:
            box3_text.scale_to_fit_width(6.4)

        box3_text.move_to(
            box3.get_center()
        )

        self.play(
            Create(box3),
            run_time=0.5,
        )

        self.play(
            Write(box3_text),
            run_time=0.7,
        )

        self.wait(1.4)
        clear_scene()

        # ========================================================
        # SCENE 5 — CONDITION NUMBER
        # ========================================================

        title = heading(
            "Hessian condition number",
            32,
        )
        title.to_edge(UP, buff=0.7)

        show(title, 0.8)

        intro = txt(
            "The ratio between the largest and smallest curvature",
            19,
            BLACK,
        )

        if intro.width > 7.1:
            intro.scale_to_fit_width(7.1)

        intro.next_to(
            title,
            DOWN,
            buff=0.3,
        )

        show(intro, 0.7)

        equation = math(
            r"\kappa(H)=\frac{\lambda_{\max}}{\lambda_{\min}}",
            38,
            BLUE,
        )

        equation.next_to(
            intro,
            DOWN,
            buff=0.55,
        )

        show(equation, 0.9)

        description = txt(
            "A large condition number means strongly unequal curvature.",
            18,
            BLACK,
        )

        if description.width > 7.0:
            description.scale_to_fit_width(7.0)

        description.next_to(
            equation,
            DOWN,
            buff=0.45,
        )

        show(description, 0.7)

        # --------------------------------------------------------
        # WELL CONDITIONED
        # --------------------------------------------------------

        good_title = heading(
            "Well-conditioned",
            25,
            BLACK,
        )

        good_title.move_to(
            UP * 1.55
        )

        self.play(
            Write(good_title),
            run_time=0.6,
        )

        good_center = DOWN * 0.05

        good_outer = Circle(
            radius=0.72,
            color=BLACK,
            stroke_width=3,
        )

        good_middle = Circle(
            radius=0.48,
            color=BLACK,
            stroke_width=3,
        )

        good_inner = Circle(
            radius=0.24,
            color=BLACK,
            stroke_width=3,
        )

        good_shapes = VGroup(
            good_outer,
            good_middle,
            good_inner,
        )

        good_shapes.move_to(
            good_center
        )

        self.play(
            Create(good_outer),
            run_time=0.5,
        )

        self.play(
            Create(good_middle),
            run_time=0.5,
        )

        self.play(
            Create(good_inner),
            run_time=0.5,
        )

        # --------------------------------------------------------
        # POORLY CONDITIONED
        # --------------------------------------------------------

        poor_title = heading(
            "Poorly conditioned",
            25,
            BLUE,
        )

        poor_title.move_to(
            DOWN * 2.0
        )

        self.play(
            Write(poor_title),
            run_time=0.6,
        )

        # Keep every ellipse BELOW the heading.
        poor_outer = Ellipse(
            width=5.4,
            height=0.82,
            color=BLUE,
            stroke_width=3,
        )

        poor_middle = Ellipse(
            width=4.0,
            height=0.60,
            color=BLUE,
            stroke_width=3,
        )

        poor_inner = Ellipse(
            width=2.5,
            height=0.40,
            color=BLUE,
            stroke_width=3,
        )

        poor_shapes = VGroup(
            poor_outer,
            poor_middle,
            poor_inner,
        )

        poor_shapes.arrange(
            DOWN,
            buff=0.25,
        )

        poor_shapes.next_to(
            poor_title,
            DOWN,
            buff=0.35,
        )

        self.play(
            Create(poor_outer),
            run_time=0.5,
        )

        self.play(
            Create(poor_middle),
            run_time=0.5,
        )

        self.play(
            Create(poor_inner),
            run_time=0.5,
        )

        self.wait(1.4)
        clear_scene()

        # ========================================================
        # SCENE 6 — FINAL SUMMARY
        # ========================================================

        title = heading(
            "The key idea",
            36,
        )
        title.to_edge(UP, buff=0.8)

        show(title, 0.8)

        statement1 = txt(
            "Gradient descent follows the local gradient,",
            21,
            BLACK,
        )

        statement1.next_to(
            title,
            DOWN,
            buff=0.8,
        )

        show(statement1, 0.7)

        statement2 = txt(
            "but the Hessian reveals how curvature changes",
            21,
            BLACK,
        )

        statement2.next_to(
            statement1,
            DOWN,
            buff=0.25,
        )

        show(statement2, 0.7)

        statement3 = txt(
            "across different directions.",
            21,
            BLUE,
        )

        statement3.next_to(
            statement2,
            DOWN,
            buff=0.25,
        )

        show(statement3, 0.7)

        equation = math(
            r"\kappa(H)=\frac{\lambda_{\max}}{\lambda_{\min}}",
            34,
            BLUE,
        )

        equation.next_to(
            statement3,
            DOWN,
            buff=0.7,
        )

        show(equation, 0.9)

        final = heading(
            "Large κ means strongly unequal curvature",
            22,
            BLACK,
        )

        if final.width > 7.1:
            final.scale_to_fit_width(7.1)

        final.next_to(
            equation,
            DOWN,
            buff=0.7,
        )

        show(final, 0.8)

        underline = Line(
            LEFT * 2.5,
            RIGHT * 2.5,
            color=BLUE,
            stroke_width=3,
        )

        underline.next_to(
            final,
            DOWN,
            buff=0.25,
        )

        self.play(
            Create(underline),
            run_time=0.5,
        )

        self.wait(2.0)


if __name__ == "__main__":
    Page_89().render()
