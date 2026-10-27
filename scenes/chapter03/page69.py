import numpy as np
from manim import *

from common.layouts import fit_in_frame


class Page69(Scene):

    def construct(self):

        # ============================================================
        # THEME — SAME AS PAGE 66 / 67 / 68
        # ============================================================

        BG = "#04244E"
        WHITE = "#F5F7FA"
        MUTED = "#B9C7D8"
        CYAN = "#55D6FF"
        YELLOW = "#FFD166"
        GREEN = "#65E572"
        RED = "#FF6B6B"

        self.camera.background_color = BG

        def txt(text, size=28, color=WHITE, weight=NORMAL):
            return Text(
                text,
                font="DejaVu Sans",
                font_size=size,
                color=color,
                weight=weight
            )

        def show(obj, time=0.7):
            self.play(Write(obj), run_time=time)

        def clear_scene():
            if self.mobjects:
                self.play(
                    *[FadeOut(obj) for obj in list(self.mobjects)],
                    run_time=0.5
                )
            self.wait(0.25)

        # ============================================================
        # SCENE 1 — SECTION INTRO
        # ============================================================

        chapter = txt(
            "CHAPTER 3",
            24,
            CYAN,
            BOLD
        )

        heading = txt(
            "Probability and Information Theory",
            38,
            WHITE,
            BOLD
        )

        section = txt(
            "3.12  Continuous Variables",
            30,
            YELLOW
        )

        chapter.to_edge(UP, buff=0.65)
        heading.next_to(chapter, DOWN, buff=0.25)
        section.next_to(heading, DOWN, buff=0.35)

        show(chapter, 0.5)
        show(heading, 0.75)
        show(section, 0.6)

        self.wait(0.8)

        clear_scene()

        # ============================================================
        # SCENE 2 — WHY CONTINUOUS PROBABILITY GETS SUBTLE
        # ============================================================

        title = txt(
            "Continuous probability gets subtle",
            31,
            WHITE,
            BOLD
        )
        title.to_edge(UP, buff=0.7)

        statement = txt(
            "For a continuous variable, probability is found by integrating",
            19,
            MUTED
        )

        statement.next_to(title, DOWN, buff=0.35)

        formula = MathTex(
            r"P(\mathbf{x}\in S)=\int_S p(\mathbf{x})\,d\mathbf{x}",
            font_size=34,
            color=YELLOW
        )

        formula.next_to(
            statement,
            DOWN,
            buff=0.45
        )

        show(title, 0.7)
        show(statement, 0.7)

        self.play(
            Write(formula),
            run_time=1.0
        )

        # ============================================================
        # VISUALIZE A REGION S
        # ============================================================

        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 5, 1],
            x_length=6.0,
            y_length=4.2,
            axis_config={
                "color": MUTED,
                "stroke_width": 2,
                "include_tip": False
            },
            tips=False
        )

        axes.shift(DOWN * 0.45)

        region = Polygon(
            axes.c2p(1, 1),
            axes.c2p(4.8, 1),
            axes.c2p(4.2, 3.7),
            axes.c2p(1.4, 3.2),
            fill_color=CYAN,
            fill_opacity=0.35,
            stroke_color=CYAN,
            stroke_width=3
        )

        region_label = MathTex(
            r"S",
            font_size=32,
            color=WHITE
        )

        region_label.move_to(region.get_center())

        self.play(
            Create(axes),
            FadeIn(region),
            FadeIn(region_label),
            run_time=1.0
        )

        area_note = txt(
            "A region has volume / area.",
            18,
            GREEN
        )

        area_note.next_to(
            axes,
            DOWN,
            buff=0.25
        )

        show(area_note, 0.5)

        self.wait(0.7)

        clear_scene()

        # ============================================================
        # SCENE 3 — STRANGE SETS
        # ============================================================

        title = txt(
            "But not every set behaves so nicely",
            30,
            WHITE,
            BOLD
        )
        title.to_edge(UP, buff=0.7)

        statement = txt(
            "Some sets can be extremely complicated.",
            20,
            MUTED
        )
        statement.next_to(title, DOWN, buff=0.35)

        show(title, 0.7)
        show(statement, 0.7)

        # Two disjoint sets
        left_set = VGroup()
        right_set = VGroup()

        rng = np.random.default_rng(42)

        for _ in range(55):
            x = rng.uniform(-2.8, -0.3)
            y = rng.uniform(-1.5, 1.5)

            dot = Dot(
                np.array([x, y, 0]),
                radius=0.025,
                color=CYAN
            )

            left_set.add(dot)

        for _ in range(55):
            x = rng.uniform(0.3, 2.8)
            y = rng.uniform(-1.5, 1.5)

            dot = Dot(
                np.array([x, y, 0]),
                radius=0.025,
                color=YELLOW
            )

            right_set.add(dot)

        left_set.move_to(DOWN * 0.2 + LEFT * 0.3)
        right_set.move_to(DOWN * 0.2 + RIGHT * 0.3)

        self.play(
            LaggedStart(
                *[FadeIn(d) for d in left_set],
                lag_ratio=0.01
            ),
            run_time=0.8
        )

        self.play(
            LaggedStart(
                *[FadeIn(d) for d in right_set],
                lag_ratio=0.01
            ),
            run_time=0.8
        )

        paradox = MathTex(
            r"S_1\cap S_2=\varnothing",
            font_size=30,
            color=RED
        )

        paradox.to_edge(DOWN, buff=0.7)

        show(paradox, 0.7)

        warning = txt(
            "Yet badly chosen sets can create paradoxes.",
            18,
            RED
        )

        warning.next_to(
            paradox,
            UP,
            buff=0.25
        )

        self.play(
            FadeIn(warning),
            run_time=0.5
        )

        self.wait(0.7)

        clear_scene()

        # ============================================================
        # SCENE 4 — MEASURE THEORY
        # ============================================================

        title = txt(
            "Measure theory gives us a rigorous idea of size",
            29,
            WHITE,
            BOLD
        )
        title.to_edge(UP, buff=0.7)

        definition = txt(
            "Instead of asking only whether a set exists...",
            19,
            MUTED
        )

        definition.next_to(
            title,
            DOWN,
            buff=0.35
        )

        question = txt(
            "we ask:  how much space does it occupy?",
            24,
            YELLOW,
            BOLD
        )

        question.next_to(
            definition,
            DOWN,
            buff=0.4
        )

        show(title, 0.7)
        show(definition, 0.6)
        show(question, 0.8)

        # ============================================================
        # FILLED REGION
        # ============================================================

        square = Square(
            side_length=2.8,
            fill_color=CYAN,
            fill_opacity=0.45,
            stroke_color=CYAN,
            stroke_width=3
        )

        square.move_to(
            LEFT * 3.2 + DOWN * 0.9
        )

        area_label = txt(
            "positive measure",
            18,
            GREEN,
            BOLD
        )

        area_label.next_to(
            square,
            DOWN,
            buff=0.25
        )

        self.play(
            FadeIn(square, scale=0.8),
            FadeIn(area_label),
            run_time=0.8
        )

        # ============================================================
        # LINE
        # ============================================================

        line = Line(
            LEFT * 1.2,
            RIGHT * 1.2,
            color=YELLOW,
            stroke_width=6
        )

        line.move_to(
            ORIGIN + DOWN * 0.9
        )

        line_label = txt(
            "measure zero",
            18,
            YELLOW,
            BOLD
        )

        line_label.next_to(
            line,
            DOWN,
            buff=0.25
        )

        # Transform square → line
        self.play(
            Transform(
                square,
                line
            ),
            Transform(
                area_label,
                line_label
            ),
            run_time=1.2
        )

        self.wait(0.5)

        # ============================================================
        # POINT
        # ============================================================

        point = Dot(
            ORIGIN + DOWN * 0.9,
            radius=0.09,
            color=RED
        )

        point_label = txt(
            "one point → measure zero",
            17,
            RED
        )

        point_label.next_to(
            point,
            DOWN,
            buff=0.3
        )

        self.play(
            Transform(square, point),
            Transform(area_label, point_label),
            run_time=0.9
        )

        self.wait(0.8)

        clear_scene()

        # ============================================================
        # SCENE 5 — COUNTABLY MANY MEASURE-ZERO SETS
        # ============================================================

        title = txt(
            "Even many tiny sets can have measure zero",
            29,
            WHITE,
            BOLD
        )
        title.to_edge(UP, buff=0.7)

        statement = txt(
            "A countable union of measure-zero sets can still have measure zero.",
            18,
            MUTED
        )

        statement.next_to(
            title,
            DOWN,
            buff=0.35
        )

        show(title, 0.7)
        show(statement, 0.7)

        # Infinite-looking sequence of points
        points = VGroup()

        xs = np.linspace(-5.0, 5.0, 31)

        for i, x in enumerate(xs):
            y = 0.35 * np.sin(i * 0.9)

            dot = Dot(
                np.array([x * 0.7, y, 0]),
                radius=0.045,
                color=CYAN
            )

            points.add(dot)

        points.move_to(DOWN * 0.5)

        self.play(
            LaggedStart(
                *[FadeIn(p, scale=0.5) for p in points],
                lag_ratio=0.025
            ),
            run_time=1.4
        )

        zero = MathTex(
            r"\text{measure}=0",
            font_size=34,
            color=YELLOW
        )

        zero.next_to(
            points,
            DOWN,
            buff=0.55
        )

        self.play(
            Write(zero),
            run_time=0.8
        )

        note = txt(
            "No volume is occupied.",
            18,
            GREEN
        )

        note.to_edge(
            DOWN,
            buff=0.65
        )

        self.play(
            FadeIn(note, shift=UP * 0.15),
            run_time=0.5
        )

        self.wait(0.8)

        clear_scene()

        # ============================================================
        # SCENE 6 — ALMOST EVERYWHERE
        # ============================================================

        title = txt(
            "A powerful phrase:  almost everywhere",
            31,
            WHITE,
            BOLD
        )
        title.to_edge(UP, buff=0.7)

        formula = MathTex(
            r"\text{property holds almost everywhere}",
            font_size=30,
            color=CYAN
        )

        formula.next_to(
            title,
            DOWN,
            buff=0.45
        )

        show(title, 0.7)
        self.play(
            Write(formula),
            run_time=0.9
        )

        # Large space
        space = Rectangle(
            width=8.5,
            height=3.0,
            stroke_color=MUTED,
            stroke_width=2
        )

        space.move_to(
            DOWN * 0.4
        )

        self.play(
            Create(space),
            run_time=0.7
        )

        # Majority region
        majority = Rectangle(
            width=7.9,
            height=2.4,
            fill_color=CYAN,
            fill_opacity=0.18,
            stroke_opacity=0
        )

        majority.move_to(space.get_center())

        self.play(
            FadeIn(majority),
            run_time=0.6
        )

        # Tiny exceptional set
        exception = Dot(
            space.get_right() + LEFT * 0.35,
            radius=0.09,
            color=RED
        )

        exception_label = txt(
            "exceptional set\n(measure zero)",
            16,
            RED
        )

        exception_label.next_to(
            exception,
            DOWN,
            buff=0.2
        )

        self.play(
            FadeIn(exception, scale=0.5),
            FadeIn(exception_label),
            run_time=0.7
        )

        almost = txt(
            "Everywhere except a negligible set.",
            20,
            GREEN,
            BOLD
        )

        almost.next_to(
            space,
            DOWN,
            buff=0.35
        )

        self.play(
            FadeIn(almost, shift=UP * 0.15),
            run_time=0.7
        )

        self.wait(0.9)

        clear_scene()

        # ============================================================
        # SCENE 7 — FINAL TAKEAWAY
        # ============================================================

        label = txt(
            "THE KEY IDEA",
            23,
            CYAN,
            BOLD
        )

        label.to_edge(
            UP,
            buff=0.85
        )

        main = txt(
            "Measure theory tells us what \"size\" means\n"
            "for complicated sets in continuous probability.",
            25,
            WHITE,
            BOLD
        )

        main.move_to(
            ORIGIN + UP * 0.3
        )

        fit_in_frame(
            main,
            margin=0.8
        )

        show(label, 0.5)

        self.play(
            Write(main),
            run_time=1.3
        )

        bottom = txt(
            "Measure zero does not mean nonexistent — it means negligible.",
            18,
            MUTED
        )

        bottom.to_edge(
            DOWN,
            buff=0.7
        )

        self.play(
            FadeIn(bottom, shift=UP * 0.15),
            run_time=0.7
        )

        underline = Underline(
            main,
            color=CYAN,
            stroke_width=3,
            buff=0.16
        )

        self.play(
            Create(underline),
            run_time=0.5
        )

        self.wait(2.0)


if __name__ == "__main__":
    Page69().render()
