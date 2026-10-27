from manim import *
import numpy as np, json as _json
from pathlib import Path
from PIL import Image
from common.chapter5_style import Chapter5Scene
from common.asmr_sync import ASMRSync

PAGE = "130"
PAGE_SRC = Path(f"assets/bookpage/page_{PAGE}.png")
BAND_DIR = Path(f"assets/bookpage/page_{PAGE}_bands")
CUE_FILE = f"/tmp/p{PAGE}_cues.json"
WHITE_BG = "#FFFFFF"; K = "#000000"; MIN_SECONDS = 62.0


class _Ctx:
    def __init__(self, owner, entry, ctx):
        self.o, self.e, self.c = owner, entry, ctx
    def __enter__(self):
        self.e["t"] = self.o.now(); self.o.flush()
        return self.c.__enter__()
    def __exit__(self, *exc):
        self.e["end"] = self.o.now(); self.o.flush()
        return self.c.__exit__(*exc)


class CueLogger:
    def __init__(self, scene, real):
        self._s, self._r, self.log = scene, real, []
    def now(self):
        try: return float(self._s.renderer.time)
        except Exception: return float(self._s.time)
    def flush(self):
        _json.dump(self.log, open(CUE_FILE, "w"))
    def cue(self, name, *a, **k):
        e = {"t": self.now(), "end": self.now(), "name": name,
             "glyphs": k.get("glyphs", 0), "pan": k.get("pan", 0.0)}
        self.log.append(e)
        return _Ctx(self, e, self._r.cue(name, *a, **k))
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


