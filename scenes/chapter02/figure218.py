from manim import *
import numpy as np


class Figure218(Scene):
    def construct(self):

        # ============================================================
        # STYLE
        # ============================================================
        self.camera.background_color = WHITE

        BLACK_C = "#111111"
        GREY_C = "#D9D9D9"
        BLUE_C = "#2563EB"
        GREEN_C = "#16A34A"
        RED_C = "#DC2626"
        ORANGE_C = "#EA580C"
        PURPLE_C = "#7C3AED"

        # ============================================================
        # HELPERS
        # ============================================================
        def title(text):
            t = Text(
                text,
                font="Arial",
                font_size=30,
                weight=BOLD,
                color=BLACK_C,
            )
            t.to_edge(UP, buff=0.28)
            return t

        def subtitle(text, y=2.65, size=20):
            t = Text(
                text,
                font="Arial",
                font_size=size,
                color=BLACK_C,
            )
            t.move_to([0, y, 0])
            return t

        def flash(obj, color=BLUE_C):
            self.play(
                Circumscribe(
                    obj,
                    color=color,
                    fade_out=True,
                    buff=0.10,
                    stroke_width=4,
                ),
                run_time=0.55,
            )

        def clear(*objs):
            existing = [o for o in objs if o is not None]
            if existing:
                self.play(
                    *[FadeOut(o) for o in existing],
                    run_time=0.55,
                )

        def section_label(text, y):
            t = Text(
                text,
                font="Arial",
                font_size=21,
                weight=BOLD,
                color=BLACK_C,
            )
            t.move_to([0, y, 0])
            return t

        # ============================================================
        # SUBTLE GRID
        # ============================================================
        grid = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-4, 4, 1],
            background_line_style={
                "stroke_color": GREY_C,
                "stroke_width": 1,
                "stroke_opacity": 0.18,
            },
            axis_config={
                "stroke_opacity": 0,
            },
        )

        self.add(grid)

        # ============================================================
        # TITLE
        # ============================================================
        heading = title("Principal Components Analysis")
        underline = Line(
            LEFT * 3.8,
            RIGHT * 3.8,
            color=BLACK_C,
            stroke_width=1.4,
        )
        underline.next_to(heading, DOWN, buff=0.13)

        self.play(
            FadeIn(heading, shift=DOWN * 0.12),
            Create(underline),
            run_time=0.8,
        )

        intro = subtitle(
            "Compress high-dimensional data while losing as little information as possible",
            y=2.55,
            size=19,
        )

        self.play(Write(intro), run_time=0.9)
        self.wait(0.7)

        # ============================================================
        # SCENE 1 — HIGH DIMENSION -> LOW DIMENSION
        # ============================================================
        section1 = section_label(
            "1. Encode data into a lower-dimensional representation",
            1.95,
        )

        self.play(FadeIn(section1), run_time=0.5)

        # Original high-dimensional vector
        x_vec = Matrix(
            [["x_1"], ["x_2"], ["x_3"], ["x_4"]],
            element_to_mobject_config={"color": BLACK_C},
            bracket_config={"color": BLACK_C},
        ).scale(0.70)

        x_label = MathTex(
            r"x\in\mathbb{R}^{n}",
            color=BLACK_C,
            font_size=31,
        )

        x_group = VGroup(x_label, x_vec).arrange(DOWN, buff=0.20)
        x_group.move_to(LEFT * 3.6 + DOWN * 0.10)

        # Code vector
        c_vec = Matrix(
            [["c_1"], ["c_2"]],
            element_to_mobject_config={"color": BLUE_C},
            bracket_config={"color": BLUE_C},
        ).scale(0.70)

        c_label = MathTex(
            r"c\in\mathbb{R}^{l}",
            color=BLUE_C,
            font_size=31,
        )

        c_group = VGroup(c_label, c_vec).arrange(DOWN, buff=0.20)
        c_group.move_to(RIGHT * 3.6 + DOWN * 0.10)

        encoder = RoundedRectangle(
            width=2.15,
            height=1.10,
            corner_radius=0.14,
            stroke_color=BLACK_C,
            stroke_width=2,
            fill_color=WHITE,
            fill_opacity=1,
        )

        encoder_text = MathTex(
            r"f(x)=c",
            color=BLACK_C,
            font_size=32,
        )
        encoder_text.move_to(encoder)

        encoder_group = VGroup(encoder, encoder_text)
        encoder_group.move_to(DOWN * 0.05)

        arrow1 = Arrow(
            x_group.get_right(),
            encoder_group.get_left(),
            buff=0.22,
            color=BLACK_C,
            stroke_width=2.5,
            max_tip_length_to_length_ratio=0.12,
        )

        arrow2 = Arrow(
            encoder_group.get_right(),
            c_group.get_left(),
            buff=0.22,
            color=BLUE_C,
            stroke_width=2.5,
            max_tip_length_to_length_ratio=0.12,
        )

        self.play(
            FadeIn(x_group),
            run_time=0.6,
        )

        flash(x_vec, ORANGE_C)

        self.play(
            GrowArrow(arrow1),
            FadeIn(encoder_group),
            run_time=0.65,
        )

        flash(encoder_text, BLUE_C)

        # Explicit movement: copies of x entries flow into encoder
        x_entries = x_vec.get_entries()

        moving_entries = VGroup(
            *[entry.copy() for entry in x_entries]
        )

        self.add(moving_entries)

        self.play(
            *[
                entry.animate.move_to(encoder.get_center()).scale(0.45)
                for entry in moving_entries
            ],
            run_time=0.8,
        )

        self.play(FadeOut(moving_entries), run_time=0.25)

        self.play(
            GrowArrow(arrow2),
            FadeIn(c_group),
            run_time=0.65,
        )

        flash(c_vec, BLUE_C)

        dim_note = MathTex(
            r"l<n",
            color=RED_C,
            font_size=32,
        )
        dim_note.next_to(c_group, DOWN, buff=0.20)

        self.play(Write(dim_note), run_time=0.4)

        self.wait(1)

        # ============================================================
        # CLEAR BEFORE NEXT IDEA
        # ============================================================
        clear(
            section1,
            x_group,
            c_group,
            encoder_group,
            arrow1,
            arrow2,
            dim_note,
        )

        # ============================================================
        # SCENE 2 — DECODING g(c) = Dc
        # ============================================================
        section2 = section_label(
            "2. Decode the compressed representation",
            1.95,
        )

        self.play(FadeIn(section2), run_time=0.5)

        decode_formula = MathTex(
            r"g(c)=Dc",
            color=BLACK_C,
            font_size=42,
        )
        decode_formula.move_to(UP * 1.25)

        self.play(Write(decode_formula), run_time=0.65)

        flash(decode_formula, GREEN_C)

        # Separate objects with generous spacing
        D = Matrix(
            [
                ["d_{11}", "d_{12}"],
                ["d_{21}", "d_{22}"],
                ["d_{31}", "d_{32}"],
            ],
            element_to_mobject_config={"color": GREEN_C},
            bracket_config={"color": GREEN_C},
        ).scale(0.62)

        c = Matrix(
            [["c_1"], ["c_2"]],
            element_to_mobject_config={"color": BLUE_C},
            bracket_config={"color": BLUE_C},
        ).scale(0.62)

        reconstructed = Matrix(
            [
                [r"\hat{x}_1"],
                [r"\hat{x}_2"],
                [r"\hat{x}_3"],
            ],
            element_to_mobject_config={"color": PURPLE_C},
            bracket_config={"color": PURPLE_C},
        ).scale(0.62)

        D.move_to(LEFT * 3.1 + DOWN * 0.45)
        c.move_to(LEFT * 0.65 + DOWN * 0.45)
        reconstructed.move_to(RIGHT * 3.25 + DOWN * 0.45)

        equals = MathTex(
            "=",
            color=BLACK_C,
            font_size=38,
        )
        equals.move_to(RIGHT * 1.35 + DOWN * 0.45)

        D_label = MathTex(
            r"D\in\mathbb{R}^{n\times l}",
            color=GREEN_C,
            font_size=25,
        )
        D_label.next_to(D, DOWN, buff=0.20)

        c_label2 = MathTex(
            r"c\in\mathbb{R}^{l}",
            color=BLUE_C,
            font_size=25,
        )
        c_label2.next_to(c, DOWN, buff=0.20)

        xhat_label = MathTex(
            r"g(c)\approx x",
            color=PURPLE_C,
            font_size=27,
        )
        xhat_label.next_to(reconstructed, DOWN, buff=0.20)

        self.play(
            FadeIn(D),
            FadeIn(D_label),
            run_time=0.55,
        )

        flash(D, GREEN_C)

        self.play(
            FadeIn(c),
            FadeIn(c_label2),
            run_time=0.5,
        )

        flash(c, BLUE_C)

        # Matrix-vector multiplication visual transition
        D_entries = D.get_entries()
        c_entries = c.get_entries()
        out_entries = reconstructed.get_entries()

        # Row 1
        self.play(
            Indicate(D_entries[0], color=GREEN_C, scale_factor=1.15),
            Indicate(D_entries[1], color=GREEN_C, scale_factor=1.15),
            Indicate(c_entries[0], color=BLUE_C, scale_factor=1.15),
            Indicate(c_entries[1], color=BLUE_C, scale_factor=1.15),
            run_time=0.55,
        )

        self.play(
            FadeIn(equals),
            FadeIn(out_entries[0]),
            run_time=0.45,
        )

        # Row 2
        self.play(
            Indicate(D_entries[2], color=GREEN_C, scale_factor=1.15),
            Indicate(D_entries[3], color=GREEN_C, scale_factor=1.15),
            Indicate(c_entries[0], color=BLUE_C, scale_factor=1.15),
            Indicate(c_entries[1], color=BLUE_C, scale_factor=1.15),
            run_time=0.55,
        )

        self.play(
            FadeIn(out_entries[1]),
            run_time=0.35,
        )

        # Row 3
        self.play(
            Indicate(D_entries[4], color=GREEN_C, scale_factor=1.15),
            Indicate(D_entries[5], color=GREEN_C, scale_factor=1.15),
            Indicate(c_entries[0], color=BLUE_C, scale_factor=1.15),
            Indicate(c_entries[1], color=BLUE_C, scale_factor=1.15),
            run_time=0.55,
        )

        self.play(
            FadeIn(out_entries[2]),
            run_time=0.35,
        )

        # Add brackets only after entries exist
        self.add(reconstructed.get_brackets())

        self.play(FadeIn(xhat_label), run_time=0.4)

        flash(reconstructed, PURPLE_C)

        self.wait(1)

        clear(
            section2,
            decode_formula,
            D,
            D_label,
            c,
            c_label2,
            reconstructed,
            equals,
            xhat_label,
        )

        # ============================================================
        # SCENE 3 — ORTHOGONAL COLUMNS OF D
        # ============================================================
        section3 = section_label(
            "3. PCA constrains the decoder directions",
            1.95,
        )

        self.play(FadeIn(section3), run_time=0.5)

        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=6.2,
            y_length=3.2,
            axis_config={
                "color": GREY_C,
                "stroke_width": 1.4,
                "include_tip": False,
            },
        )

        axes.move_to(DOWN * 0.25)

        self.play(Create(axes), run_time=0.6)

        origin = axes.c2p(0, 0)

        d1 = Arrow(
            origin,
            axes.c2p(2.0, 0),
            buff=0,
            color=BLUE_C,
            stroke_width=5,
        )

        d2 = Arrow(
            origin,
            axes.c2p(0, 1.45),
            buff=0,
            color=GREEN_C,
            stroke_width=5,
        )

        d1_label = MathTex(
            r"D_{:,1}",
            color=BLUE_C,
            font_size=29,
        )
        d1_label.next_to(d1.get_end(), DOWN, buff=0.12)

        d2_label = MathTex(
            r"D_{:,2}",
            color=GREEN_C,
            font_size=29,
        )
        d2_label.next_to(d2.get_end(), RIGHT, buff=0.12)

        self.play(GrowArrow(d1), FadeIn(d1_label), run_time=0.6)

        flash(d1, BLUE_C)

        self.play(GrowArrow(d2), FadeIn(d2_label), run_time=0.6)

        flash(d2, GREEN_C)

        angle = RightAngle(
            Line(origin, axes.c2p(1, 0)),
            Line(origin, axes.c2p(0, 1)),
            length=0.25,
            color=RED_C,
        )

        self.play(Create(angle), run_time=0.4)

        orthogonal = MathTex(
            r"D_{:,i}^{T}D_{:,j}=0"
            r"\quad (i\neq j)",
            color=BLACK_C,
            font_size=31,
        )

        orthogonal.move_to(DOWN * 2.35)

        self.play(Write(orthogonal), run_time=0.6)

        flash(orthogonal, RED_C)

        unit_norm = MathTex(
            r"\|D_{:,i}\|_2=1",
            color=BLACK_C,
            font_size=31,
        )

        unit_norm.next_to(orthogonal, RIGHT, buff=0.65)

        # Shift both so they stay centered with spacing
        pair = VGroup(orthogonal, unit_norm)
        pair.arrange(RIGHT, buff=0.65)
        pair.move_to(DOWN * 2.35)

        self.play(
            orthogonal.animate.move_to(pair[0]),
            Write(unit_norm),
            run_time=0.6,
        )

        flash(unit_norm, GREEN_C)

        self.wait(1)

        clear(
            section3,
            axes,
            d1,
            d2,
            d1_label,
            d2_label,
            angle,
            orthogonal,
            unit_norm,
        )

        # ============================================================
        # SCENE 4 — RECONSTRUCTION ERROR
        # ============================================================
        section4 = section_label(
            "4. Choose the code that minimizes reconstruction error",
            1.95,
        )

        self.play(FadeIn(section4), run_time=0.5)

        axes2 = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=6.4,
            y_length=3.3,
            axis_config={
                "color": GREY_C,
                "stroke_width": 1.3,
                "include_tip": False,
            },
        )

        axes2.move_to(DOWN * 0.15)

        self.play(Create(axes2), run_time=0.55)

        # Principal direction
        principal_line = Line(
            axes2.c2p(-2.5, -1.0),
            axes2.c2p(2.5, 1.0),
            color=BLUE_C,
            stroke_width=4,
        )

        self.play(Create(principal_line), run_time=0.6)

        # Original point x
        x_point = Dot(
            axes2.c2p(1.45, 1.35),
            radius=0.09,
            color=RED_C,
        )

        x_text = MathTex(
            "x",
            color=RED_C,
            font_size=30,
        )
        x_text.next_to(x_point, UP + RIGHT, buff=0.10)

        self.play(FadeIn(x_point), FadeIn(x_text), run_time=0.45)

        flash(x_point, RED_C)

        # Projection / reconstruction
        reconstruction_coords = np.array([1.72, 0.688])
        recon_point = Dot(
            axes2.c2p(
                reconstruction_coords[0],
                reconstruction_coords[1],
            ),
            radius=0.09,
            color=GREEN_C,
        )

        recon_text = MathTex(
            r"g(c)",
            color=GREEN_C,
            font_size=29,
        )
        recon_text.next_to(recon_point, DOWN + RIGHT, buff=0.10)

        error_line = DashedLine(
            x_point.get_center(),
            recon_point.get_center(),
            color=ORANGE_C,
            stroke_width=3,
        )

        self.play(
            Create(error_line),
            run_time=0.55,
        )

        self.play(
            FadeIn(recon_point),
            FadeIn(recon_text),
            run_time=0.45,
        )

        flash(error_line, ORANGE_C)

        error_label = MathTex(
            r"\|x-g(c)\|_2",
            color=ORANGE_C,
            font_size=29,
        )

        error_label.next_to(error_line, LEFT, buff=0.16)

        self.play(Write(error_label), run_time=0.45)

        self.wait(0.7)

        # ============================================================
        # EQUATION (2.54)
        # ============================================================
        clear(
            section4,
            axes2,
            principal_line,
            x_point,
            x_text,
            recon_point,
            recon_text,
            error_line,
            error_label,
        )

        eq_title = section_label(
            "Optimal code",
            1.80,
        )

        self.play(FadeIn(eq_title), run_time=0.4)

        eq1 = MathTex(
            r"c^*",
            r"=",
            r"\operatorname*{arg\,min}_{c}",
            r"\|x-g(c)\|_2",
            color=BLACK_C,
            font_size=43,
        )

        eq1.move_to(UP * 0.75)

        self.play(Write(eq1), run_time=0.9)

        flash(eq1[0], BLUE_C)
        flash(eq1[3], ORANGE_C)

        note1 = Text(
            "Find the code whose reconstruction is closest to x",
            font="Arial",
            font_size=20,
            color=BLACK_C,
        )

        note1.next_to(eq1, DOWN, buff=0.45)

        self.play(FadeIn(note1), run_time=0.5)

        self.wait(0.8)

        # ============================================================
        # L2 -> SQUARED L2 EXPLICIT TRANSITION
        # ============================================================
        squared_label = Text(
            "Same minimizer → square the norm",
            font="Arial",
            font_size=21,
            weight=BOLD,
            color=BLACK_C,
        )

        squared_label.move_to(DOWN * 0.65)

        self.play(FadeIn(squared_label), run_time=0.4)

        eq2 = MathTex(
            r"c^*",
            r"=",
            r"\operatorname*{arg\,min}_{c}",
            r"\|x-g(c)\|_2^2",
            color=BLACK_C,
            font_size=43,
        )

        eq2.move_to(DOWN * 1.55)

        # Flash the old norm first
        flash(eq1[3], ORANGE_C)

        # Then visibly transform it into squared norm
        self.play(
            TransformFromCopy(eq1[0], eq2[0]),
            TransformFromCopy(eq1[1], eq2[1]),
            TransformFromCopy(eq1[2], eq2[2]),
            TransformFromCopy(eq1[3], eq2[3]),
            run_time=0.85,
        )

        flash(eq2[3], GREEN_C)

        self.wait(0.8)

        # ============================================================
        # FINAL EXPANSION
        # ============================================================
        clear(
            eq_title,
            eq1,
            note1,
            squared_label,
        )

        # Move eq2 upward, giving final expression its own space
        self.play(
            eq2.animate.move_to(UP * 1.05),
            run_time=0.55,
        )

        expand_text = Text(
            "Expand the squared Euclidean norm",
            font="Arial",
            font_size=21,
            weight=BOLD,
            color=BLACK_C,
        )

        expand_text.move_to(UP * 2.0)

        self.play(FadeIn(expand_text), run_time=0.4)

        flash(eq2[3], BLUE_C)

        final_expr = MathTex(
            r"(x-g(c))^{T}(x-g(c))",
            color=BLACK_C,
            font_size=45,
        )

        final_expr.move_to(DOWN * 0.35)

        self.play(
            TransformFromCopy(eq2[3], final_expr),
            run_time=0.9,
        )

        flash(final_expr, PURPLE_C)

        final_note = Text(
            "PCA minimizes reconstruction error",
            font="Arial",
            font_size=24,
            weight=BOLD,
            color=BLACK_C,
        )

        final_note.move_to(DOWN * 1.45)

        self.play(
            FadeIn(final_note, shift=UP * 0.12),
            run_time=0.55,
        )

        final_box = SurroundingRectangle(
            VGroup(eq2, final_expr, final_note),
            color=BLACK_C,
            buff=0.28,
            stroke_width=1.5,
            corner_radius=0.12,
        )

        self.play(Create(final_box), run_time=0.55)

        self.wait(2)


if __name__ == "__main__":
    Figure218().render()
