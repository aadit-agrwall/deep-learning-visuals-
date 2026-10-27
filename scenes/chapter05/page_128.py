from manim import *
import numpy as np, json as _json
from pathlib import Path
from PIL import Image
from common.chapter5_style import Chapter5Scene
from common.asmr_sync import ASMRSync

PAGE = "128"
PAGE_SRC = Path(f"assets/bookpage/page_{PAGE}.png")
BAND_DIR = Path(f"assets/bookpage/page_{PAGE}_bands")
CUE_FILE = f"/tmp/p{PAGE}_cues.json"
WHITE_BG = "#FFFFFF"; K = "#000000"; MIN_SECONDS = 62.0


class CueLogger:
    def __init__(self, scene, real):
        self._s, self._r, self.log = scene, real, []
    def cue(self, name, *a, **k):
        try: t = float(self._s.renderer.time)
        except Exception: t = float(self._s.time)
        self.log.append({"t": t, "name": name, "glyphs": k.get("glyphs", 0), "pan": k.get("pan", 0.0)})
        _json.dump(self.log, open(CUE_FILE, "w"))
        return self._r.cue(name, *a, **k)
    def __getattr__(self, n): return getattr(self._r, n)


class Collapse(Animation):
    def __init__(self, mobject, point, spin=0.0, reverse=False, **kwargs):
        self.point = np.array(point, dtype=float); self.spin = spin; self.reverse = reverse
        self.cur_s = 1.0; self.cur_a = 0.0
        super().__init__(mobject, **kwargs)
        if reverse: self._apply(1.0)
    def _apply(self, t):
        s = max(1 - 0.985 * t, 1e-3); a = self.spin * t
        self.mobject.scale(s / self.cur_s, about_point=self.point)
        self.mobject.rotate(a - self.cur_a, about_point=self.point)
        self.cur_s, self.cur_a = s, a
    def interpolate_mobject(self, alpha):
        t = self.rate_func(alpha); self._apply(1 - t if self.reverse else t)


class ZoomPulse(Animation):
    def __init__(self, mobject, point, s0, s1, **kwargs):
        self.point = np.array(point, dtype=float); self.s0, self.s1, self.cur = s0, s1, 1.0
        super().__init__(mobject, **kwargs)
    def interpolate_mobject(self, alpha):
        t = self.rate_func(alpha); s = max(self.s0 + (self.s1 - self.s0) * t, 1e-3)
        self.mobject.scale(s / self.cur, about_point=self.point); self.cur = s


def build_bands():
    if not PAGE_SRC.exists(): raise FileNotFoundError(f"Missing page image: {PAGE_SRC}")
    image = Image.open(PAGE_SRC).convert("RGB"); w, h = image.size
    image = image.crop((6, 6, w - 6, h - 6)); w, h = image.size
    arr = np.asarray(image)
    ink = (arr[:, 14:-14].min(axis=2) < 235).any(axis=1); ink[:3] = False; ink[-6:] = False
    BAND_DIR.mkdir(parents=True, exist_ok=True)
    for old in BAND_DIR.glob("band_*.png"): old.unlink()
    bands, y = [], 0
    while y < h:
        if not ink[y]: y += 1; continue
        s = y
        while y < h and ink[y]: y += 1
        top, bottom = max(0, s - 2), min(h, y + 2)
        p = BAND_DIR / f"band_{len(bands):03d}.png"
        image.crop((0, top, w, bottom)).save(p); bands.append((str(p), top, bottom))
    if not bands: raise ValueError("No text strips detected")
    return w, h, bands


def fit(mob, width):
    if mob.width > width: mob.scale_to_fit_width(width)
    return mob
def T(text, size=30, bold=False):
    return Tex((r"\textbf{" + text + "}") if bold else text, color=K, font_size=size)
def Mx(*parts, size=40):
    return MathTex(*parts, color=K, font_size=size)


