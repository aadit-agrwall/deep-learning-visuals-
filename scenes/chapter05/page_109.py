from manim import *

from common import palette as pal
from common.chapter5_style import Chapter5Scene


class Page_109(Chapter5Scene):
    PAGE_NO = "109"
    RNG_SEED = 1090

    # ---- layout helpers (page-local, distinct from inherited ones) ----
    def _fit(self, group):
        """Scale a whole scene group to fit a safe box inside the frame
        (width AND height), then center it slightly above the footer."""
        max_w = config.frame_width * 0.82
        max_h = config.frame_height * 0.74
        if group.width > max_w:
            group.scale_to_fit_width(max_w)
        if group.height > max_h:
            group.scale_to_fit_height(max_h)
        group.move_to([0, config.frame_height * 0.03, 0])
        return group

    def _bars(self, train_h, test_h):
        train = Rectangle(width=1.3, height=train_h, color=pal.INPUT,
                          fill_color=pal.INPUT, fill_opacity=0.55)
        test = Rectangle(width=1.3, height=test_h, color=pal.OUTPUT,
                         fill_color=pal.OUTPUT, fill_opacity=0.55)
        VGroup(train, test).arrange(RIGHT, buff=2.4, aligned_edge=DOWN)
        return train, test

    def _dataset_box(self, color, label):
        box = RoundedRectangle(corner_radius=0.15, width=2.8, height=1.6, color=color)
        dots = VGroup(*[Dot(radius=0.06, color=color) for _ in range(12)])
        dots.arrange_in_grid(rows=3, cols=4, buff=0.3).move_to(box)
        lbl = self.txt(label, color=color).next_to(box, DOWN, buff=0.2)
        return VGroup(box, dots, lbl)

    def construct(self):
        self.init_page()

        # ---------- Scene 1: the question ----------
        s1_title = self.txt("Test error is what\nwe actually care about", color=pal.TEXT)
        s1_form = self.formula(
            r"\frac{1}{m^{(\mathrm{test})}}\left\|\boldsymbol{X}^{(\mathrm{test})}"
            r"\boldsymbol{w}-\boldsymbol{y}^{(\mathrm{test})}\right\|_2^2",
            color=pal.FORMULA,
        )
        s1_q = self.txt("But we only get to see\nthe training set.", color=pal.ERROR)
        s1 = VGroup(s1_title, s1_form, s1_q).arrange(DOWN, buff=0.7)
        self._fit(s1)

        self.type_in(s1_title)
        self.play(Write(s1_form))
        self.wait(0.5)
        self.type_in(s1_q)
        self.wait(1.0)
        self.dust_wipe([s1_title, s1_form, s1_q])

        # ---------- Scene 2: data-generating process + i.i.d. ----------
        s2_title = self.txt("Statistical learning theory", color=pal.TEXT)
        blob = Ellipse(width=3.4, height=1.5, color=pal.DISTRIBUTION,
                       fill_color=pal.DISTRIBUTION, fill_opacity=0.35)
        blob_lbl = self.formula(r"p_{\mathrm{data}}", color=pal.DISTRIBUTION)
        blob_lbl.move_to(blob)
        blob_grp = VGroup(blob, blob_lbl)

        train_box = self._dataset_box(pal.INPUT, "train")
        test_box = self._dataset_box(pal.OUTPUT, "test")
        boxes = VGroup(train_box, test_box).arrange(RIGHT, buff=1.2)

        iid_ind = self.txt("independent examples", color=pal.INPUT)
        iid_id = self.txt("identically distributed sets", color=pal.OUTPUT)
        iid = VGroup(iid_ind, iid_id).arrange(DOWN, buff=0.3)

        stack = VGroup(s2_title, blob_grp, boxes, iid).arrange(DOWN, buff=0.9)
        a1 = Arrow(blob.get_bottom(), train_box[0].get_top(), buff=0.1, color=pal.DISTRIBUTION)
        a2 = Arrow(blob.get_bottom(), test_box[0].get_top(), buff=0.1, color=pal.DISTRIBUTION)
        s2 = VGroup(stack, a1, a2)
        self._fit(s2)

        self.type_in(s2_title)
        self.play(FadeIn(blob), Write(blob_lbl))
        self.play(GrowArrow(a1), GrowArrow(a2))
        self.play(FadeIn(train_box), FadeIn(test_box))
        self.type_in(iid_ind)
        self.type_in(iid_id)
        self.wait(1.0)
        self.dust_wipe([s2_title, blob_grp, a1, a2, boxes, iid_ind, iid_id])

        # ---------- Scene 3: fixed w -> equal expectations ----------
        s3_title = self.txt("Fix w first,\nthen sample both sets", color=pal.TEXT)
        tr, te = self._bars(2.2, 2.2)
        bars = VGroup(tr, te)
        eq = self.formula(r"=", color=pal.FORMULA).move_to(bars)
        tr_lbl = self.txt("train error", color=pal.INPUT).next_to(tr, DOWN, buff=0.25)
        te_lbl = self.txt("test error", color=pal.OUTPUT).next_to(te, DOWN, buff=0.25)
        s3_note = self.txt("Same sampling process.\nOnly the name differs.", color=pal.TEXT)
        chart3 = VGroup(bars, eq, tr_lbl, te_lbl)
        s3 = VGroup(s3_title, chart3, s3_note).arrange(DOWN, buff=0.7)
        self._fit(s3)

        self.type_in(s3_title)
        self.play(GrowFromEdge(tr, DOWN), GrowFromEdge(te, DOWN))
        self.play(Write(eq), FadeIn(tr_lbl), FadeIn(te_lbl))
        self.type_in(s3_note)
        self.wait(1.0)
        self.dust_wipe([s3_title, tr, te, eq, tr_lbl, te_lbl, s3_note])

        # ---------- Scene 4: in practice, w is chosen on train ----------
        s4_title = self.txt("In practice:\ntrain, choose w, then test", color=pal.TEXT)
        tr2, te2 = self._bars(1.2, 2.4)
        tr2_lbl = self.txt("train error", color=pal.INPUT).next_to(tr2, DOWN, buff=0.25)
        te2_lbl = self.txt("test error", color=pal.OUTPUT).next_to(te2, DOWN, buff=0.25)
        gap_x = (tr2.get_right()[0] + te2.get_left()[0]) / 2
        y_lo, y_hi = tr2.get_top()[1], te2.get_top()[1]
        gap_ref = DashedLine(tr2.get_top(), [te2.get_left()[0], y_lo, 0], color=pal.ERROR)
        gap_arrow = DoubleArrow([gap_x, y_lo, 0], [gap_x, y_hi, 0], buff=0, color=pal.ERROR,
                                tip_length=0.18)
        gap_lbl = self.txt("gap", color=pal.ERROR).next_to(gap_arrow, LEFT, buff=0.15)
        chart4 = VGroup(tr2, te2, tr2_lbl, te2_lbl, gap_ref, gap_arrow, gap_lbl)
        ineq = self.formula(r"E[\text{test}] \geq E[\text{train}]", color=pal.FORMULA)
        s4 = VGroup(s4_title, chart4, ineq).arrange(DOWN, buff=0.7)
        self._fit(s4)

        self.type_in(s4_title)
        self.play(GrowFromEdge(tr2, DOWN), GrowFromEdge(te2, DOWN))
        self.play(FadeIn(tr2_lbl), FadeIn(te2_lbl))
        self.play(Create(gap_ref), GrowFromCenter(gap_arrow), FadeIn(gap_lbl))
        self.play(Write(ineq))
        self.wait(1.0)
        self.dust_wipe([s4_title, tr2, te2, tr2_lbl, te2_lbl, gap_ref, gap_arrow, gap_lbl, ineq])

        # ---------- Scene 5: two factors, two challenges ----------
        s5_title = self.txt("Two factors decide\nperformance", color=pal.TEXT)

        def card(num, goal, challenge, color):
            g = self.txt(f"{num}. {goal}", color=pal.TEXT)
            c = self.txt(challenge, color=color)
            inner = VGroup(g, c).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
            box = RoundedRectangle(corner_radius=0.2, width=inner.width + 0.8,
                                   height=inner.height + 0.6, color=color)
            inner.move_to(box)
            return VGroup(box, inner)

        c1 = card(1, "Make the training error small", "fails: underfitting", pal.ERROR)
        c2 = card(2, "Make the train/test gap small", "fails: overfitting", pal.DISTRIBUTION)
        cards = VGroup(c1, c2).arrange(DOWN, buff=0.5)
        s5 = VGroup(s5_title, cards).arrange(DOWN, buff=0.8)
        self._fit(s5)

        self.type_in(s5_title)
        self.play(FadeIn(c1, shift=RIGHT * 0.3))
        self.play(FadeIn(c2, shift=RIGHT * 0.3))
        self.wait(1.2)
        self.dust_wipe([s5_title, c1, c2])

        # ---------- Scene 6: takeaway ----------
        take = self.txt("Small training error.\nSmall gap.", color=pal.OUTPUT)
        underline = Line(take.get_corner(DL) + DOWN * 0.2,
                         take.get_corner(DR) + DOWN * 0.2, color=pal.OUTPUT)
        s6 = VGroup(take, underline)
        self._fit(s6)

        self.type_in(take)
        self.play(Create(underline))
        self.zoom_pulse(s6)
        self.wait(1.0)