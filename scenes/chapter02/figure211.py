from manim import *

config.background_color = WHITE


class Figure211(Scene):

    BLACK_TEXT = "#111111"
    BLUE = "#1769AA"
    GREEN = "#16855B"
    RED = "#C43D3D"
    GRID = "#B8B8B8"
    GREY = "#666666"

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def heading(self, text):
        return Text(
            text,
            font_size=28,
            color=self.BLACK_TEXT,
        ).to_edge(UP, buff=0.28)

    def flash(self, mob, color=None):
        if color is None:
            color = self.BLUE

        self.play(
            Indicate(
                mob,
                color=color,
                scale_factor=1.05,
                rate_func=there_and_back,
            ),
            run_time=0.35,
        )

    def clear(self, group):
        self.play(
            FadeOut(group),
            run_time=0.4,
        )

    # --------------------------------------------------
    # Scene
    # --------------------------------------------------

    def construct(self):

        # ==================================================
        # 1. DIAGONAL MATRIX MULTIPLICATION
        # ==================================================

        g = VGroup()

        h = self.heading("Diagonal matrices scale components independently")

        self.play(Write(h), run_time=0.6)

        D = MathTex(
            r"\operatorname{diag}(\mathbf v)"
            r"="
            r"\begin{bmatrix}"
            r"v_1&0&0\\"
            r"0&v_2&0\\"
            r"0&0&v_3"
            r"\end{bmatrix}",
            font_size=34,
            color=self.BLACK_TEXT,
        )

        x = MathTex(
            r"\mathbf x="
            r"\begin{bmatrix}"
            r"x_1\\x_2\\x_3"
            r"\end{bmatrix}",
            font_size=38,
            color=self.BLACK_TEXT,
        )

        D.move_to(LEFT * 2.5 + UP * 0.25)
        x.move_to(RIGHT * 2.3 + UP * 0.25)

        self.play(
            Write(D),
            Write(x),
            run_time=0.8,
        )

        self.flash(D, self.BLUE)
        self.flash(x, self.GREEN)

        arrow = Arrow(
            D.get_right(),
            x.get_left(),
            buff=0.35,
            color=self.GREY,
            stroke_width=2,
        )

        self.play(
            GrowArrow(arrow),
            run_time=0.45,
        )

        result = MathTex(
            r"\operatorname{diag}(\mathbf v)\mathbf x"
            r"="
            r"\begin{bmatrix}"
            r"v_1x_1\\"
            r"v_2x_2\\"
            r"v_3x_3"
            r"\end{bmatrix}",
            font_size=37,
            color=self.BLUE,
        )

        result.move_to(DOWN * 1.05)

        self.play(
            Write(result),
            run_time=0.8,
        )

        self.flash(result, self.BLUE)

        hadamard = MathTex(
            r"="
            r"\mathbf v\odot\mathbf x",
            font_size=32,
            color=self.GREEN,
        )

        hadamard.next_to(
            result,
            DOWN,
            buff=0.35,
        )

        self.play(
            Write(hadamard),
            run_time=0.55,
        )

        g.add(h, D, x, arrow, result, hadamard)

        self.wait(1)
        self.clear(g)

        # ==================================================
        # 2. DIAGONAL INVERSE
        # ==================================================

        g = VGroup()

        h = self.heading("Inverse of a diagonal matrix")

        self.play(Write(h), run_time=0.6)

        original = MathTex(
            r"D="
            r"\begin{bmatrix}"
            r"v_1&0&0\\"
            r"0&v_2&0\\"
            r"0&0&v_3"
            r"\end{bmatrix}",
            font_size=38,
            color=self.BLACK_TEXT,
        )

        inverse = MathTex(
            r"D^{-1}="
            r"\begin{bmatrix}"
            r"\frac1{v_1}&0&0\\"
            r"0&\frac1{v_2}&0\\"
            r"0&0&\frac1{v_3}"
            r"\end{bmatrix}",
            font_size=36,
            color=self.BLUE,
        )

        original.move_to(LEFT * 2.3 + UP * 0.25)
        inverse.move_to(RIGHT * 2.3 + UP * 0.25)

        self.play(
            Write(original),
            run_time=0.7,
        )

        self.flash(original, self.BLUE)

        arrow = Arrow(
            original.get_right(),
            inverse.get_left(),
            buff=0.4,
            color=self.GREY,
            stroke_width=2,
        )

        self.play(
            GrowArrow(arrow),
            run_time=0.45,
        )

        self.play(
            Write(inverse),
            run_time=0.8,
        )

        self.flash(inverse, self.GREEN)

        condition = MathTex(
            r"v_i\neq0\quad\text{for every }i",
            font_size=31,
            color=self.RED,
        )

        condition.move_to(DOWN * 1.25)

        self.play(
            Write(condition),
            run_time=0.65,
        )

        note = Text(
            "The inverse exists only when every diagonal entry is nonzero.",
            font_size=20,
            color=self.BLACK_TEXT,
        )

        note.move_to(DOWN * 2.05)

        self.play(
            Write(note),
            run_time=0.65,
        )

        g.add(h, original, inverse, arrow, condition, note)

        self.wait(1)
        self.clear(g)

        # ==================================================
        # 3. RECTANGULAR DIAGONAL MATRIX
        # ==================================================

        g = VGroup()

        h = self.heading("Rectangular diagonal matrices")

        self.play(Write(h), run_time=0.6)

        D = MathTex(
            r"D="
            r"\begin{bmatrix}"
            r"d_1&0\\"
            r"0&d_2\\"
            r"0&0"
            r"\end{bmatrix}",
            font_size=40,
            color=self.BLACK_TEXT,
        )

        x = MathTex(
            r"\mathbf x="
            r"\begin{bmatrix}"
            r"x_1\\x_2"
            r"\end{bmatrix}",
            font_size=40,
            color=self.BLACK_TEXT,
        )

        result = MathTex(
            r"D\mathbf x="
            r"\begin{bmatrix}"
            r"d_1x_1\\"
            r"d_2x_2\\"
            r"0"
            r"\end{bmatrix}",
            font_size=40,
            color=self.BLUE,
        )

        D.move_to(LEFT * 3.0 + UP * 0.15)
        x.move_to(ORIGIN + UP * 0.15)
        result.move_to(RIGHT * 2.8 + UP * 0.15)

        self.play(
            Write(D),
            Write(x),
            run_time=0.75,
        )

        self.flash(D, self.BLUE)

        arrow1 = Arrow(
            D.get_right(),
            x.get_left(),
            buff=0.35,
            color=self.GREY,
            stroke_width=2,
        )

        self.play(
            GrowArrow(arrow1),
            run_time=0.4,
        )

        arrow2 = Arrow(
            x.get_right(),
            result.get_left(),
            buff=0.35,
            color=self.GREY,
            stroke_width=2,
        )

        self.play(
            GrowArrow(arrow2),
            run_time=0.4,
        )

        self.play(
            Write(result),
            run_time=0.75,
        )

        self.flash(result, self.GREEN)

        note = Text(
            "Extra dimensions can appear as zeros.",
            font_size=21,
            color=self.BLACK_TEXT,
        )

        note.move_to(DOWN * 1.55)

        self.play(
            Write(note),
            run_time=0.65,
        )

        g.add(h, D, x, result, arrow1, arrow2, note)

        self.wait(1)
        self.clear(g)

        # ==================================================
        # 4. SYMMETRIC MATRIX
        # ==================================================

        g = VGroup()

        h = self.heading("Symmetric matrices")

        self.play(Write(h), run_time=0.6)

        A = MathTex(
            r"A="
            r"\begin{bmatrix}"
            r"a&b&c\\"
            r"b&d&e\\"
            r"c&e&f"
            r"\end{bmatrix}",
            font_size=43,
            color=self.BLACK_TEXT,
        )

        At = MathTex(
            r"A^T="
            r"\begin{bmatrix}"
            r"a&b&c\\"
            r"b&d&e\\"
            r"c&e&f"
            r"\end{bmatrix}",
            font_size=43,
            color=self.BLUE,
        )

        A.move_to(LEFT * 2.4 + UP * 0.15)
        At.move_to(RIGHT * 2.4 + UP * 0.15)

        self.play(
            Write(A),
            run_time=0.7,
        )

        self.flash(A, self.BLUE)

        arrow = Arrow(
            A.get_right(),
            At.get_left(),
            buff=0.45,
            color=self.GREY,
            stroke_width=2,
        )

        self.play(
            GrowArrow(arrow),
            run_time=0.45,
        )

        self.play(
            Write(At),
            run_time=0.7,
        )

        self.flash(At, self.GREEN)

        equation = MathTex(
            r"A=A^T",
            font_size=38,
            color=self.RED,
        )

        equation.move_to(DOWN * 1.35)

        self.play(
            Write(equation),
            run_time=0.6,
        )

        g.add(h, A, At, arrow, equation)

        self.wait(1)
        self.clear(g)

        # ==================================================
        # 5. UNIT VECTOR
        # ==================================================

        g = VGroup()

        h = self.heading("Unit vectors")

        self.play(Write(h), run_time=0.6)

        plane = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=7,
            y_length=4.2,
            background_line_style={
                "stroke_color": self.GRID,
                "stroke_width": 1,
                "stroke_opacity": 0.20,
            },
            axis_config={
                "color": "#777777",
                "stroke_width": 1.2,
                "include_tip": False,
            },
        )

        plane.shift(DOWN * 0.15)

        self.play(
            Create(plane),
            run_time=0.55,
        )

        origin = plane.c2p(0, 0)
        endpoint = plane.c2p(0.8, 0.6)

        vec = Arrow(
            origin,
            endpoint,
            buff=0,
            color=self.BLUE,
            stroke_width=4,
        )

        label = MathTex(
            r"\|\mathbf{x}\|_2=1",
            font_size=33,
            color=self.BLACK_TEXT,
        )

        label.to_edge(DOWN, buff=0.4)

        self.play(
            GrowArrow(vec),
            run_time=0.7,
        )

        self.flash(vec, self.BLUE)

        self.play(
            Write(label),
            run_time=0.65,
        )

        self.flash(label, self.GREEN)

        g.add(h, plane, vec, label)

        self.wait(1)
        self.clear(g)

        # ==================================================
        # 6. ORTHOGONAL VECTORS
        # ==================================================

        g = VGroup()

        h = self.heading("Orthogonal vectors")

        self.play(Write(h), run_time=0.6)

        plane = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-2.5, 2.5, 1],
            x_length=7,
            y_length=5,
            background_line_style={
                "stroke_color": self.GRID,
                "stroke_width": 1,
                "stroke_opacity": 0.20,
            },
            axis_config={
                "color": "#777777",
                "stroke_width": 1.2,
                "include_tip": False,
            },
        )

        plane.shift(DOWN * 0.1)

        self.play(
            Create(plane),
            run_time=0.55,
        )

        origin = plane.c2p(0, 0)

        vx_end = plane.c2p(2.2, 0)
        vy_end = plane.c2p(0, 1.8)

        vx = Arrow(
            origin,
            vx_end,
            buff=0,
            color=self.BLACK_TEXT,
            stroke_width=4,
        )

        vy = Arrow(
            origin,
            vy_end,
            buff=0,
            color=self.BLUE,
            stroke_width=4,
        )

        self.play(
            GrowArrow(vx),
            run_time=0.55,
        )

        self.flash(vx, self.BLACK_TEXT)

        self.play(
            GrowArrow(vy),
            run_time=0.55,
        )

        self.flash(vy, self.BLUE)

        right_angle = RightAngle(
            vx,
            vy,
            length=0.35,
            color=self.RED,
        )

        self.play(
            Create(right_angle),
            run_time=0.45,
        )

        self.flash(right_angle, self.RED)

        equation = MathTex(
            r"\mathbf{x}^T\mathbf{y}=0",
            font_size=36,
            color=self.BLACK_TEXT,
        )

        equation.to_edge(DOWN, buff=0.42)

        self.play(
            Write(equation),
            run_time=0.65,
        )

        g.add(h, plane, vx, vy, right_angle, equation)

        self.wait(1)
        self.clear(g)

        # ==================================================
        # 7. ORTHONORMAL VECTORS
        # ==================================================

        g = VGroup()

        h = self.heading("Orthonormal vectors")

        self.play(Write(h), run_time=0.6)

        left = MathTex(
            r"\mathbf{x}^T\mathbf{y}=0",
            font_size=34,
            color=self.BLUE,
        )

        right = MathTex(
            r"\|\mathbf{x}\|_2"
            r"="
            r"\|\mathbf{y}\|_2"
            r"=1",
            font_size=34,
            color=self.GREEN,
        )

        left.move_to(LEFT * 2.3 + UP * 0.25)
        right.move_to(RIGHT * 2.2 + UP * 0.25)

        self.play(
            Write(left),
            run_time=0.65,
        )

        self.flash(left, self.BLUE)

        self.play(
            Write(right),
            run_time=0.65,
        )

        self.flash(right, self.GREEN)

        brace = Brace(
            VGroup(left, right),
            DOWN,
            buff=0.3,
        )

        description = Text(
            "orthogonal + unit length",
            font_size=22,
            color=self.BLACK_TEXT,
        )

        description.next_to(
            brace,
            DOWN,
            buff=0.25,
        )

        self.play(
            GrowFromCenter(brace),
            Write(description),
            run_time=0.65,
        )

        g.add(h, left, right, brace, description)

        self.wait(1)
        self.clear(g)

        # ==================================================
        # 8. ORTHOGONAL MATRIX
        # ==================================================

        g = VGroup()

        h = self.heading("Orthogonal matrices")

        self.play(Write(h), run_time=0.6)

        A = MathTex(
            r"A="
            r"\begin{bmatrix}"
            r"0&-1\\"
            r"1&0"
            r"\end{bmatrix}",
            font_size=48,
            color=self.BLACK_TEXT,
        )

        A.move_to(LEFT * 3.0 + UP * 0.15)

        self.play(
            Write(A),
            run_time=0.7,
        )

        self.flash(A, self.BLUE)

        equation = MathTex(
            r"A^T A=AA^T=I",
            font_size=38,
            color=self.GREEN,
        )

        equation.move_to(
            RIGHT * 1.9 + UP * 0.35
        )

        self.play(
            Write(equation),
            run_time=0.75,
        )

        self.flash(equation, self.GREEN)

        inverse = MathTex(
            r"A^{-1}=A^T",
            font_size=39,
            color=self.RED,
        )

        inverse.move_to(
            RIGHT * 1.9 + DOWN * 0.75
        )

        self.play(
            Write(inverse),
            run_time=0.7,
        )

        self.flash(inverse, self.RED)

        note = Text(
            "Rows and columns are mutually orthonormal.",
            font_size=21,
            color=self.BLACK_TEXT,
        )

        note.to_edge(DOWN, buff=0.38)

        self.play(
            Write(note),
            run_time=0.65,
        )

        g.add(h, A, equation, inverse, note)

        self.wait(2)


if __name__ == "__main__":
    Figure211().render()