class Page_130(Chapter5Scene):
    PAGE_NO = "130"

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

    def card(self, text, y, size=26, h=0.9):
        r = RoundedRectangle(width=7.2, height=h, corner_radius=0.2, stroke_color=K,
                             stroke_width=3, fill_opacity=0).move_to([0, y, 0])
        t = Tex(text, color=K, font_size=size); fit(t, 6.8); t.move_to(r)
        return r, t

    # A - log turns product into sum (5.58)
    def scene_a(self, audio):
        items = self.heading_in(audio, "Log Turns Product into Sum")
        n0 = self.note_in(audio, "A product of probabilities underflows numerically.", 2.2, 26)
        l1 = Mx(r"\boldsymbol{\theta}_{\mathrm{ML}}=\underset{\boldsymbol{\theta}}{\arg\max}\prod_{i=1}^{m}p_{\mathrm{model}}(\boldsymbol{x}^{(i)};\boldsymbol{\theta})", size=36)
        fit(l1, 6.6); l1.move_to([0, 1.2, 0])
        with audio.cue("draw"): self.play(Write(l1), run_time=1.5)
        ar = Arrow([0, 0.55, 0], [0, -0.15, 0], color=K, buff=0, stroke_width=5)
        lg = T(r"take $\log$", 26).next_to(ar, RIGHT, buff=0.15)
        with audio.cue("slide"): self.play(GrowArrow(ar), FadeIn(lg), run_time=0.8)
        l2 = Mx(r"\boldsymbol{\theta}_{\mathrm{ML}}=\underset{\boldsymbol{\theta}}{\arg\max}\sum_{i=1}^{m}\log p_{\mathrm{model}}(\boldsymbol{x}^{(i)};\boldsymbol{\theta})", size=36)
        fit(l2, 5.9); l2.move_to([-0.35, -1.0, 0])
        n58 = T("(5.58)", 28).move_to([3.3, -1.0, 0])
        with audio.cue("draw"): self.play(Write(l2), run_time=1.6)
        self.play(FadeIn(n58), run_time=0.25)
        box = SurroundingRectangle(l2, color=K, buff=0.18, stroke_width=4)
        with audio.cue("grow"): self.play(Create(box), run_time=0.6)
        n1 = self.note_in(audio, r"The $\arg\max$ does not change, and a sum is convenient.", -2.4, 26)
        self.wait(1.5)
        return items + [n0, l1, ar, lg, l2, n58, box, n1]

    # B - empirical distribution (5.59)
    def scene_b(self, audio):
        items = self.heading_in(audio, "The Empirical Distribution")
        n0 = self.note_in(audio, r"The $\arg\max$ is unchanged when we rescale the cost.", 2.2, 26)
        l1 = Mx(r"\frac{1}{m}", r"\sum_{i=1}^{m}\log p_{\mathrm{model}}(\boldsymbol{x}^{(i)};\boldsymbol{\theta})", size=36)
        fit(l1, 5.6); l1.move_to([0, 1.3, 0])
        with audio.cue("draw"): self.play(Write(l1), run_time=1.4)
        box1 = SurroundingRectangle(l1[0], color=K, buff=0.1, stroke_width=4)
        with audio.cue("grow"): self.play(Create(box1), run_time=0.5)
        l2 = Mx(r"\boldsymbol{\theta}_{\mathrm{ML}}=\underset{\boldsymbol{\theta}}{\arg\max}\,\mathbb{E}_{\mathbf{x}\sim\hat p_{\mathrm{data}}}\log p_{\mathrm{model}}(\boldsymbol{x};\boldsymbol{\theta})", size=36)
        fit(l2, 5.9); l2.move_to([-0.35, 0.1, 0])
        n59 = T("(5.59)", 28).move_to([3.3, 0.1, 0])
        with audio.cue("draw"): self.play(Write(l2), run_time=1.6)
        self.play(FadeIn(n59), run_time=0.25)
        ax = Axes(x_range=[0, 10, 1], y_range=[0, 1, 1], x_length=5.6, y_length=1.2, tips=False,
                  axis_config={"color": K, "stroke_width": 3, "include_ticks": False}).move_to([0, -1.9, 0])
        xs = [1, 2, 2.6, 3.4, 4.2, 5, 5.6, 6.4, 7.2, 8.3]
        spikes = VGroup(*[Line(ax.c2p(x, 0), ax.c2p(x, 0.8), color=K, stroke_width=5) for x in xs])
        tops = VGroup(*[Dot(ax.c2p(x, 0.8), radius=0.07, color=K) for x in xs])
        lab = Mx(r"\hat p_{\mathrm{data}}", size=32).move_to(ax.c2p(9.3, 0.85))
        with audio.cue("draw"): self.play(Create(ax), Write(lab), run_time=0.9)
        with audio.cue("grow"):
            self.play(LaggedStart(*[GrowFromCenter(s) for s in spikes], lag_ratio=0.12),
                      FadeIn(tops), run_time=1.6)
        n1 = self.note_in(audio, "Expectation over the empirical distribution of the training data.", -3.1, 24)
        self.wait(1.4)
        return items + [n0, l1, box1, l2, n59, ax, spikes, tops, lab, n1]

    # C - KL divergence (5.60, 5.61)
    def scene_c(self, audio):
        items = self.heading_in(audio, "KL Divergence")
        n0 = self.note_in(audio, "Minimize the dissimilarity between the two distributions.", 2.25, 26)
        a = Mx(r"D_{\mathrm{KL}}\left(\hat p_{\mathrm{data}}\,\|\,p_{\mathrm{model}}\right)", size=40)
        fit(a, 5.4); a.move_to([-0.8, 1.45, 0])
        with audio.cue("draw"): self.play(Write(a), run_time=1.3)
        b = Mx(r"=\mathbb{E}_{\mathbf{x}\sim\hat p_{\mathrm{data}}}\bigl[", r"\log\hat p_{\mathrm{data}}(\boldsymbol{x})", r"-\log p_{\mathrm{model}}(\boldsymbol{x})\bigr]", size=36)
        fit(b, 5.9); b.move_to([-0.35, 0.5, 0])
        n60 = T("(5.60)", 28).move_to([3.3, 0.5, 0])
        with audio.cue("draw"): self.play(Write(b), run_time=1.7)
        self.play(FadeIn(n60), run_time=0.25)
        box = SurroundingRectangle(b[1], color=K, buff=0.1, stroke_width=4)
        with audio.cue("grow"): self.play(Create(box), run_time=0.6)
        n1 = self.note_in(audio, "This term depends only on the data, not on the model.", -0.5, 26)
        c = Mx(r"-\,\mathbb{E}_{\mathbf{x}\sim\hat p_{\mathrm{data}}}\bigl[\log p_{\mathrm{model}}(\boldsymbol{x})\bigr]", size=38)
        fit(c, 5.4); c.move_to([-0.4, -1.5, 0])
        n61 = T("(5.61)", 28).move_to([3.3, -1.5, 0])
        with audio.cue("draw"): self.play(Write(c), run_time=1.5)
        self.play(FadeIn(n61), run_time=0.25)
        box2 = SurroundingRectangle(c, color=K, buff=0.18, stroke_width=4)
        with audio.cue("grow"): self.play(Create(box2), run_time=0.6)
        n2 = self.note_in(audio, "We only need to minimize this: the same as maximizing (5.59).", -2.7, 24)
        self.wait(1.5)
        return items + [n0, a, b, n60, box, n1, c, n61, box2, n2]

    # D - cross-entropy and matching
    def scene_d(self, audio):
        items = self.heading_in(audio, "Cross-Entropy and Matching")
        r1, t1 = self.card(r"Minimizing KL $=$ minimizing the \textbf{cross-entropy}", 2.0)
        with audio.cue("grow", pan=-0.3): self.play(Create(r1), Write(t1), run_time=1.3)
        r2, t2 = self.card(r"Any negative log-likelihood is a cross-entropy", 0.95)
        with audio.cue("grow", pan=0.0): self.play(Create(r2), Write(t2), run_time=1.3)
        r3, t3 = self.card(r"Mean squared error: Gaussian model", -0.1)
        with audio.cue("grow", pan=0.3): self.play(Create(r3), Write(t3), run_time=1.2)

        ax = Axes(x_range=[-3.5, 3.5, 1], y_range=[0, 0.7, 0.35], x_length=5.6, y_length=1.5, tips=False,
                  axis_config={"color": K, "stroke_width": 3, "include_ticks": False}).move_to([0, -2.0, 0])
        pm = lambda mu, s: (lambda x: np.exp(-(x - mu) ** 2 / (2 * s * s)) / (s * np.sqrt(2 * np.pi)))
        cd = ax.plot(pm(0, 1.0), x_range=[-3.5, 3.5], color=K, stroke_width=7)
        cm0 = DashedVMobject(ax.plot(pm(1.5, 0.6), x_range=[-3.5, 3.5], color=K, stroke_width=5),
                             num_dashes=40, dashed_ratio=0.55)
        cm1 = DashedVMobject(ax.plot(pm(0.0, 1.0), x_range=[-3.5, 3.5], color=K, stroke_width=5),
                             num_dashes=40, dashed_ratio=0.55)
        ld = Mx(r"\hat p_{\mathrm{data}}", size=28).move_to(ax.c2p(-2.4, 0.45))
        lm = Mx(r"p_{\mathrm{model}}", size=28).move_to(ax.c2p(2.6, 0.45))
        with audio.cue("draw"): self.play(Create(ax), Create(cd), Write(ld), run_time=1.2)
        with audio.cue("slide", pan=0.3): self.play(Create(cm0), Write(lm), run_time=1.0)
        with audio.cue("slide", pan=-0.3): self.play(Transform(cm0, cm1), run_time=1.8)
        n = self.note_in(audio, "The model distribution is made to match the data.", -3.15, 26)
        self.wait(1.4)
        return items + [r1, t1, r2, t2, r3, t3, ax, cd, cm0, ld, lm, n]

    # E - NLL and the KL minimum
    def scene_e(self, audio):
        items = self.heading_in(audio, "Negative Log-Likelihood")
        n0 = self.note_in(audio, "In software we minimize a cost function.", 2.25, 28)
        eq = Mx(r"\text{maximum likelihood}", r"\;\Longrightarrow\;", r"\text{minimize NLL}", size=34)
        fit(eq, 7.0); eq.move_to([0, 1.4, 0])
        with audio.cue("draw"): self.play(Write(eq), run_time=1.5)
        eq2 = Mx(r"\mathrm{NLL}", r"=\text{cross-entropy}", size=40).move_to([0, 0.5, 0])
        with audio.cue("draw"): self.play(Write(eq2), run_time=1.1)
        box = SurroundingRectangle(eq2, color=K, buff=0.18, stroke_width=4)
        with audio.cue("grow"): self.play(Create(box), run_time=0.6)

        nl = NumberLine(x_range=[-2, 3, 1], length=6.0, color=K, stroke_width=3,
                        include_numbers=False).move_to([0, -1.1, 0])
        z = Dot(nl.n2p(0), radius=0.12, color=K).set_z_index(5)
        zl = T(r"KL: minimum value $0$", 26).next_to(nl.n2p(0), UP, buff=0.4)
        zt = Line(nl.n2p(0) + UP * 0.2, nl.n2p(0) + DOWN * 0.2, color=K, stroke_width=4)
        with audio.cue("draw"): self.play(Create(nl), Create(zt), run_time=0.9)
        with audio.cue("grow"): self.play(GrowFromCenter(z), FadeIn(zl), run_time=0.8)
        neg = Dot(nl.n2p(-1.3), radius=0.12, color=K).set_z_index(5)
        nlb = T(r"NLL can be negative", 26).next_to(nl.n2p(-1.3), DOWN, buff=0.35)
        ar = Arrow(nl.n2p(0.0) + DOWN * 0.3, nl.n2p(-1.3) + DOWN * 0.05, color=K, buff=0.05, stroke_width=4)
        with audio.cue("slide", pan=-0.3): self.play(GrowArrow(ar), GrowFromCenter(neg), run_time=1.0)
        with audio.cue("type", glyphs=18): self.play(Write(nlb), run_time=1.0)
        n1 = self.note_in(audio, r"when $\boldsymbol{x}$ is real-valued.", -3.1, 28)
        self.wait(1.6)
        return items + [n0, eq, eq2, box, nl, zt, z, zl, neg, nlb, ar, n1]

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
    Page_130().render()
