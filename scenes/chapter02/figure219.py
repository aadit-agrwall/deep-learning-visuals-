from manim import *


class Figure219(Scene):
    def construct(self):

        # ============================================================
        # STYLE
        # ============================================================
        self.camera.background_color = WHITE

        BLACK_C = "#111111"
        GREY_C = "#D0D0D0"
        BLUE_C = "#2563EB"
        GREEN_C = "#16A34A"
        RED_C = "#DC2626"
        ORANGE_C = "#EA580C"
        PURPLE_C = "#7C3AED"

        # ============================================================
        # HELPERS
        # ============================================================
        def flash(obj, color=BLUE_C):
            self.play(
                Circumscribe(
                    obj,
                    color=color,
                    buff=0.10,
                    stroke_width=3.5,
                    fade_out=True,
                ),
                run_time=0.50,
            )

        def write(obj, runtime=0.65):
            self.play(Write(obj), run_time=runtime)

        def clear_all(*objects):
            objs = [o for o in objects if o is not None]
            if objs:
                self.play(
                    *[FadeOut(o) for o in objs],
                    run_time=0.45,
                )

        def label(text, y=3.0, size=22):
            t = Text(
                text,
                font="Arial",
                font_size=size,
                weight=BOLD,
                color=BLACK_C,
            )
            t.move_to([0, y, 0])
            return t

        def eq_number(number, equation):
            n = MathTex(
                rf"\text{{({number})}}",
                color=GREY_C,
                font_size=24,
            )
            n.next_to(equation, RIGHT, buff=0.38)
            return n

        # ============================================================
        # SUBTLE BACKGROUND GRID
        # ============================================================
        grid = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-4, 4, 1],
            background_line_style={
                "stroke_color": GREY_C,
                "stroke_width": 1,
                "stroke_opacity": 0.12,
            },
            axis_config={
                "stroke_opacity": 0,
            },
        )

        self.add(grid)

        # ============================================================
        # HEADER
        # ============================================================
        heading = Text(
            "PCA — Minimizing Reconstruction Error",
            font="Arial",
            font_size=30,
            weight=BOLD,
            color=BLACK_C,
        )
        heading.to_edge(UP, buff=0.30)

        line = Line(
            LEFT * 4.7,
            RIGHT * 4.7,
            color=BLACK_C,
            stroke_width=1.2,
        )
        line.next_to(heading, DOWN, buff=0.13)

        self.play(
            FadeIn(heading, shift=DOWN * 0.1),
            Create(line),
            run_time=0.75,
        )

        self.wait(0.4)

        # ============================================================
        # STEP 1 — EXPAND THE SQUARED NORM
        # ============================================================
        step1 = label(
            "Expand the squared reconstruction error",
            y=2.65,
        )

        self.play(FadeIn(step1), run_time=0.45)

        eq57 = MathTex(
            r"x^{T}x"
            r"-x^{T}g(c)"
            r"-g(c)^{T}x"
            r"+g(c)^{T}g(c)",
            color=BLACK_C,
            font_size=40,
        )
        eq57.move_to(UP * 1.45)

        num57 = eq_number("2.57", eq57)

        write(eq57, 0.8)
        self.play(FadeIn(num57), run_time=0.3)

        flash(eq57, BLUE_C)

        note57 = Text(
            "Expand the product",
            font="Arial",
            font_size=19,
            color=GREY_C,
        )
        note57.move_to(DOWN * 0.15)

        self.play(FadeIn(note57), run_time=0.35)

        self.wait(0.7)

        # ============================================================
        # STEP 2 — DISTRIBUTIVE PROPERTY
        # ============================================================
        clear_all(step1, eq57, num57, note57)

        step2 = label(
            "Use the distributive property",
            y=2.65,
        )

        self.play(FadeIn(step2), run_time=0.4)

        eq58 = MathTex(
            r"x^{T}x"
            r"-2x^{T}g(c)"
            r"+g(c)^{T}g(c)",
            color=BLACK_C,
            font_size=42,
        )
        eq58.move_to(UP * 1.35)

        num58 = eq_number("2.58", eq58)

        write(eq58, 0.75)
        self.play(FadeIn(num58), run_time=0.3)

        flash(eq58, ORANGE_C)

        note58 = Text(
            "The two cross terms are equal scalars",
            font="Arial",
            font_size=19,
            color=GREY_C,
        )
        note58.move_to(DOWN * 0.10)

        self.play(FadeIn(note58), run_time=0.4)

        self.wait(0.7)

        # ============================================================
        # STEP 3 — REMOVE CONSTANT TERM
        # ============================================================
        clear_all(step2, eq58, num58, note58)

        step3 = label(
            "Drop terms that do not depend on c",
            y=2.65,
        )

        self.play(FadeIn(step3), run_time=0.4)

        constant = MathTex(
            r"x^{T}x",
            color=GREY_C,
            font_size=40,
        )
        constant.move_to(LEFT * 3.0 + UP * 1.0)

        constant_note = Text(
            "constant",
            font="Arial",
            font_size=18,
            color=GREY_C,
        )
        constant_note.next_to(constant, DOWN, buff=0.15)

        self.play(Write(constant), FadeIn(constant_note), run_time=0.45)

        flash(constant, GREY_C)

        eq59 = MathTex(
            r"c^{*}"
            r"="
            r"\operatorname*{arg\,min}_{c}"
            r"\left("
            r"-2x^{T}g(c)"
            r"+g(c)^{T}g(c)"
            r"\right)",
            color=BLACK_C,
            font_size=38,
        )
        eq59.move_to(DOWN * 0.35)

        num59 = eq_number("2.59", eq59)

        write(eq59, 0.8)
        self.play(FadeIn(num59), run_time=0.3)

        flash(eq59, GREEN_C)

        self.wait(0.8)

        # ============================================================
        # STEP 4 — SUBSTITUTE g(c) = Dc
        # ============================================================
        clear_all(
            step3,
            constant,
            constant_note,
            eq59,
            num59,
        )

        step4 = label(
            "Substitute the decoder definition  g(c) = Dc",
            y=2.65,
        )

        self.play(FadeIn(step4), run_time=0.4)

        decoder = MathTex(
            r"g(c)=Dc",
            color=GREEN_C,
            font_size=34,
        )
        decoder.move_to(UP * 1.55)

        write(decoder, 0.5)
        flash(decoder, GREEN_C)

        eq60 = MathTex(
            r"c^{*}"
            r"="
            r"\operatorname*{arg\,min}_{c}"
            r"\left("
            r"-2x^{T}Dc"
            r"+c^{T}D^{T}Dc"
            r"\right)",
            color=BLACK_C,
            font_size=37,
        )
        eq60.move_to(DOWN * 0.25)

        num60 = eq_number("2.60", eq60)

        write(eq60, 0.8)
        self.play(FadeIn(num60), run_time=0.3)

        flash(eq60, BLUE_C)

        self.wait(0.7)

        # ============================================================
        # STEP 5 — D^T D = I
        # ============================================================
        clear_all(step4, decoder, eq60, num60)

        step5 = label(
            "Use the orthogonality and unit-norm constraints",
            y=2.65,
        )

        self.play(FadeIn(step5), run_time=0.4)

        constraint = MathTex(
            r"D^{T}D=I",
            color=GREEN_C,
            font_size=38,
        )
        constraint.move_to(UP * 1.55)

        write(constraint, 0.55)
        flash(constraint, GREEN_C)

        eq61 = MathTex(
            r"c^{*}"
            r"="
            r"\operatorname*{arg\,min}_{c}"
            r"\left("
            r"-2x^{T}Dc"
            r"+c^{T}Ic"
            r"\right)",
            color=BLACK_C,
            font_size=38,
        )
        eq61.move_to(DOWN * 0.25)

        num61 = eq_number("2.61", eq61)

        write(eq61, 0.75)
        self.play(FadeIn(num61), run_time=0.3)

        flash(eq61, BLUE_C)

        self.wait(0.6)

        # ============================================================
        # STEP 6 — IDENTITY DISAPPEARS
        # ============================================================
        clear_all(step5, constraint, eq61, num61)

        step6 = label(
            "Multiplication by the identity changes nothing",
            y=2.65,
        )

        self.play(FadeIn(step6), run_time=0.4)

        eq62 = MathTex(
            r"c^{*}"
            r"="
            r"\operatorname*{arg\,min}_{c}"
            r"\left("
            r"-2x^{T}Dc"
            r"+c^{T}c"
            r"\right)",
            color=BLACK_C,
            font_size=40,
        )
        eq62.move_to(UP * 0.85)

        num62 = eq_number("2.62", eq62)

        write(eq62, 0.8)
        self.play(FadeIn(num62), run_time=0.3)

        flash(eq62, PURPLE_C)

        self.wait(0.8)

        # ============================================================
        # STEP 7 — TAKE THE GRADIENT
        # ============================================================
        clear_all(step6, eq62, num62)

        step7 = label(
            "Now solve the optimization problem",
            y=2.65,
        )

        self.play(FadeIn(step7), run_time=0.4)

        gradient = MathTex(
            r"\nabla_{c}"
            r"\left("
            r"-2x^{T}Dc+c^{T}c"
            r"\right)"
            r"=0",
            color=BLACK_C,
            font_size=40,
        )
        gradient.move_to(UP * 1.15)

        num63 = eq_number("2.63", gradient)

        write(gradient, 0.8)
        self.play(FadeIn(num63), run_time=0.3)

        flash(gradient, ORANGE_C)

        eq64 = MathTex(
            r"-2D^{T}x+2c=0",
            color=BLACK_C,
            font_size=42,
        )
        eq64.move_to(DOWN * 0.15)

        num64 = eq_number("2.64", eq64)

        self.play(
            TransformFromCopy(gradient, eq64),
            FadeIn(num64),
            run_time=0.75,
        )

        flash(eq64, BLUE_C)

        eq65 = MathTex(
            r"c=D^{T}x",
            color=GREEN_C,
            font_size=46,
        )
        eq65.move_to(DOWN * 1.45)

        num65 = eq_number("2.65", eq65)

        self.play(
            TransformFromCopy(eq64, eq65),
            FadeIn(num65),
            run_time=0.75,
        )

        flash(eq65, GREEN_C)

        self.wait(1)

        # ============================================================
        # STEP 8 — ENCODER
        # ============================================================
        clear_all(
            step7,
            gradient,
            num63,
            eq64,
            num64,
            eq65,
            num65,
        )

        step8 = label(
            "The optimal encoder is just a matrix-vector product",
            y=2.65,
        )

        self.play(FadeIn(step8), run_time=0.4)

        encoder_title = Text(
            "ENCODE",
            font="Arial",
            font_size=22,
            weight=BOLD,
            color=BLUE_C,
        )
        encoder_title.move_to(UP * 1.45)

        self.play(FadeIn(encoder_title), run_time=0.35)

        eq66 = MathTex(
            r"f(x)=D^{T}x",
            color=BLUE_C,
            font_size=48,
        )
        eq66.move_to(UP * 0.45)

        num66 = eq_number("2.66", eq66)

        write(eq66, 0.7)
        self.play(FadeIn(num66), run_time=0.3)

        flash(eq66, BLUE_C)

        # Visual matrix-vector flow
        D_small = Matrix(
            [
                ["d_{11}", "d_{12}"],
                ["d_{21}", "d_{22}"],
                ["d_{31}", "d_{32}"],
            ],
            element_to_mobject_config={"color": GREEN_C},
            bracket_config={"color": GREEN_C},
        ).scale(0.52)

        x_small = Matrix(
            [["x_1"], ["x_2"], ["x_3"]],
            element_to_mobject_config={"color": BLACK_C},
            bracket_config={"color": BLACK_C},
        ).scale(0.52)

        c_small = Matrix(
            [["c_1"], ["c_2"]],
            element_to_mobject_config={"color": BLUE_C},
            bracket_config={"color": BLUE_C},
        ).scale(0.52)

        D_small.move_to(LEFT * 2.7 + DOWN * 1.45)
        x_small.move_to(LEFT * 0.8 + DOWN * 1.45)
        c_small.move_to(RIGHT * 2.55 + DOWN * 1.45)

        arrow_a = Arrow(
            D_small.get_right(),
            x_small.get_left(),
            buff=0.18,
            color=BLACK_C,
            stroke_width=2.2,
        )

        arrow_b = Arrow(
            x_small.get_right(),
            c_small.get_left(),
            buff=0.18,
            color=BLUE_C,
            stroke_width=2.2,
        )

        self.play(
            FadeIn(D_small),
            FadeIn(x_small),
            run_time=0.45,
        )

        flash(D_small, GREEN_C)

        self.play(
            GrowArrow(arrow_a),
            run_time=0.35,
        )

        self.play(
            GrowArrow(arrow_b),
            FadeIn(c_small),
            run_time=0.5,
        )

        flash(c_small, BLUE_C)

        self.wait(0.8)

        # ============================================================
        # STEP 9 — RECONSTRUCTION
        # ============================================================
        clear_all(
            step8,
            encoder_title,
            eq66,
            num66,
            D_small,
            x_small,
            c_small,
            arrow_a,
            arrow_b,
        )

        step9 = label(
            "Reconstruct the original vector",
            y=2.65,
        )

        self.play(FadeIn(step9), run_time=0.4)

        reconstruction_title = Text(
            "RECONSTRUCT",
            font="Arial",
            font_size=22,
            weight=BOLD,
            color=PURPLE_C,
        )
        reconstruction_title.move_to(UP * 1.45)

        self.play(
            FadeIn(reconstruction_title),
            run_time=0.35,
        )

        eq67 = MathTex(
            r"r(x)"
            r"="
            r"g(f(x))"
            r"="
            r"DD^{T}x",
            color=PURPLE_C,
            font_size=46,
        )
        eq67.move_to(UP * 0.55)

        num67 = eq_number("2.67", eq67)

        write(eq67, 0.85)
        self.play(FadeIn(num67), run_time=0.3)

        flash(eq67, PURPLE_C)

        # Explicit reconstruction chain
        input_x = MathTex(
            r"x",
            color=BLACK_C,
            font_size=42,
        )
        input_x.move_to(LEFT * 3.5 + DOWN * 1.45)

        c_code = MathTex(
            r"D^{T}x",
            color=BLUE_C,
            font_size=38,
        )
        c_code.move_to(LEFT * 1.2 + DOWN * 1.45)

        output_x = MathTex(
            r"DD^{T}x",
            color=PURPLE_C,
            font_size=38,
        )
        output_x.move_to(RIGHT * 2.0 + DOWN * 1.45)

        a1 = Arrow(
            input_x.get_right(),
            c_code.get_left(),
            buff=0.25,
            color=BLUE_C,
            stroke_width=2.5,
        )

        a2 = Arrow(
            c_code.get_right(),
            output_x.get_left(),
            buff=0.25,
            color=PURPLE_C,
            stroke_width=2.5,
        )

        encode_tag = Text(
            "encode",
            font="Arial",
            font_size=17,
            color=BLUE_C,
        )
        encode_tag.next_to(a1, UP, buff=0.08)

        decode_tag = Text(
            "decode",
            font="Arial",
            font_size=17,
            color=PURPLE_C,
        )
        decode_tag.next_to(a2, UP, buff=0.08)

        self.play(
            FadeIn(input_x),
            run_time=0.35,
        )

        flash(input_x, BLACK_C)

        self.play(
            GrowArrow(a1),
            FadeIn(encode_tag),
            FadeIn(c_code),
            run_time=0.55,
        )

        flash(c_code, BLUE_C)

        self.play(
            GrowArrow(a2),
            FadeIn(decode_tag),
            FadeIn(output_x),
            run_time=0.55,
        )

        flash(output_x, PURPLE_C)

        # ============================================================
        # FINAL MESSAGE
        # ============================================================
        final_note = Text(
            "PCA = encode → compress → reconstruct",
            font="Arial",
            font_size=25,
            weight=BOLD,
            color=BLACK_C,
        )
        final_note.move_to(DOWN * 2.55)

        self.play(
            FadeIn(final_note, shift=UP * 0.10),
            run_time=0.55,
        )

        final_box = SurroundingRectangle(
            VGroup(eq67, input_x, c_code, output_x, final_note),
            color=BLACK_C,
            buff=0.28,
            stroke_width=1.4,
            corner_radius=0.12,
        )

        self.play(
            Create(final_box),
            run_time=0.55,
        )

        self.wait(2)


if __name__ == "__main__":
    Figure219().render()
