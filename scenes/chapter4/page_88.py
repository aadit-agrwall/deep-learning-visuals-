from manim import *
import numpy as np

# ============================================================
# PAGE 88
# Saddle Point / Hessian Eigenvalues / Unequal Curvature
# TRUE 9:16 PORTRAIT
# ============================================================

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16
config.frame_rate = 60


WHITE_BG = "#FFFFFF"
BLACK = "#000000"
BLUE = "#0047AB"


class Page_88(ThreeDScene):

    def construct(self):

        self.camera.background_color = WHITE_BG

        # ----------------------------------------------------
        # TEXT HELPERS
        # ----------------------------------------------------

        def title(text, size=31):
            return Text(
                text,
                font="DejaVu Serif",
                font_size=size,
                color=BLACK,
            )

        def body(text, size=21, color=BLACK):
            return Text(
                text,
                font="DejaVu Serif",
                font_size=size,
                color=color,
            )

        def math(tex, size=32, color=BLACK):
            return MathTex(
                tex,
                font_size=size,
                color=color,
            )

        # ----------------------------------------------------
        # SAFE CLEAR
        #
        # IMPORTANT:
        # Do NOT reference self.axes.
        # Every current mobject is simply faded out.
        # ----------------------------------------------------

        def clear_scene():
            mobs = list(self.mobjects)

            if mobs:
                self.play(
                    *[FadeOut(mob) for mob in mobs],
                    run_time=0.45,
                )

            self.wait(0.15)

        # ====================================================
        # SCENE 1
        # ====================================================

        chapter = Text(
            "CHAPTER 4",
            font="DejaVu Serif",
            font_size=21,
            color=BLACK,
        )

        heading = Text(
            "Numerical Computation",
            font="DejaVu Serif",
            font_size=31,
            color=BLACK,
        )

        chapter.to_edge(UP, buff=0.55)
        heading.next_to(chapter, DOWN, buff=0.20)

        rule = Line(
            LEFT * 3.65,
            RIGHT * 3.65,
            color=BLACK,
            stroke_width=1.3,
        )

        rule.next_to(heading, DOWN, buff=0.23)

        section = title(
            "Second derivative and curvature",
            29,
        )

        section.next_to(
            rule,
            DOWN,
            buff=0.45,
        )

        self.play(
            Write(chapter),
            Write(heading),
            Create(rule),
            run_time=1.1,
        )

        self.play(
            Write(section),
            run_time=0.7,
        )

        self.wait(1.0)

        clear_scene()

        # ====================================================
        # SCENE 2
        # SECOND DERIVATIVE TEST
        # ====================================================

        heading = title(
            "Second-derivative test",
            31,
        )

        heading.to_edge(
            UP,
            buff=0.65,
        )

        self.play(
            Write(heading),
            run_time=0.7,
        )

        intro = body(
            "At a critical point, the first derivative is zero.",
            21,
        )

        intro.next_to(
            heading,
            DOWN,
            buff=0.48,
        )

        self.play(
            Write(intro),
            run_time=0.7,
        )

        critical = math(
            r"f'(x)=0",
            37,
            BLUE,
        )

        critical.next_to(
            intro,
            DOWN,
            buff=0.38,
        )

        self.play(
            Write(critical),
            run_time=0.65,
        )

        # ----------------------------------------------------
        # MINIMUM
        # ----------------------------------------------------

        min_box = RoundedRectangle(
            width=7.0,
            height=1.35,
            corner_radius=0.16,
            color=BLUE,
            stroke_width=3,
        )

        min_text = math(
            r"f''(x)>0\quad\Rightarrow\quad\text{local minimum}",
            25,
            BLUE,
        )

        min_text.move_to(
            min_box.get_center()
        )

        min_group = VGroup(
            min_box,
            min_text,
        )

        min_group.next_to(
            critical,
            DOWN,
            buff=0.55,
        )

        # ----------------------------------------------------
        # MAXIMUM
        # ----------------------------------------------------

        max_box = RoundedRectangle(
            width=7.0,
            height=1.35,
            corner_radius=0.16,
            color=BLACK,
            stroke_width=3,
        )

        max_text = math(
            r"f''(x)<0\quad\Rightarrow\quad\text{local maximum}",
            25,
            BLACK,
        )

        max_text.move_to(
            max_box.get_center()
        )

        max_group = VGroup(
            max_box,
            max_text,
        )

        max_group.next_to(
            min_group,
            DOWN,
            buff=0.35,
        )

        # ----------------------------------------------------
        # INCONCLUSIVE
        # ----------------------------------------------------

        inc_box = RoundedRectangle(
            width=7.0,
            height=1.35,
            corner_radius=0.16,
            color=BLUE,
            stroke_width=3,
        )

        inc_text = math(
            r"f''(x)=0\quad\Rightarrow\quad\text{inconclusive}",
            25,
            BLUE,
        )

        inc_text.move_to(
            inc_box.get_center()
        )

        inc_group = VGroup(
            inc_box,
            inc_text,
        )

        inc_group.next_to(
            max_group,
            DOWN,
            buff=0.35,
        )

        self.play(
            Create(min_box),
            Write(min_text),
            run_time=0.65,
        )

        self.play(
            Create(max_box),
            Write(max_text),
            run_time=0.65,
        )

        self.play(
            Create(inc_box),
            Write(inc_text),
            run_time=0.65,
        )

        self.wait(1.4)

        clear_scene()

        # ====================================================
        # SCENE 3
        # HESSIAN EIGENVALUE TEST
        # ====================================================

        heading = title(
            "The Hessian in multiple dimensions",
            28,
        )

        heading.to_edge(
            UP,
            buff=0.65,
        )

        self.play(
            Write(heading),
            run_time=0.7,
        )

        statement = body(
            "The Hessian collects the second derivatives.",
            21,
        )

        statement.next_to(
            heading,
            DOWN,
            buff=0.45,
        )

        self.play(
            Write(statement),
            run_time=0.7,
        )

        hessian = math(
            r"H(f)(x)",
            43,
            BLUE,
        )

        hessian.next_to(
            statement,
            DOWN,
            buff=0.38,
        )

        self.play(
            Write(hessian),
            run_time=0.65,
        )

        eigenvalues = math(
            r"\lambda_1,\lambda_2,\ldots,\lambda_n",
            33,
            BLACK,
        )

        eigenvalues.next_to(
            hessian,
            DOWN,
            buff=0.42,
        )

        self.play(
            Write(eigenvalues),
            run_time=0.65,
        )

        rule = body(
            "The signs of the eigenvalues determine the local geometry.",
            20,
        )

        rule.next_to(
            eigenvalues,
            DOWN,
            buff=0.42,
        )

        self.play(
            Write(rule),
            run_time=0.7,
        )

        # ----------------------------------------------------
        # CLASSIFICATION
        # ----------------------------------------------------

        minimum = VGroup(
            body("ALL POSITIVE", 20, BLUE),
            body("local minimum", 19, BLACK),
        )

        maximum = VGroup(
            body("ALL NEGATIVE", 20, BLACK),
            body("local maximum", 19, BLACK),
        )

        saddle = VGroup(
            body("MIXED SIGNS", 20, BLUE),
            body("saddle point", 19, BLACK),
        )

        for group in [minimum, maximum, saddle]:
            group.arrange(
                DOWN,
                buff=0.12,
            )

        classification = VGroup(
            minimum,
            maximum,
            saddle,
        )

        classification.arrange(
            DOWN,
            buff=0.38,
        )

        classification.next_to(
            rule,
            DOWN,
            buff=0.55,
        )

        for group in classification:
            self.play(
                Write(group[0]),
                Write(group[1]),
                run_time=0.55,
            )

        self.wait(1.4)

        clear_scene()

        # ====================================================
        # SCENE 4
        # SADDLE SURFACE
        # ====================================================

        # Reset 3D camera explicitly.
        self.set_camera_orientation(
            phi=68 * DEGREES,
            theta=-45 * DEGREES,
            zoom=0.9,
        )

        heading = title(
            "A saddle point has both signs",
            29,
        )

        heading.to_edge(
            UP,
            buff=0.55,
        )

        self.play(
            Write(heading),
            run_time=0.7,
        )

        equation = math(
            r"f(x_1,x_2)=x_1^2-x_2^2",
            32,
            BLUE,
        )

        equation.next_to(
            heading,
            DOWN,
            buff=0.30,
        )

        self.play(
            Write(equation),
            run_time=0.65,
        )

        # ----------------------------------------------------
        # GRAPH
        #
        # It occupies its own region.
        # No labels or paragraphs are placed on it.
        # ----------------------------------------------------

        axes = ThreeDAxes(
            x_range=[-2.4, 2.4, 1],
            y_range=[-2.4, 2.4, 1],
            z_range=[-5, 5, 2],
            x_length=5.8,
            y_length=5.8,
            z_length=3.1,
            axis_config={
                "color": BLACK,
                "stroke_width": 1.4,
            },
        )

        axes.shift(
            DOWN * 0.8
        )

        surface = Surface(
            lambda u, v: axes.c2p(
                u,
                v,
                u**2 - v**2,
            ),
            u_range=[-2.1, 2.1],
            v_range=[-2.1, 2.1],
            resolution=(24, 24),
            fill_opacity=0.0,
            stroke_color=BLUE,
            stroke_width=1.15,
        )

        self.play(
            Create(axes),
            Create(surface),
            run_time=2.2,
        )

        self.begin_ambient_camera_rotation(
            rate=0.06
        )

        self.wait(2.2)

        self.stop_ambient_camera_rotation()

        clear_scene()

        # ====================================================
        # SCENE 5
        # PRINCIPAL DIRECTIONS
        # ====================================================

        self.set_camera_orientation(
            phi=0,
            theta=-90 * DEGREES,
            zoom=1,
        )

        heading = title(
            "Two directions, two curvatures",
            29,
        )

        heading.to_edge(
            UP,
            buff=0.65,
        )

        self.play(
            Write(heading),
            run_time=0.7,
        )

        center = Dot(
            DOWN * 0.4,
            radius=0.09,
            color=BLACK,
        )

        self.play(
            FadeIn(center),
            run_time=0.35,
        )

        # ----------------------------------------------------
        # POSITIVE CURVATURE
        # ----------------------------------------------------

        positive_arrow = Arrow(
            center.get_center(),
            center.get_center()
            + RIGHT * 2.25
            + UP * 1.15,
            color=BLUE,
            stroke_width=4,
            buff=0.08,
        )

        self.play(
            Create(positive_arrow),
            run_time=0.75,
        )

        positive_value = math(
            r"\lambda_1>0",
            34,
            BLUE,
        )

        positive_value.next_to(
            positive_arrow.get_end(),
            RIGHT,
            buff=0.12,
        )

        positive_text = body(
            "curves upward",
            20,
            BLUE,
        )

        positive_text.next_to(
            positive_value,
            DOWN,
            buff=0.12,
        )

        self.play(
            Write(positive_value),
            Write(positive_text),
            run_time=0.7,
        )

        # ----------------------------------------------------
        # NEGATIVE CURVATURE
        # ----------------------------------------------------

        negative_arrow = Arrow(
            center.get_center(),
            center.get_center()
            + LEFT * 2.25
            + UP * 1.15,
            color=BLACK,
            stroke_width=4,
            buff=0.08,
        )

        self.play(
            Create(negative_arrow),
            run_time=0.75,
        )

        negative_value = math(
            r"\lambda_2<0",
            34,
            BLACK,
        )

        negative_value.next_to(
            negative_arrow.get_end(),
            LEFT,
            buff=0.12,
        )

        negative_text = body(
            "curves downward",
            20,
            BLACK,
        )

        negative_text.next_to(
            negative_value,
            DOWN,
            buff=0.12,
        )

        self.play(
            Write(negative_value),
            Write(negative_text),
            run_time=0.7,
        )

        conclusion = body(
            "Mixed eigenvalue signs → saddle point",
            23,
            BLUE,
        )

        conclusion.to_edge(
            DOWN,
            buff=0.75,
        )

        self.play(
            Write(conclusion),
            run_time=0.8,
        )

        self.wait(1.5)

        clear_scene()

        # ====================================================
        # SCENE 6
        # POOR HESSIAN CONDITIONING
        # ====================================================

        heading = title(
            "Poor Hessian conditioning",
            31,
        )

        heading.to_edge(
            UP,
            buff=0.65,
        )

        self.play(
            Write(heading),
            run_time=0.7,
        )

        intro = body(
            "Different directions can have very different curvature.",
            20,
        )

        intro.next_to(
            heading,
            DOWN,
            buff=0.45,
        )

        self.play(
            Write(intro),
            run_time=0.7,
        )

        # ----------------------------------------------------
        # ELLIPTICAL CONTOURS
        # ----------------------------------------------------

        outer = Ellipse(
            width=6.1,
            height=2.0,
            color=BLUE,
            stroke_width=3,
        )

        middle = Ellipse(
            width=4.25,
            height=1.35,
            color=BLUE,
            stroke_width=3,
        )

        inner = Ellipse(
            width=2.25,
            height=0.70,
            color=BLUE,
            stroke_width=3,
        )

        contours = VGroup(
            outer,
            middle,
            inner,
        )

        contours.shift(
            DOWN * 1.0
        )

        self.play(
            Create(outer),
            Create(middle),
            Create(inner),
            run_time=1.4,
        )

        long_axis = Line(
            LEFT * 3.0 + DOWN * 1.0,
            RIGHT * 3.0 + DOWN * 1.0,
            color=BLACK,
            stroke_width=3,
        )

        short_axis = Line(
            UP * 0.95 + DOWN * 1.0,
            DOWN * 0.95 + DOWN * 1.0,
            color=BLUE,
            stroke_width=3,
        )

        self.play(
            Create(long_axis),
            Create(short_axis),
            run_time=0.8,
        )

        slow = body(
            "slow direction",
            20,
            BLACK,
        )

        sharp = body(
            "sharp direction",
            20,
            BLUE,
        )

        slow.next_to(
            long_axis,
            DOWN,
            buff=0.25,
        )

        sharp.next_to(
            short_axis,
            RIGHT,
            buff=0.25,
        )

        self.play(
            Write(slow),
            Write(sharp),
            run_time=0.7,
        )

        condition = math(
            r"\frac{\lambda_{\max}}{\lambda_{\min}}\gg 1",
            35,
            BLUE,
        )

        condition.to_edge(
            DOWN,
            buff=0.85,
        )

        self.play(
            Write(condition),
            run_time=0.8,
        )

        self.wait(1.6)

        clear_scene()

        # ====================================================
        # SCENE 7
        # FINAL SUMMARY
        # ====================================================

        heading = title(
            "What the Hessian tells us",
            31,
        )

        heading.to_edge(
            UP,
            buff=0.7,
        )

        self.play(
            Write(heading),
            run_time=0.7,
        )

        lines = [
            body(
                "Positive eigenvalues → local minimum",
                21,
                BLUE,
            ),
            body(
                "Negative eigenvalues → local maximum",
                21,
                BLACK,
            ),
            body(
                "Mixed signs → saddle point",
                21,
                BLUE,
            ),
            body(
                "Very unequal magnitudes → poor conditioning",
                20,
                BLACK,
            ),
        ]

        summary = VGroup(*lines)

        summary.arrange(
            DOWN,
            buff=0.45,
            aligned_edge=LEFT,
        )

        summary.move_to(
            DOWN * 0.25
        )

        for line in lines:
            self.play(
                Write(line),
                run_time=0.65,
            )

        final = math(
            r"H(f)(x)\;\text{encodes local curvature}",
            29,
            BLUE,
        )

        final.to_edge(
            DOWN,
            buff=0.85,
        )

        self.play(
            Write(final),
            run_time=0.8,
        )

        self.wait(2.0)


if __name__ == "__main__":
    Page_88().render()
