from manim import *

config.background_color = WHITE


class Figure207(Scene):

    # ==========================================================
    # HELPERS
    # ==========================================================

    def flash(self, mob, color=YELLOW, run_time=0.4):
        self.play(
            Indicate(
                mob,
                color=color,
                scale_factor=1.12,
            ),
            run_time=run_time,
        )

    def clear_group(self, group, run_time=0.45):
        if len(group) > 0:
            self.play(
                FadeOut(*group),
                run_time=run_time,
            )

    def heading(self, text):
        return Text(
            text,
            font_size=29,
            color=BLACK,
        ).to_edge(
            UP,
            buff=0.85,
        )

    def matrix(
        self,
        values,
        center,
        cell_w=0.8,
        cell_h=0.65,
        font_size=28,
    ):
        rows = len(values)
        cols = len(values[0])

        entries = VGroup()

        for r in range(rows):
            for c in range(cols):

                entry = MathTex(
                    values[r][c],
                    font_size=font_size,
                    color=BLACK,
                )

                entry.move_to(
                    center
                    + RIGHT * (c - (cols - 1) / 2) * cell_w
                    + UP * ((rows - 1) / 2 - r) * cell_h
                )

                entries.add(entry)

        height = (rows - 1) * cell_h + 0.65
        width = (cols - 1) * cell_w + 0.65

        left = MathTex(
            r"\left[",
            font_size=font_size * 1.6,
            color=BLACK,
        )

        right = MathTex(
            r"\right]",
            font_size=font_size * 1.6,
            color=BLACK,
        )

        left.stretch_to_fit_height(height)
        right.stretch_to_fit_height(height)

        left.move_to(
            center + LEFT * (width / 2 + 0.22)
        )

        right.move_to(
            center + RIGHT * (width / 2 + 0.22)
        )

        return VGroup(left, entries, right), entries

    # ==========================================================
    # SCENE
    # ==========================================================

    def construct(self):

        title = Text(
            "Linear Dependence and Span",
            font_size=32,
            color=BLACK,
        )

        title.to_edge(
            UP,
            buff=0.3,
        )

        self.play(
            Write(title),
            run_time=0.8,
        )

        # ======================================================
        # 1. INVERSE SOLUTION
        # ======================================================

        g = VGroup()

        h = self.heading(
            "The inverse gives a solution — when it exists"
        )

        equation = MathTex(
            r"\mathbf{x}=A^{-1}\mathbf{b}",
            font_size=45,
            color=BLACK,
        )

        equation.move_to(
            DOWN * 0.15
        )

        caption = Text(
            "This requires A⁻¹ to exist.",
            font_size=24,
            color=BLACK,
        )

        caption.next_to(
            equation,
            DOWN,
            buff=0.4,
        )

        self.play(
            Write(h),
            Write(equation),
            Write(caption),
            run_time=1.0,
        )

        self.flash(
            equation,
            color=GREEN,
        )

        self.wait(1)

        g.add(
            h,
            equation,
            caption,
        )

        self.clear_group(g)

        # ======================================================
        # 2. NUMBER OF SOLUTIONS
        # ======================================================

        g = VGroup()

        h = self.heading(
            "A system can have different numbers of solutions"
        )

        self.play(
            Write(h),
            run_time=0.7,
        )

        # One solution
        one_circle = Circle(
            radius=0.65,
            stroke_width=2,
            color=BLACK,
        )

        one_dot = Dot(
            color=BLACK,
        )

        one = VGroup(
            one_circle,
            one_dot,
        )

        one.move_to(
            LEFT * 3.5 + DOWN * 0.25
        )

        one_label = Text(
            "One solution",
            font_size=24,
            color=BLACK,
        )

        one_label.next_to(
            one,
            DOWN,
            buff=0.35,
        )

        # No solution
        none = Circle(
            radius=0.65,
            stroke_width=2,
            color=BLACK,
        )

        none.move_to(
            DOWN * 0.25
        )

        none_label = Text(
            "No solution",
            font_size=24,
            color=BLACK,
        )

        none_label.next_to(
            none,
            DOWN,
            buff=0.35,
        )

        # Infinite solutions
        infinite_line = Line(
            LEFT * 0.9,
            RIGHT * 0.9,
            stroke_width=2,
            color=BLACK,
        )

        infinite = VGroup(
            infinite_line,
            Dot(LEFT * 0.55, color=BLACK),
            Dot(ORIGIN, color=BLACK),
            Dot(RIGHT * 0.55, color=BLACK),
        )

        infinite.move_to(
            RIGHT * 3.5 + DOWN * 0.25
        )

        infinite_label = Text(
            "Infinitely many",
            font_size=24,
            color=BLACK,
        )

        infinite_label.next_to(
            infinite,
            DOWN,
            buff=0.35,
        )

        self.play(
            Create(one),
            Write(one_label),
            run_time=0.7,
        )

        self.flash(
            one,
            color=GREEN,
        )

        self.play(
            Create(none),
            Write(none_label),
            run_time=0.7,
        )

        self.flash(
            none,
            color=RED,
        )

        self.play(
            Create(infinite),
            Write(infinite_label),
            run_time=0.7,
        )

        self.flash(
            infinite,
            color=YELLOW,
        )

        g.add(
            h,
            one,
            one_label,
            none,
            none_label,
            infinite,
            infinite_label,
        )

        self.wait(1)

        self.clear_group(g)

        # ======================================================
        # 3. INFINITELY MANY SOLUTIONS
        # ======================================================

        g = VGroup()

        h = self.heading(
            "If x and y are solutions, infinitely many can follow"
        )

        self.play(
            Write(h),
            run_time=0.7,
        )

        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2.5, 2.5, 1],
            x_length=6.5,
            y_length=4.2,
            axis_config={
                "color": BLACK,
                "stroke_width": 1.5,
                "include_tip": False,
                "include_numbers": False,
            },
        )

        axes.move_to(
            DOWN * 0.35
        )

        self.play(
            Create(axes),
            run_time=0.7,
        )

        x_point = axes.c2p(
            -2,
            -1.2,
        )

        y_point = axes.c2p(
            2,
            1.2,
        )

        solution_line = Line(
            x_point,
            y_point,
            color=GRAY_B,
            stroke_width=2,
        )

        x_dot = Dot(
            x_point,
            radius=0.08,
            color=BLACK,
        )

        y_dot = Dot(
            y_point,
            radius=0.08,
            color=BLACK,
        )

        x_label = MathTex(
            r"\mathbf{x}",
            font_size=30,
        ).next_to(
            x_dot,
            DOWN + LEFT,
            buff=0.15,
        )

        y_label = MathTex(
            r"\mathbf{y}",
            font_size=30,
        ).next_to(
            y_dot,
            UP + RIGHT,
            buff=0.15,
        )

        self.play(
            Create(solution_line),
            FadeIn(x_dot),
            FadeIn(y_dot),
            Write(x_label),
            Write(y_label),
            run_time=0.8,
        )

        self.flash(
            x_dot,
            color=GREEN,
        )

        self.flash(
            y_dot,
            color=GREEN,
        )

        z_dot = Dot(
            axes.c2p(0, 0),
            radius=0.09,
            color=BLACK,
        )

        z_label = MathTex(
            r"\mathbf{z}=\alpha\mathbf{x}+(1-\alpha)\mathbf{y}",
            font_size=27,
            color=BLACK,
        )

        z_label.to_edge(
            DOWN,
            buff=0.35,
        )

        self.play(
            FadeIn(z_dot),
            Write(z_label),
            run_time=0.8,
        )

        positions = [
            axes.c2p(-1.4, -0.84),
            axes.c2p(-0.7, -0.42),
            axes.c2p(0, 0),
            axes.c2p(0.8, 0.48),
            axes.c2p(1.5, 0.9),
        ]

        for pos in positions:

            self.flash(
                z_dot,
                color=YELLOW,
                run_time=0.22,
            )

            self.play(
                z_dot.animate.move_to(pos),
                run_time=0.4,
            )

        g.add(
            h,
            axes,
            solution_line,
            x_dot,
            y_dot,
            x_label,
            y_label,
            z_dot,
            z_label,
        )

        self.wait(1)

        self.clear_group(g)

        # ======================================================
        # 4. COLUMNS OF A
        # ======================================================

        g = VGroup()

        h = self.heading(
            "The columns of A define directions"
        )

        self.play(
            Write(h),
            run_time=0.7,
        )

        plane = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-2.5, 2.5, 1],
            x_length=7,
            y_length=5,
            background_line_style={
                "stroke_color": GRAY_A,
                "stroke_width": 1,
                "stroke_opacity": 0.3,
            },
            axis_config={
                "color": BLACK,
                "stroke_width": 1.5,
            },
        )

        plane.move_to(
            DOWN * 0.35
        )

        self.play(
            Create(plane),
            run_time=0.8,
        )

        origin = plane.c2p(0, 0)

        v1_end = plane.c2p(2, 1)
        v2_end = plane.c2p(1, 2)

        v1 = Arrow(
            origin,
            v1_end,
            color=BLACK,
            stroke_width=4,
            buff=0,
        )

        v2 = Arrow(
            origin,
            v2_end,
            color=BLACK,
            stroke_width=4,
            buff=0,
        )

        v1_label = MathTex(
            r"A_{:,1}",
            font_size=28,
        ).next_to(
            v1_end,
            RIGHT,
            buff=0.15,
        )

        v2_label = MathTex(
            r"A_{:,2}",
            font_size=28,
        ).next_to(
            v2_end,
            UP,
            buff=0.15,
        )

        self.play(
            GrowArrow(v1),
            Write(v1_label),
            run_time=0.8,
        )

        self.flash(
            v1,
            color=YELLOW,
        )

        self.play(
            GrowArrow(v2),
            Write(v2_label),
            run_time=0.8,
        )

        self.flash(
            v2,
            color=YELLOW,
        )

        formula = MathTex(
            r"A\mathbf{x}=x_1A_{:,1}+x_2A_{:,2}",
            font_size=31,
            color=BLACK,
        )

        formula.to_edge(
            DOWN,
            buff=0.35,
        )

        self.play(
            Write(formula),
            run_time=0.9,
        )

        g.add(
            h,
            plane,
            v1,
            v2,
            v1_label,
            v2_label,
            formula,
        )

        self.wait(1)

        self.clear_group(g)

        # ======================================================
        # 5. LINEAR COMBINATION
        # ======================================================

        g = VGroup()

        h = self.heading(
            "Each coefficient controls how far we travel"
        )

        self.play(
            Write(h),
            run_time=0.7,
        )

        plane = NumberPlane(
            x_range=[-3, 4, 1],
            y_range=[-2.5, 4, 1],
            x_length=7,
            y_length=5.3,
            background_line_style={
                "stroke_color": GRAY_A,
                "stroke_width": 1,
                "stroke_opacity": 0.3,
            },
            axis_config={
                "color": BLACK,
                "stroke_width": 1.5,
            },
        )

        plane.move_to(
            DOWN * 0.4
        )

        self.play(
            Create(plane),
            run_time=0.7,
        )

        origin = plane.c2p(0, 0)

        v1 = Arrow(
            origin,
            plane.c2p(2, 1),
            color=BLACK,
            stroke_width=4,
            buff=0,
        )

        v2 = Arrow(
            origin,
            plane.c2p(1, 2),
            color=BLACK,
            stroke_width=4,
            buff=0,
        )

        self.play(
            GrowArrow(v1),
            run_time=0.6,
        )

        self.play(
            GrowArrow(v2),
            run_time=0.6,
        )

        c1 = MathTex(
            r"x_1",
            font_size=30,
        ).next_to(
            v1.get_center(),
            DOWN + LEFT,
            buff=0.15,
        )

        c2 = MathTex(
            r"x_2",
            font_size=30,
        ).next_to(
            v2.get_center(),
            UP + LEFT,
            buff=0.15,
        )

        self.play(
            Write(c1),
            Write(c2),
        )

        self.flash(
            c1,
            color=YELLOW,
        )

        scaled_v1 = Arrow(
            origin,
            plane.c2p(3, 1.5),
            color=BLACK,
            stroke_width=5,
            buff=0,
        )

        self.play(
            Transform(
                v1,
                scaled_v1,
            ),
            run_time=0.9,
        )

        self.flash(
            c2,
            color=YELLOW,
        )

        scaled_v2 = Arrow(
            origin,
            plane.c2p(1.5, 3),
            color=BLACK,
            stroke_width=5,
            buff=0,
        )

        self.play(
            Transform(
                v2,
                scaled_v2,
            ),
            run_time=0.9,
        )

        # Resultant is deliberately kept inside the frame.
        result = Arrow(
            origin,
            plane.c2p(2.8, 4.2),
            color=BLACK,
            stroke_width=5,
            buff=0,
        )

        result_label = MathTex(
            r"\mathbf{b}",
            font_size=31,
        ).next_to(
            result.get_end(),
            RIGHT,
            buff=0.12,
        )

        self.flash(
            VGroup(v1, v2),
            color=GREEN,
        )

        self.play(
            GrowArrow(result),
            Write(result_label),
            run_time=1,
        )

        combination = MathTex(
            r"\mathbf{b}=x_1A_{:,1}+x_2A_{:,2}",
            font_size=31,
        )

        combination.to_edge(
            DOWN,
            buff=0.35,
        )

        self.play(
            Write(combination),
            run_time=0.8,
        )

        g.add(
            h,
            plane,
            v1,
            v2,
            c1,
            c2,
            result,
            result_label,
            combination,
        )

        self.wait(1)

        self.clear_group(g)

        # ======================================================
        # 6. LINEAR COMBINATION
        # ======================================================

        g = VGroup()

        h = self.heading(
            "This operation is called a linear combination"
        )

        formula = MathTex(
            r"\sum_i c_i\mathbf{v}^{(i)}",
            font_size=46,
            color=BLACK,
        )

        formula.move_to(
            UP * 0.55
        )

        explanation = Text(
            "Scale each vector, then add the results.",
            font_size=25,
            color=BLACK,
        )

        explanation.next_to(
            formula,
            DOWN,
            buff=0.35,
        )

        self.play(
            Write(h),
            Write(formula),
            Write(explanation),
            run_time=0.9,
        )

        self.flash(
            formula,
            color=YELLOW,
        )

        vectors = VGroup()

        vector_data = [
            (
                LEFT * 3.4 + DOWN * 1.0,
                LEFT * 2.4 + UP * 0.2,
                r"c_1\mathbf{v}^{(1)}",
            ),
            (
                LEFT * 0.8 + DOWN * 1.0,
                LEFT * 0.1 + UP * 0.8,
                r"c_2\mathbf{v}^{(2)}",
            ),
            (
                RIGHT * 1.8 + DOWN * 1.0,
                RIGHT * 3.0 + UP * 0.1,
                r"c_3\mathbf{v}^{(3)}",
            ),
        ]

        for start, end, label_text in vector_data:

            arrow = Arrow(
                start,
                end,
                color=BLACK,
                stroke_width=4,
                buff=0,
            )

            label = MathTex(
                label_text,
                font_size=24,
            )

            label.next_to(
                arrow.get_end(),
                UP,
                buff=0.15,
            )

            self.play(
                GrowArrow(arrow),
                run_time=0.6,
            )

            self.flash(
                arrow,
                color=YELLOW,
            )

            self.play(
                Write(label),
                run_time=0.4,
            )

            vectors.add(
                arrow,
                label,
            )

        result = Text(
            "Scale + add = linear combination",
            font_size=26,
            color=BLACK,
        )

        result.to_edge(
            DOWN,
            buff=0.35,
        )

        self.play(
            Write(result),
            run_time=0.7,
        )

        g.add(
            h,
            formula,
            explanation,
            vectors,
            result,
        )

        self.wait(1)

        self.clear_group(g)

        # ======================================================
        # 7. SPAN
        # ======================================================

        g = VGroup()

        h = self.heading(
            "The span is everything reachable by linear combinations"
        )

        self.play(
            Write(h),
            run_time=0.7,
        )

        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=8,
            y_length=5.2,
            background_line_style={
                "stroke_color": GRAY_A,
                "stroke_width": 1,
                "stroke_opacity": 0.3,
            },
            axis_config={
                "color": BLACK,
                "stroke_width": 1.5,
            },
        )

        plane.move_to(
            DOWN * 0.35
        )

        self.play(
            Create(plane),
            run_time=0.7,
        )

        # Visual span region.
        span_region = Polygon(
            plane.c2p(-3.5, -2.6),
            plane.c2p(3.5, -2.6),
            plane.c2p(3.5, 2.6),
            plane.c2p(-3.5, 2.6),
            fill_color=BLUE,
            fill_opacity=0.08,
            stroke_opacity=0,
        )

        self.play(
            FadeIn(span_region),
            run_time=0.8,
        )

        origin = plane.c2p(0, 0)

        v1 = Arrow(
            origin,
            plane.c2p(2.2, 1.1),
            color=BLACK,
            stroke_width=4,
            buff=0,
        )

        v2 = Arrow(
            origin,
            plane.c2p(1.1, 2.2),
            color=BLACK,
            stroke_width=4,
            buff=0,
        )

        self.play(
            GrowArrow(v1),
            run_time=0.6,
        )

        self.flash(
            v1,
            color=YELLOW,
        )

        self.play(
            GrowArrow(v2),
            run_time=0.6,
        )

        self.flash(
            v2,
            color=YELLOW,
        )

        span_label = MathTex(
            r"\operatorname{span}"
            r"\left\{\mathbf{v}^{(1)},\mathbf{v}^{(2)}\right\}",
            font_size=31,
            color=BLACK,
        )

        span_label.to_edge(
            DOWN,
            buff=0.35,
        )

        self.play(
            Write(span_label),
            run_time=0.9,
        )

        self.flash(
            span_region,
            color=BLUE,
            run_time=0.6,
        )

        conclusion = Text(
            "All points reachable by linear combinations.",
            font_size=24,
            color=BLACK,
        )

        conclusion.next_to(
            span_label,
            UP,
            buff=0.2,
        )

        self.play(
            Write(conclusion),
            run_time=0.7,
        )

        g.add(
            h,
            plane,
            span_region,
            v1,
            v2,
            span_label,
            conclusion,
        )

        self.wait(2)

        self.clear_group(g)

        # ======================================================
        # FINAL SUMMARY
        # ======================================================

        final_title = Text(
            "Linear combination → Span",
            font_size=31,
            color=BLACK,
        )

        final_title.move_to(
            UP * 1.2
        )

        final_formula = MathTex(
            r"\operatorname{span}"
            r"\{\mathbf{v}^{(1)},\ldots,\mathbf{v}^{(n)}\}"
            r"="
            r"\left\{\sum_i c_i\mathbf{v}^{(i)}\right\}",
            font_size=32,
            color=BLACK,
        )

        final_formula.move_to(
            DOWN * 0.15
        )

        self.play(
            Write(final_title),
            run_time=0.7,
        )

        self.play(
            Write(final_formula),
            run_time=1.0,
        )

        self.flash(
            final_formula,
            color=YELLOW,
        )

        self.wait(2)


if __name__ == "__main__":
    Figure207().render()
