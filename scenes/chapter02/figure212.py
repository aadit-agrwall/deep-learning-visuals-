from manim import *

config.background_color = WHITE


class Figure212(Scene):

    BLACK_TEXT = "#111111"
    BLUE = "#1769AA"
    GREEN = "#16855B"
    RED = "#C43D3D"
    PURPLE = "#7048A8"
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
                scale_factor=1.06,
                rate_func=there_and_back,
            ),
            run_time=0.35,
        )

    def clear(self, group):
        self.play(
            FadeOut(group),
            run_time=0.4,
        )

    def plane(self):
        return NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=8,
            y_length=5.2,
            background_line_style={
                "stroke_color": self.GRID,
                "stroke_width": 1,
                "stroke_opacity": 0.22,
            },
            axis_config={
                "color": "#777777",
                "stroke_width": 1.2,
                "include_tip": False,
            },
        )

    # --------------------------------------------------
    # Main scene
    # --------------------------------------------------

    def construct(self):

        # ==================================================
        # 1. WHY DECOMPOSE A MATRIX?
        # ==================================================

        g = VGroup()

        h = self.heading("Eigendecomposition")

        self.play(
            Write(h),
            run_time=0.6,
        )

        statement = Text(
            "A matrix can be decomposed into simpler components.",
            font_size=23,
            color=self.BLACK_TEXT,
        )

        statement.move_to(UP * 0.65)

        self.play(
            Write(statement),
            run_time=0.7,
        )

        self.flash(statement, self.BLUE)

        matrix = MathTex(
            r"A"
            r"\quad\longrightarrow\quad"
            r"\text{eigenvectors}"
            r"+"
            r"\text{eigenvalues}",
            font_size=34,
            color=self.BLACK_TEXT,
        )

        matrix.move_to(DOWN * 0.25)

        self.play(
            Write(matrix),
            run_time=0.8,
        )

        self.flash(matrix, self.GREEN)

        analogy = Text(
            "Like factoring an integer into prime factors.",
            font_size=21,
            color=self.GREY,
        )

        analogy.move_to(DOWN * 1.45)

        self.play(
            Write(analogy),
            run_time=0.65,
        )

        example = MathTex(
            r"12=2\times2\times3",
            font_size=35,
            color=self.BLACK_TEXT,
        )

        example.move_to(DOWN * 2.15)

        self.play(
            Write(example),
            run_time=0.65,
        )

        self.flash(example, self.BLUE)

        g.add(
            h,
            statement,
            matrix,
            analogy,
            example,
        )

        self.wait(1)
        self.clear(g)

        # ==================================================
        # 2. EIGENVECTOR GEOMETRIC IDEA
        # ==================================================

        g = VGroup()

        h = self.heading("An eigenvector keeps its direction")

        self.play(
            Write(h),
            run_time=0.6,
        )

        p = self.plane()
        p.shift(DOWN * 0.15)

        self.play(
            Create(p),
            run_time=0.55,
        )

        origin = p.c2p(0, 0)

        v_end = p.c2p(2.0, 1.0)
        Av_end = p.c2p(3.0, 1.5)

        v = Arrow(
            origin,
            v_end,
            buff=0,
            stroke_width=4,
            color=self.BLUE,
        )

        Av = Arrow(
            origin,
            Av_end,
            buff=0,
            stroke_width=4,
            color=self.GREEN,
        )

        self.play(
            GrowArrow(v),
            run_time=0.65,
        )

        self.flash(v, self.BLUE)

        label_v = MathTex(
            r"\mathbf v",
            font_size=30,
            color=self.BLUE,
        )

        label_v.next_to(
            v_end,
            RIGHT,
            buff=0.1,
        )

        self.play(
            Write(label_v),
            run_time=0.45,
        )

        transform = MathTex(
            r"A\mathbf v",
            font_size=30,
            color=self.GREEN,
        )

        transform.move_to(
            RIGHT * 2.8 + DOWN * 2.15
        )

        self.play(
            GrowArrow(Av),
            run_time=0.75,
        )

        self.flash(Av, self.GREEN)

        label_Av = MathTex(
            r"A\mathbf v",
            font_size=30,
            color=self.GREEN,
        )

        label_Av.next_to(
            Av_end,
            RIGHT,
            buff=0.1,
        )

        self.play(
            Write(label_Av),
            run_time=0.45,
        )

        equation = MathTex(
            r"A\mathbf v=\lambda\mathbf v",
            font_size=38,
            color=self.BLACK_TEXT,
        )

        equation.to_edge(
            DOWN,
            buff=0.35,
        )

        self.play(
            Write(equation),
            run_time=0.75,
        )

        self.flash(equation, self.RED)

        g.add(
            h,
            p,
            v,
            Av,
            label_v,
            label_Av,
            equation,
        )

        self.wait(1)
        self.clear(g)

        # ==================================================
        # 3. EIGENVALUE = SCALE FACTOR
        # ==================================================

        g = VGroup()

        h = self.heading("The eigenvalue tells us the scale change")

        self.play(
            Write(h),
            run_time=0.6,
        )

        original = MathTex(
            r"\mathbf v",
            font_size=40,
            color=self.BLUE,
        )

        scaled = MathTex(
            r"\lambda\mathbf v",
            font_size=40,
            color=self.GREEN,
        )

        original.move_to(LEFT * 2.4 + UP * 0.3)
        scaled.move_to(RIGHT * 2.4 + UP * 0.3)

        self.play(
            Write(original),
            run_time=0.55,
        )

        self.flash(original, self.BLUE)

        arrow = Arrow(
            original.get_right(),
            scaled.get_left(),
            buff=0.5,
            color=self.GREY,
            stroke_width=2,
        )

        self.play(
            GrowArrow(arrow),
            run_time=0.45,
        )

        self.play(
            Write(scaled),
            run_time=0.6,
        )

        self.flash(scaled, self.GREEN)

        explanation = Text(
            "The direction stays the same; only the magnitude changes.",
            font_size=21,
            color=self.BLACK_TEXT,
        )

        explanation.move_to(
            DOWN * 0.75
        )

        self.play(
            Write(explanation),
            run_time=0.7,
        )

        positive = MathTex(
            r"\lambda>1"
            r"\quad\Rightarrow\quad"
            r"\text{stretches}",
            font_size=29,
            color=self.BLUE,
        )

        negative = MathTex(
            r"0<\lambda<1"
            r"\quad\Rightarrow\quad"
            r"\text{shrinks}",
            font_size=29,
            color=self.GREEN,
        )

        positive.move_to(
            LEFT * 2.0 + DOWN * 1.75
        )

        negative.move_to(
            RIGHT * 2.0 + DOWN * 1.75
        )

        self.play(
            Write(positive),
            run_time=0.55,
        )

        self.flash(positive, self.BLUE)

        self.play(
            Write(negative),
            run_time=0.55,
        )

        self.flash(negative, self.GREEN)

        g.add(
            h,
            original,
            scaled,
            arrow,
            explanation,
            positive,
            negative,
        )

        self.wait(1)
        self.clear(g)

        # ==================================================
        # 4. RESCALING EIGENVECTORS
        # ==================================================

        g = VGroup()

        h = self.heading("Rescaling an eigenvector does not change its eigenvalue")

        self.play(
            Write(h),
            run_time=0.65,
        )

        left = MathTex(
            r"A\mathbf v=\lambda\mathbf v",
            font_size=37,
            color=self.BLUE,
        )

        right = MathTex(
            r"A(s\mathbf v)=\lambda(s\mathbf v)",
            font_size=37,
            color=self.GREEN,
        )

        left.move_to(
            LEFT * 2.25 + UP * 0.25
        )

        right.move_to(
            RIGHT * 2.15 + UP * 0.25
        )

        self.play(
            Write(left),
            run_time=0.65,
        )

        self.flash(left, self.BLUE)

        arrow = Arrow(
            left.get_right(),
            right.get_left(),
            buff=0.35,
            color=self.GREY,
            stroke_width=2,
        )

        self.play(
            GrowArrow(arrow),
            run_time=0.45,
        )

        self.play(
            Write(right),
            run_time=0.75,
        )

        self.flash(right, self.GREEN)

        condition = MathTex(
            r"s\in\mathbb R,\qquad s\neq0",
            font_size=31,
            color=self.BLACK_TEXT,
        )

        condition.move_to(DOWN * 0.85)

        self.play(
            Write(condition),
            run_time=0.6,
        )

        note = Text(
            "So eigenvectors are usually normalized to unit length.",
            font_size=21,
            color=self.BLACK_TEXT,
        )

        note.move_to(DOWN * 1.65)

        self.play(
            Write(note),
            run_time=0.65,
        )

        unit = MathTex(
            r"\|\mathbf v\|_2=1",
            font_size=34,
            color=self.RED,
        )

        unit.move_to(DOWN * 2.3)

        self.play(
            Write(unit),
            run_time=0.55,
        )

        self.flash(unit, self.RED)

        g.add(
            h,
            left,
            right,
            arrow,
            condition,
            note,
            unit,
        )

        self.wait(1)
        self.clear(g)

        # ==================================================
        # 5. MULTIPLE EIGENVECTORS
        # ==================================================

        g = VGroup()

        h = self.heading("A matrix can have many eigenvectors")

        self.play(
            Write(h),
            run_time=0.6,
        )

        v1 = MathTex(
            r"\mathbf v^{(1)}",
            font_size=34,
            color=self.BLUE,
        )

        v2 = MathTex(
            r"\mathbf v^{(2)}",
            font_size=34,
            color=self.GREEN,
        )

        v3 = MathTex(
            r"\mathbf v^{(3)}",
            font_size=34,
            color=self.PURPLE,
        )

        vectors = VGroup(
            v1,
            v2,
            v3,
        ).arrange(
            RIGHT,
            buff=1.15,
        )

        vectors.move_to(UP * 0.45)

        self.play(
            Write(v1),
            run_time=0.45,
        )

        self.flash(v1, self.BLUE)

        self.play(
            Write(v2),
            run_time=0.45,
        )

        self.flash(v2, self.GREEN)

        self.play(
            Write(v3),
            run_time=0.45,
        )

        self.flash(v3, self.PURPLE)

        eigenvalues = MathTex(
            r"\lambda_1,\qquad\lambda_2,\qquad\lambda_3",
            font_size=33,
            color=self.RED,
        )

        eigenvalues.move_to(
            DOWN * 0.65
        )

        self.play(
            Write(eigenvalues),
            run_time=0.7,
        )

        self.flash(eigenvalues, self.RED)

        statement = MathTex(
            r"A\mathbf v^{(i)}"
            r"="
            r"\lambda_i\mathbf v^{(i)}",
            font_size=36,
            color=self.BLACK_TEXT,
        )

        statement.move_to(
            DOWN * 1.65
        )

        self.play(
            Write(statement),
            run_time=0.7,
        )

        self.flash(statement, self.BLUE)

        g.add(
            h,
            vectors,
            eigenvalues,
            statement,
        )

        self.wait(1)
        self.clear(g)

        # ==================================================
        # 6. BUILDING V
        # ==================================================

        g = VGroup()

        h = self.heading("Put the eigenvectors into a matrix")

        self.play(
            Write(h),
            run_time=0.6,
        )

        vector_list = MathTex(
            r"V="
            r"\left[\,"
            r"\mathbf v^{(1)}"
            r",\;"
            r"\mathbf v^{(2)}"
            r",\;"
            r"\cdots"
            r",\;"
            r"\mathbf v^{(n)}"
            r"\,\right]",
            font_size=34,
            color=self.BLACK_TEXT,
        )

        vector_list.move_to(
            UP * 0.35
        )

        self.play(
            Write(vector_list),
            run_time=0.85,
        )

        self.flash(vector_list, self.BLUE)

        description = Text(
            "One eigenvector per column.",
            font_size=22,
            color=self.BLACK_TEXT,
        )

        description.move_to(
            DOWN * 0.65
        )

        self.play(
            Write(description),
            run_time=0.6,
        )

        self.flash(description, self.GREEN)

        eigenvalue_vector = MathTex(
            r"\boldsymbol{\lambda}"
            r"="
            r"\begin{bmatrix}"
            r"\lambda_1\\"
            r"\lambda_2\\"
            r"\vdots\\"
            r"\lambda_n"
            r"\end{bmatrix}",
            font_size=37,
            color=self.RED,
        )

        eigenvalue_vector.move_to(
            DOWN * 1.55
        )

        self.play(
            Write(eigenvalue_vector),
            run_time=0.8,
        )

        self.flash(eigenvalue_vector, self.RED)

        g.add(
            h,
            vector_list,
            description,
            eigenvalue_vector,
        )

        self.wait(1)
        self.clear(g)

        # ==================================================
        # 7. AV = V LAMBDA
        # ==================================================

        g = VGroup()

        h = self.heading("Eigendecomposition: the key relationship")

        self.play(
            Write(h),
            run_time=0.6,
        )

        A = MathTex(
            r"A",
            font_size=46,
            color=self.BLACK_TEXT,
        )

        V = MathTex(
            r"V",
            font_size=46,
            color=self.BLUE,
        )

        AV = MathTex(
            r"AV",
            font_size=46,
            color=self.BLACK_TEXT,
        )

        A.move_to(LEFT * 3.0 + UP * 0.15)
        V.move_to(LEFT * 1.7 + UP * 0.15)

        self.play(
            Write(A),
            run_time=0.45,
        )

        self.flash(A, self.BLACK_TEXT)

        self.play(
            Write(V),
            run_time=0.45,
        )

        self.flash(V, self.BLUE)

        left_product = MathTex(
            r"AV",
            font_size=46,
            color=self.BLACK_TEXT,
        )

        left_product.move_to(
            LEFT * 2.35 + DOWN * 0.85
        )

        self.play(
            Write(left_product),
            run_time=0.5,
        )

        equals = MathTex(
            r"=",
            font_size=45,
            color=self.BLACK_TEXT,
        )

        equals.move_to(
            ORIGIN + DOWN * 0.85
        )

        self.play(
            Write(equals),
            run_time=0.4,
        )

        V_right = MathTex(
            r"V",
            font_size=46,
            color=self.BLUE,
        )

        Lambda = MathTex(
            r"\Lambda",
            font_size=46,
            color=self.RED,
        )

        V_right.move_to(
            RIGHT * 1.25 + DOWN * 0.85
        )

        Lambda.move_to(
            RIGHT * 2.5 + DOWN * 0.85
        )

        self.play(
            Write(V_right),
            run_time=0.45,
        )

        self.flash(V_right, self.BLUE)

        self.play(
            Write(Lambda),
            run_time=0.45,
        )

        self.flash(Lambda, self.RED)

        final = MathTex(
            r"\boxed{AV=V\Lambda}",
            font_size=42,
            color=self.GREEN,
        )

        final.move_to(
            DOWN * 2.0
        )

        self.play(
            Write(final),
            run_time=0.8,
        )

        self.flash(final, self.GREEN)

        note = Text(
            "A transforms each eigenvector only by its corresponding eigenvalue.",
            font_size=20,
            color=self.BLACK_TEXT,
        )

        note.to_edge(
            DOWN,
            buff=0.32,
        )

        self.play(
            Write(note),
            run_time=0.7,
        )

        g.add(
            h,
            A,
            V,
            left_product,
            equals,
            V_right,
            Lambda,
            final,
            note,
        )

        self.wait(2)


if __name__ == "__main__":
    Figure212().render()
