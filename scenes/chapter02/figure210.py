from manim import *

config.background_color = WHITE


class Figure210(Scene):

    BLACK_TEXT = "#111111"
    BLUE = "#1769AA"
    GREEN = "#16855B"
    RED = "#C43D3D"
    GRID = "#B8B8B8"

    def title(self, text):
        return Text(
            text,
            font_size=29,
            color=self.BLACK_TEXT,
        ).to_edge(UP, buff=0.32)

    def grid(self):
        return NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=8,
            y_length=5.0,
            background_line_style={
                "stroke_color": self.GRID,
                "stroke_width": 1,
                "stroke_opacity": 0.22,
            },
            axis_config={
                "color": "#777777",
                "stroke_width": 1.3,
                "include_tip": False,
            },
        )

    def flash(self, mob, color=None):
        if color is None:
            color = self.BLUE

        self.play(
            Indicate(
                mob,
                color=color,
                scale_factor=1.06,
                rate_func=there_and_back,
            ),
            run_time=0.35,
        )

    def clear(self, group):
        if len(group) > 0:
            self.play(
                FadeOut(group),
                run_time=0.45,
            )

    def construct(self):

        # ======================================================
        # 1. L1 NORM
        # ======================================================

        g = VGroup()

        heading = self.title("The L1 norm")

        self.play(
            Write(heading),
            run_time=0.65,
        )

        vector = MathTex(
            r"\mathbf{x}="
            r"\begin{bmatrix}"
            r"x_1\\"
            r"x_2\\"
            r"x_3"
            r"\end{bmatrix}",
            font_size=40,
            color=self.BLACK_TEXT,
        )

        vector.move_to(
            LEFT * 2.7 + UP * 0.25
        )

        formula = MathTex(
            r"\|\mathbf{x}\|_1="
            r"|x_1|+|x_2|+|x_3|",
            font_size=37,
            color=self.BLACK_TEXT,
        )

        formula.move_to(
            RIGHT * 1.5 + UP * 0.25
        )

        self.play(
            Write(vector),
            run_time=0.75,
        )

        self.flash(vector, self.BLUE)

        self.play(
            Write(formula),
            run_time=0.8,
        )

        self.flash(formula, self.GREEN)

        explanation = Text(
            "Add the absolute value of every component.",
            font_size=22,
            color=self.BLACK_TEXT,
        )

        explanation.move_to(DOWN * 1.55)

        self.play(
            Write(explanation),
            run_time=0.7,
        )

        example = MathTex(
            r"\mathbf{x}="
            r"\begin{bmatrix}"
            r"2\\-3\\1"
            r"\end{bmatrix}"
            r"\quad\Longrightarrow\quad"
            r"\|\mathbf{x}\|_1=|2|+|-3|+|1|=6",
            font_size=31,
            color=self.BLACK_TEXT,
        )

        example.move_to(DOWN * 2.45)

        self.play(
            Write(example),
            run_time=0.85,
        )

        self.flash(example, self.BLUE)

        g.add(
            heading,
            vector,
            formula,
            explanation,
            example,
        )

        self.wait(1)
        self.clear(g)

        # ======================================================
        # 2. L1 AND ZERO / NONZERO
        # ======================================================

        g = VGroup()

        heading = self.title("Why L1 is useful")

        self.play(
            Write(heading),
            run_time=0.65,
        )

        vector = MathTex(
            r"\mathbf{x}="
            r"\begin{bmatrix}"
            r"0\\2\\0\\-3"
            r"\end{bmatrix}",
            font_size=40,
            color=self.BLACK_TEXT,
        )

        vector.move_to(
            LEFT * 2.8 + UP * 0.2
        )

        self.play(
            Write(vector),
            run_time=0.75,
        )

        self.flash(vector, self.BLUE)

        norm = MathTex(
            r"\|\mathbf{x}\|_1="
            r"|0|+|2|+|0|+|-3|=5",
            font_size=32,
            color=self.BLACK_TEXT,
        )

        norm.move_to(
            RIGHT * 1.5 + UP * 0.2
        )

        self.play(
            Write(norm),
            run_time=0.8,
        )

        self.flash(norm, self.GREEN)

        zero_text = Text(
            "Zero components remain exactly zero.",
            font_size=23,
            color=self.BLUE,
        )

        zero_text.move_to(DOWN * 1.05)

        self.play(
            Write(zero_text),
            run_time=0.7,
        )

        important = Text(
            "This makes L1 useful when zero vs. nonzero matters.",
            font_size=21,
            color=self.BLACK_TEXT,
        )

        important.move_to(DOWN * 2.0)

        self.play(
            Write(important),
            run_time=0.7,
        )

        g.add(
            heading,
            vector,
            norm,
            zero_text,
            important,
        )

        self.wait(1)
        self.clear(g)

        # ======================================================
        # 3. L0 IS NOT A NORM
        # ======================================================

        g = VGroup()

        heading = self.title(
            "The so-called L0 norm is not actually a norm"
        )

        self.play(
            Write(heading),
            run_time=0.7,
        )

        left = MathTex(
            r"\mathbf{x}="
            r"\begin{bmatrix}"
            r"2\\0\\-3"
            r"\end{bmatrix}",
            font_size=39,
            color=self.BLACK_TEXT,
        )

        right = MathTex(
            r"2\mathbf{x}="
            r"\begin{bmatrix}"
            r"4\\0\\-6"
            r"\end{bmatrix}",
            font_size=39,
            color=self.BLACK_TEXT,
        )

        left.move_to(
            LEFT * 2.4 + UP * 0.35
        )

        right.move_to(
            RIGHT * 2.4 + UP * 0.35
        )

        self.play(
            Write(left),
            run_time=0.7,
        )

        self.flash(left, self.BLUE)

        arrow = Arrow(
            left.get_right(),
            right.get_left(),
            buff=0.45,
            color="#777777",
            stroke_width=2,
        )

        self.play(
            GrowArrow(arrow),
            run_time=0.5,
        )

        self.play(
            Write(right),
            run_time=0.7,
        )

        self.flash(right, self.GREEN)

        count_left = MathTex(
            r"\#\{x_i\neq0\}=2",
            font_size=30,
            color=self.BLACK_TEXT,
        )

        count_right = MathTex(
            r"\#\{(2x_i)\neq0\}=2",
            font_size=30,
            color=self.BLACK_TEXT,
        )

        count_left.move_to(
            LEFT * 2.4 + DOWN * 0.9
        )

        count_right.move_to(
            RIGHT * 2.4 + DOWN * 0.9
        )

        self.play(
            Write(count_left),
            Write(count_right),
            run_time=0.7,
        )

        conclusion = Text(
            "Scaling changes the values, but not the number of nonzero entries.",
            font_size=20,
            color=self.RED,
        )

        conclusion.move_to(DOWN * 2.0)

        self.play(
            Write(conclusion),
            run_time=0.75,
        )

        g.add(
            heading,
            left,
            right,
            arrow,
            count_left,
            count_right,
            conclusion,
        )

        self.wait(1)
        self.clear(g)

        # ======================================================
        # 4. L INFINITY
        # ======================================================

        g = VGroup()

        heading = self.title(
            "The L∞ norm"
        )

        self.play(
            Write(heading),
            run_time=0.65,
        )

        vector = MathTex(
            r"\mathbf{x}="
            r"\begin{bmatrix}"
            r"-2\\5\\-3\\1"
            r"\end{bmatrix}",
            font_size=41,
            color=self.BLACK_TEXT,
        )

        vector.move_to(
            LEFT * 2.8 + UP * 0.2
        )

        self.play(
            Write(vector),
            run_time=0.75,
        )

        self.flash(vector, self.BLUE)

        formula = MathTex(
            r"\|\mathbf{x}\|_\infty="
            r"\max_i |x_i|",
            font_size=37,
            color=self.BLACK_TEXT,
        )

        formula.move_to(
            RIGHT * 1.5 + UP * 0.45
        )

        self.play(
            Write(formula),
            run_time=0.8,
        )

        self.flash(formula, self.GREEN)

        result = MathTex(
            r"\|\mathbf{x}\|_\infty=5",
            font_size=39,
            color=self.BLUE,
        )

        result.move_to(
            RIGHT * 1.5 + DOWN * 0.55
        )

        self.play(
            Write(result),
            run_time=0.7,
        )

        self.flash(result, self.BLUE)

        explanation = Text(
            "Only the largest absolute component matters.",
            font_size=22,
            color=self.BLACK_TEXT,
        )

        explanation.move_to(DOWN * 1.8)

        self.play(
            Write(explanation),
            run_time=0.7,
        )

        g.add(
            heading,
            vector,
            formula,
            result,
            explanation,
        )

        self.wait(1)
        self.clear(g)

        # ======================================================
        # 5. FROBENIUS NORM
        # ======================================================

        g = VGroup()

        heading = self.title(
            "The Frobenius norm"
        )

        self.play(
            Write(heading),
            run_time=0.65,
        )

        matrix = MathTex(
            r"A="
            r"\begin{bmatrix}"
            r"1&2\\"
            r"3&4"
            r"\end{bmatrix}",
            font_size=47,
            color=self.BLACK_TEXT,
        )

        matrix.move_to(
            LEFT * 2.5 + UP * 0.2
        )

        self.play(
            Write(matrix),
            run_time=0.75,
        )

        self.flash(matrix, self.BLUE)

        formula = MathTex(
            r"\|A\|_F="
            r"\sqrt{\sum_{i,j}A_{i,j}^{\,2}}",
            font_size=34,
            color=self.BLACK_TEXT,
        )

        formula.move_to(
            RIGHT * 1.65 + UP * 0.35
        )

        self.play(
            Write(formula),
            run_time=0.8,
        )

        self.flash(formula, self.GREEN)

        expanded = MathTex(
            r"\|A\|_F="
            r"\sqrt{1^2+2^2+3^2+4^2}"
            r"=\sqrt{30}",
            font_size=31,
            color=self.BLACK_TEXT,
        )

        expanded.move_to(DOWN * 0.75)

        self.play(
            Write(expanded),
            run_time=0.8,
        )

        self.flash(expanded, self.BLUE)

        explanation = Text(
            "It is analogous to the L2 norm of a vector.",
            font_size=21,
            color=self.BLACK_TEXT,
        )

        explanation.move_to(DOWN * 1.85)

        self.play(
            Write(explanation),
            run_time=0.7,
        )

        g.add(
            heading,
            matrix,
            formula,
            expanded,
            explanation,
        )

        self.wait(1)
        self.clear(g)

        # ======================================================
        # 6. DOT PRODUCT
        # ======================================================

        g = VGroup()

        heading = self.title(
            "Dot product and the angle between vectors"
        )

        self.play(
            Write(heading),
            run_time=0.65,
        )

        plane = self.grid()

        plane.shift(DOWN * 0.15)

        self.play(
            Create(plane),
            run_time=0.65,
        )

        origin = plane.c2p(0, 0)

        x_end = plane.c2p(3.0, 0.8)
        y_end = plane.c2p(1.25, 2.4)

        x_vec = Arrow(
            origin,
            x_end,
            buff=0,
            stroke_width=4,
            color=self.BLACK_TEXT,
        )

        y_vec = Arrow(
            origin,
            y_end,
            buff=0,
            stroke_width=4,
            color=self.BLUE,
        )

        self.play(
            GrowArrow(x_vec),
            run_time=0.6,
        )

        self.flash(x_vec, self.BLACK_TEXT)

        self.play(
            GrowArrow(y_vec),
            run_time=0.6,
        )

        self.flash(y_vec, self.BLUE)

        x_label = MathTex(
            r"\mathbf{x}",
            font_size=29,
            color=self.BLACK_TEXT,
        )

        y_label = MathTex(
            r"\mathbf{y}",
            font_size=29,
            color=self.BLUE,
        )

        x_label.next_to(
            x_end,
            RIGHT,
            buff=0.1,
        )

        y_label.next_to(
            y_end,
            UP,
            buff=0.1,
        )

        self.play(
            Write(x_label),
            Write(y_label),
            run_time=0.5,
        )

        angle = Angle(
            x_vec,
            y_vec,
            radius=0.5,
            color=self.RED,
        )

        theta = MathTex(
            r"\theta",
            font_size=27,
            color=self.RED,
        )

        theta.move_to(
            origin + RIGHT * 0.55 + UP * 0.18
        )

        self.play(
            Create(angle),
            Write(theta),
            run_time=0.6,
        )

        self.flash(angle, self.RED)

        formula = MathTex(
            r"\mathbf{x}^{T}\mathbf{y}"
            r"="
            r"\|\mathbf{x}\|_2"
            r"\|\mathbf{y}\|_2"
            r"\cos\theta",
            font_size=31,
            color=self.BLACK_TEXT,
        )

        formula.to_edge(
            DOWN,
            buff=0.35,
        )

        self.play(
            Write(formula),
            run_time=0.85,
        )

        self.flash(formula, self.GREEN)

        g.add(
            heading,
            plane,
            x_vec,
            y_vec,
            x_label,
            y_label,
            angle,
            theta,
            formula,
        )

        self.wait(1)
        self.clear(g)

        # ======================================================
        # 7. DIAGONAL MATRIX
        # ======================================================

        g = VGroup()

        heading = self.title(
            "A special kind of matrix: diagonal"
        )

        self.play(
            Write(heading),
            run_time=0.65,
        )

        matrix = MathTex(
            r"D="
            r"\begin{bmatrix}"
            r"d_1&0&0\\"
            r"0&d_2&0\\"
            r"0&0&d_3"
            r"\end{bmatrix}",
            font_size=46,
            color=self.BLACK_TEXT,
        )

        matrix.move_to(UP * 0.35)

        self.play(
            Write(matrix),
            run_time=0.8,
        )

        self.flash(matrix, self.BLUE)

        definition = MathTex(
            r"D_{i,j}=0"
            r"\qquad"
            r"\text{for }i\neq j",
            font_size=32,
            color=self.BLACK_TEXT,
        )

        definition.move_to(DOWN * 0.85)

        self.play(
            Write(definition),
            run_time=0.75,
        )

        self.flash(definition, self.GREEN)

        description = Text(
            "All off-diagonal entries are zero.",
            font_size=22,
            color=self.BLACK_TEXT,
        )

        description.move_to(DOWN * 1.8)

        self.play(
            Write(description),
            run_time=0.7,
        )

        g.add(
            heading,
            matrix,
            definition,
            description,
        )

        self.wait(1)
        self.clear(g)

        # ======================================================
        # 8. SUMMARY
        # ======================================================

        heading = self.title(
            "Different norms measure size in different ways"
        )

        self.play(
            Write(heading),
            run_time=0.65,
        )

        l1 = MathTex(
            r"\|\mathbf{x}\|_1=\sum_i|x_i|",
            font_size=31,
            color=self.BLACK_TEXT,
        )

        linf = MathTex(
            r"\|\mathbf{x}\|_\infty=\max_i|x_i|",
            font_size=31,
            color=self.BLACK_TEXT,
        )

        frob = MathTex(
            r"\|A\|_F=\sqrt{\sum_{i,j}A_{i,j}^2}",
            font_size=31,
            color=self.BLACK_TEXT,
        )

        dot = MathTex(
            r"\mathbf{x}^{T}\mathbf{y}"
            r"="
            r"\|\mathbf{x}\|_2"
            r"\|\mathbf{y}\|_2"
            r"\cos\theta",
            font_size=29,
            color=self.BLACK_TEXT,
        )

        summary = VGroup(
            l1,
            linf,
            frob,
            dot,
        ).arrange(
            DOWN,
            buff=0.38,
        )

        summary.move_to(DOWN * 0.2)

        for item in summary:
            self.play(
                Write(item),
                run_time=0.55,
            )
            self.flash(item, self.BLUE)

        final = Text(
            "The choice of norm depends on what structure matters.",
            font_size=22,
            color=self.BLACK_TEXT,
        )

        final.to_edge(
            DOWN,
            buff=0.35,
        )

        self.play(
            Write(final),
            run_time=0.75,
        )

        self.wait(2)


if __name__ == "__main__":
    Figure210().render()