class Page_128(Chapter5Scene):
    PAGE_NO = "128"

    def make_page(self, width, height, bands):
        aspect = width / height
        ph = min(config.frame_height - 1.3, (config.frame_width - 0.4) / aspect); pw = ph * aspect
        sc = pw / width; c = np.array([0.0, 0.1, 0.0])
        paper = Rectangle(width=pw, height=ph, stroke_width=0, fill_color=WHITE_BG, fill_opacity=1).move_to(c)
        paper.set_z_index(0); top = c[1] + ph / 2; strips = []
        for path, t, b in bands:
            s = ImageMobject(path); s.scale_to_fit_width(pw)
            s.move_to([c[0], top - ((t + b) / 2) * sc, 0]); s.set_z_index(1); strips.append(s)
        return paper, strips

    def page_motion(self, paper, strips, point, reverse=False, run=2.0):
        pt = np.array(point, dtype=float)
        order = sorted(strips, key=lambda s: np.linalg.norm(s.get_center() - pt), reverse=not reverse)
        anims = [Collapse(s, pt, PI * 0.5, reverse=reverse, rate_func=smooth, remover=not reverse, run_time=run) for s in order]
        return AnimationGroup(LaggedStart(*anims, lag_ratio=0.03),
                              Collapse(paper, pt, PI * 0.5, reverse=reverse, rate_func=smooth, remover=not reverse, run_time=run * 1.6))

    def next_scene(self, audio, items):
        with audio.cue("wipe"):
            self.play(*[FadeOut(i) for i in items if i is not None], run_time=0.7)
        self.wait(0.2)

    def heading_in(self, audio, text):
        h = T(text, 40, True); fit(h, 7.6); h.to_edge(UP, buff=0.5)
        with audio.cue("type", glyphs=len(text)): self.play(Write(h), run_time=1.2)
        u = Line(h.get_left(), h.get_right(), color=K, stroke_width=4).next_to(h, DOWN, buff=0.12)
        with audio.cue("draw"): self.play(Create(u), run_time=0.5)
        return [h, u]

    def note_in(self, audio, text, y, size=30):
        n = T(text, size); fit(n, 7.4); n.move_to([0, y, 0])
        with audio.cue("type", glyphs=len(text)): self.play(Write(n), run_time=1.3)
        return n

    def card(self, text, y, size=28, h=1.0):
        r = RoundedRectangle(width=7.0, height=h, corner_radius=0.2, stroke_color=K,
                             stroke_width=3, fill_opacity=0).move_to([0, y, 0])
        t = Tex(text, color=K, font_size=size); fit(t, 6.5); t.move_to(r)
        return r, t

    # ---------------------------------------------------------
    # A - Figure 5.6
    # ---------------------------------------------------------
    def scene_a(self, audio):
        items = self.heading_in(audio, "Figure 5.6: Capacity and Error")

        # legend
        def legend(x, kind, label):
            a, b = [x, 2.0, 0], [x + 0.6, 2.0, 0]
            if kind == "dot": ln = DashedLine(a, b, color=K, stroke_width=5, dash_length=0.06, dashed_ratio=0.5)
            elif kind == "dash": ln = DashedLine(a, b, color=K, stroke_width=5, dash_length=0.18, dashed_ratio=0.65)
            else: ln = Line(a, b, color=K, stroke_width=8)
            tx = T(label, 24).next_to(ln, RIGHT, buff=0.12)
            return VGroup(ln, tx)
        lg = [legend(-3.6, "dot", "Bias"), legend(-1.9, "dash", "Variance"),
              legend(0.1, "solid", "Generalization error")]
        with audio.cue("grow"):
            self.play(LaggedStart(*[FadeIn(g) for g in lg], lag_ratio=0.25), run_time=1.2)
        items += lg

        ax = Axes(x_range=[0, 1, 1], y_range=[0, 1.1, 1], x_length=6.0, y_length=3.0, tips=False,
                  axis_config={"color": K, "stroke_width": 3, "include_ticks": False}).move_to([0, -0.2, 0])
        bias = DashedVMobject(ax.plot(lambda x: (1 - x) ** 2, x_range=[0, 1], color=K, stroke_width=5),
                              num_dashes=48, dashed_ratio=0.3)
        var = DashedVMobject(ax.plot(lambda x: x ** 2, x_range=[0, 1], color=K, stroke_width=5),
                             num_dashes=18, dashed_ratio=0.65)
        gen_f = lambda x: (1 - x) ** 2 + x ** 2
        gen = ax.plot(gen_f, x_range=[0, 1], color=K, stroke_width=8)

        uz = T("Underfitting zone", 24).move_to(ax.c2p(0.26, 1.04))
        oz = T("Overfitting zone", 24).move_to(ax.c2p(0.76, 1.04))
        cap = T(r"Capacity $\rightarrow$", 24).next_to(ax.c2p(0.93, 0), DOWN, buff=0.15)

        with audio.cue("draw"):
            self.play(Create(ax), FadeIn(cap), run_time=1.0)
        with audio.cue("slide", pan=-0.4):
            self.play(Create(bias), run_time=1.4)
        with audio.cue("slide", pan=0.4):
            self.play(Create(var), run_time=1.4)
        with audio.cue("slide", profile="transfer"):
            self.play(Create(gen), run_time=1.6)

        best = ax.c2p(0.5, gen_f(0.5))
        vline = DashedLine(ax.c2p(0.5, 0), ax.c2p(0.5, 1.1), color=K, stroke_width=3)
        opt = T("Optimal capacity", 24).next_to(ax.c2p(0.5, 0), DOWN, buff=0.15)
        dot = Dot(best, radius=0.11, color=K).set_z_index(5)
        with audio.cue("grow"):
            self.play(Create(vline), FadeIn(uz), FadeIn(oz), FadeIn(opt), GrowFromCenter(dot), run_time=1.0)
        self.play(Flash(best, color=K, flash_radius=0.6, line_length=0.25, run_time=0.7))

        n = self.note_in(audio, "Bias falls, variance rises: a U-shaped error curve.", -3.0, 28)
        self.wait(1.6)
        return items + [ax, bias, var, gen, uz, oz, cap, vline, opt, dot, n]

    # ---------------------------------------------------------
    # B - capacity, MSE, bias, variance
    # ---------------------------------------------------------
    def scene_b(self, audio):
        items = self.heading_in(audio, "Capacity and Generalization Error")
        n1 = self.note_in(audio, "Generalization error is measured by the MSE", 1.9, 30)
        eq = Mx(r"\mathrm{MSE}", "=", r"\mathrm{Bias}^2+\mathrm{Var}", size=44)
        fit(eq, 6.5); eq.move_to([0, 0.9, 0])
        with audio.cue("draw"): self.play(Write(eq), run_time=1.4)
        box = SurroundingRectangle(eq, color=K, buff=0.2, stroke_width=4)
        with audio.cue("grow"): self.play(Create(box), run_time=0.6)
        items += [n1, eq, box]

        def pill(text, pos):
            r = RoundedRectangle(width=2.7, height=0.9, corner_radius=0.2, stroke_color=K,
                                 stroke_width=3, fill_opacity=0).move_to(pos)
            t = T(text, 30).move_to(r)
            return VGroup(r, t)
        cap = pill(r"Capacity $\uparrow$", [-2.4, -0.9, 0])
        var = pill(r"Variance $\uparrow$", [2.3, -0.2, 0])
        bia = pill(r"Bias $\downarrow$", [2.3, -1.6, 0])
        with audio.cue("grow", pan=-0.3): self.play(GrowFromCenter(cap), run_time=0.7)
        a1 = Arrow(cap.get_right(), var.get_left(), color=K, buff=0.1, stroke_width=4)
        with audio.cue("slide", pan=0.3): self.play(GrowArrow(a1), GrowFromCenter(var), run_time=0.9)
        a2 = Arrow(cap.get_right(), bia.get_left(), color=K, buff=0.1, stroke_width=4)
        with audio.cue("slide", pan=0.3): self.play(GrowArrow(a2), GrowFromCenter(bia), run_time=0.9)
        items += [cap, var, bia, a1, a2]

        n2 = self.note_in(audio, "This gives the U-shaped curve of error versus capacity.", -2.9, 28)
        items.append(n2)
        self.wait(1.6)
        return items

    # ---------------------------------------------------------
    # C - consistency: more data
    # ---------------------------------------------------------
    def scene_c(self, audio):
        items = self.heading_in(audio, "5.4.5 Consistency")
        n1 = self.note_in(audio, "How does an estimator behave as the data grows?", 1.95, 28)
        items.append(n1)

        ax = Axes(x_range=[0, 60, 10], y_range=[0, 1, 0.5], x_length=5.4, y_length=2.4, tips=False,
                  axis_config={"color": K, "stroke_width": 3, "include_ticks": False}).move_to([0, -0.4, 0])
        up = ax.plot(lambda x: min(0.97, 0.6 + 0.9 / np.sqrt(x)), x_range=[1, 60], color=K, stroke_width=3)
        lo = ax.plot(lambda x: max(0.03, 0.6 - 0.9 / np.sqrt(x)), x_range=[1, 60], color=K, stroke_width=3)
        truth = DashedLine(ax.c2p(0, 0.6), ax.c2p(60, 0.6), color=K, stroke_width=4)
        tl = Mx(r"\theta", size=38).next_to(ax.c2p(60, 0.6), RIGHT, buff=0.12)
        xl = Mx("m", size=34).next_to(ax, DOWN, buff=0.2)
        yl = Mx(r"\hat\theta_m", size=32).next_to(ax.c2p(0, 1), LEFT, buff=0.1)
        with audio.cue("draw"): self.play(Create(ax), Write(xl), Write(yl), run_time=1.0)
        with audio.cue("slide", profile="transfer"): self.play(Create(truth), Write(tl), run_time=1.0)
        with audio.cue("slide", pan=-0.3): self.play(Create(up), Create(lo), run_time=1.3)

        rng = np.random.default_rng(128)
        dots = VGroup()
        for m in range(1, 61):
            est = float(np.clip(0.6 + rng.normal(0, 0.45 / np.sqrt(m)), 0.04, 0.97))
            dots.add(Dot(ax.c2p(m, est), radius=0.05, color=K))
        with audio.cue("grow"):
            self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.03), run_time=2.6)
        n2 = self.note_in(audio, r"As $m$ grows, $\hat\theta_m$ converges to the true value $\theta$.", -2.9, 28)
        self.wait(1.5)
        return items + [ax, up, lo, truth, tl, xl, yl, dots, n2]

    # ---------------------------------------------------------
    # D - equation 5.55
    # ---------------------------------------------------------
    def scene_d(self, audio):
        items = self.heading_in(audio, "Convergence in Probability")
        eq = Mx(r"\mathrm{plim}_{m\to\infty}\hat\theta_m", "=", r"\theta", size=44)
        fit(eq, 5.2); eq.move_to([-0.4, 1.95, 0])
        num = T("(5.55)", 28).move_to([3.1, 1.95, 0])
        with audio.cue("draw"): self.play(Write(eq), run_time=1.4)
        self.play(FadeIn(num), run_time=0.25)
        items += [eq, num]

        pr = Mx(r"P\left(|\hat\theta_m-\theta|>\epsilon\right)", r"\to 0", r"\text{ as } m\to\infty", size=34)
        fit(pr, 7.2); pr.move_to([0, 1.05, 0])
        with audio.cue("draw"): self.play(Write(pr), run_time=1.4)
        items.append(pr)
        t1 = self.note_in(audio, r"plim: convergence in probability, for any $\epsilon>0$", 0.3, 26)
        items.append(t1)

        ax = Axes(x_range=[-3, 3, 1], y_range=[0, 1.7, 1], x_length=5.6, y_length=1.7, tips=False,
                  axis_config={"color": K, "stroke_width": 3, "include_ticks": False}).move_to([0, -1.75, 0])
        g = lambda s: (lambda x: np.exp(-x ** 2 / (2 * s * s)) / (s * np.sqrt(2 * np.pi)))
        c1 = ax.plot(g(1.0), x_range=[-3, 3], color=K, stroke_width=6)
        c2 = ax.plot(g(0.5), x_range=[-3, 3], color=K, stroke_width=6)
        c3 = ax.plot(g(0.3), x_range=[-3, 3], color=K, stroke_width=6)
        e1 = DashedLine(ax.c2p(-1, 0), ax.c2p(-1, 1.7), color=K, stroke_width=3)
        e2 = DashedLine(ax.c2p(1, 0), ax.c2p(1, 1.7), color=K, stroke_width=3)
        lt = Mx(r"\theta", size=32).next_to(ax.c2p(0, 0), DOWN, buff=0.15)
        le1 = Mx(r"\theta-\epsilon", size=28).next_to(ax.c2p(-1, 0), DOWN, buff=0.15)
        le2 = Mx(r"\theta+\epsilon", size=28).next_to(ax.c2p(1, 0), DOWN, buff=0.15)
        with audio.cue("draw"):
            self.play(Create(ax), Create(e1), Create(e2), Write(lt), Write(le1), Write(le2), run_time=1.2)
        with audio.cue("slide", pan=-0.3): self.play(Create(c1), run_time=1.0)
        with audio.cue("slide"): self.play(Transform(c1, c2), run_time=1.2)
        with audio.cue("slide", pan=0.3): self.play(Transform(c1, c3), run_time=1.2)
        self.wait(1.6)
        return items + [ax, c1, e1, e2, lt, le1, le2]

    # ---------------------------------------------------------
    # E - weak vs strong
    # ---------------------------------------------------------
    def scene_e(self, audio):
        items = self.heading_in(audio, "Weak and Strong Consistency")
        r1, t1 = self.card(r"\textbf{Weak consistency}: convergence in probability", 1.7)
        with audio.cue("grow", pan=-0.3): self.play(Create(r1), Write(t1), run_time=1.3)
        e1 = Mx(r"\hat\theta_m \xrightarrow{p} \theta", size=46).move_to([0, 0.5, 0])
        with audio.cue("draw"): self.play(Write(e1), run_time=1.2)
        r2, t2 = self.card(r"\textbf{Strong consistency}: almost sure convergence of $\hat\theta$ to $\theta$", -0.8)
        with audio.cue("grow", pan=0.3): self.play(Create(r2), Write(t2), run_time=1.5)
        e2 = Mx(r"\hat\theta_m \xrightarrow{\text{a.s.}} \theta", size=46).move_to([0, -2.0, 0])
        with audio.cue("draw"): self.play(Write(e2), run_time=1.2)
        box = SurroundingRectangle(e2, color=K, buff=0.18, stroke_width=4)
        with audio.cue("grow"): self.play(Create(box), run_time=0.6)
        n = self.note_in(audio, "Condition (5.55) is known as consistency.", -3.1, 28)
        self.wait(1.6)
        return items + [r1, t1, e1, r2, t2, e2, box, n]

    def construct(self):
        self.camera.background_color = WHITE_BG; config.background_color = WHITE_BG
        audio = CueLogger(self, ASMRSync(self, self.PAGE_NO))
        w, h, bands = build_bands()
        paper, strips = self.make_page(w, h, bands); pc = paper.get_center()
        with audio.cue("grow"): self.play(FadeIn(paper), *[FadeIn(s) for s in strips], run_time=0.6)
        self.wait(3.4)
        with audio.cue("zoom"): self.play(self.page_motion(paper, strips, pc, reverse=False))
        dot = Dot(pc, radius=0.07, color=K)
        with audio.cue("grow"): self.play(GrowFromCenter(dot), run_time=0.3)
        with audio.cue("zoom"):
            self.play(Flash(pc, color=K, flash_radius=0.8, line_length=0.3, run_time=0.7), FadeOut(dot, scale=4), run_time=0.7)
        for scene in (self.scene_a, self.scene_b, self.scene_c, self.scene_d, self.scene_e):
            self.next_scene(audio, scene(audio))
        paper2, strips2 = self.make_page(w, h, bands); pc2 = paper2.get_center()
        self.add(paper2, *strips2)
        with audio.cue("zoom"): self.play(self.page_motion(paper2, strips2, pc2, reverse=True))
        self.wait(0.8); allm = [paper2, *strips2]
        with audio.cue("zoom"):
            self.play(*[ZoomPulse(m, pc2, 1.0, 1.04, run_time=1.2, rate_func=smooth) for m in allm])
            self.play(*[ZoomPulse(m, pc2, 1.0, 1 / 1.04, run_time=1.2, rate_func=smooth) for m in allm])
        self.wait(1.5)
        try: now = self.renderer.time
        except Exception: now = self.time
        if now < MIN_SECONDS: self.wait(MIN_SECONDS - now + 0.2)
        audio.finish()


if __name__ == "__main__":
    Page_128().render()
