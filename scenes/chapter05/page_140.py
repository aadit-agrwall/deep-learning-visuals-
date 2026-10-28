from manim import *
import numpy as np, json as _json
from pathlib import Path
from PIL import Image
from common.chapter5_style import Chapter5Scene
from common.asmr_sync import ASMRSync

PAGE = "140"
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
def gauss(mu, s):
    return lambda x: np.exp(-(x - mu) ** 2 / (2 * s * s)) / (s * np.sqrt(2 * np.pi))
def dashed(m, n=40, r=0.55):
    return DashedVMobject(m, num_dashes=n, dashed_ratio=r)


class Page_140(Chapter5Scene):
    PAGE_NO = "140"

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

    def card(self, text, y, size=26, h=0.9, w=7.2, x=0.0):
        r = RoundedRectangle(width=w, height=h, corner_radius=0.2, stroke_color=K,
                             stroke_width=3, fill_opacity=0).move_to([x, y, 0])
        t = Tex(text, color=K, font_size=size); fit(t, w - 0.4); t.move_to(r)
        return r, t

    def axes(self, xr, yr, xl, yl, pos):
        return Axes(x_range=xr, y_range=yr, x_length=xl, y_length=yl, tips=False,
                    axis_config={"color": K, "stroke_width": 3, "include_ticks": False}).move_to(pos)

    # A - efficient kernel vs explicit phi
    def scene_a(self, audio):
        items = self.heading_in(audio, "Efficient Kernels")
        n0 = self.note_in(audio, "Two routes to the same similarity value:", 2.35, 24)
        r1, t1 = self.card(r"Naive: build $\phi(\boldsymbol{x})$ and $\phi(\boldsymbol{x}')$, then dot them", 1.35, 22, 0.8)
        with audio.cue("grow", pan=-0.3): self.play(Create(r1), Write(t1), run_time=1.3)
        r2, t2 = self.card(r"Kernel: evaluate $k(\boldsymbol{x},\boldsymbol{x}')$ directly", 0.35, 24, 0.8)
        with audio.cue("grow", pan=0.3): self.play(Create(r2), Write(t2), run_time=1.2)
        a1 = Arrow([-2.2, -0.45, 0], [-2.2, -1.25, 0], color=K, buff=0, stroke_width=4, tip_length=0.18)
        a2 = Arrow([2.2, -0.45, 0], [2.2, -1.25, 0], color=K, buff=0, stroke_width=4, tip_length=0.18)
        s1 = Mx(r"\phi(\boldsymbol{x})\cdot\phi(\boldsymbol{x}')", size=30).move_to([-2.2, -1.75, 0])
        s2 = Mx(r"k(\boldsymbol{x},\boldsymbol{x}')", size=30).move_to([2.2, -1.75, 0])
        with audio.cue("slide", pan=-0.3): self.play(GrowArrow(a1), Write(s1), run_time=0.9)
        with audio.cue("slide", pan=0.3): self.play(GrowArrow(a2), Write(s2), run_time=0.9)
        eq = Mx(r"=", size=40).move_to([0, -1.75, 0])
        with audio.cue("draw"): self.play(Write(eq), run_time=0.5)
        n1 = self.note_in(audio, "Same answer, far less computation.", -2.75, 26)
        n2 = self.note_in(audio, "k often admits a significantly more efficient implementation.", -3.35, 20)
        self.wait(1.4)
        return items + [n0, r1, t1, r2, t2, a1, a2, s1, s2, eq, n1, n2]

    # B - infinite dimensional phi, min kernel
    def scene_b(self, audio):
        items = self.heading_in(audio, "Infinite Dimensions")
        n0 = self.note_in(audio, r"Map a nonnegative integer $x$ to a vector:", 2.35, 22)
        r1, t1 = self.card(r"$\phi(x)$: $x$ ones followed by infinitely many zeros", 1.45, 24, 0.8)
        with audio.cue("grow", pan=-0.3): self.play(Create(r1), Write(t1), run_time=1.3)
        # bit rows for x=3 and x'=5
        def row(count, y, label):
            cells = VGroup()
            for i in range(10):
                sq = Square(side_length=0.42, color=K, stroke_width=3).move_to([-2.6 + 0.46 * i, y, 0])
                if i < count: sq.set_fill(K, opacity=1)
                cells.add(sq)
            lab = Mx(label, size=26).next_to(cells, LEFT, buff=0.25)
            dots = Mx(r"\cdots", size=28).next_to(cells, RIGHT, buff=0.15)
            return cells, lab, dots
        c1, l1, d1 = row(3, 0.45, r"\phi(3)")
        c2, l2, d2 = row(5, -0.25, r"\phi(5)")
        with audio.cue("grow", pan=-0.3): self.play(LaggedStart(*[FadeIn(s) for s in c1], lag_ratio=0.08), FadeIn(l1), FadeIn(d1), run_time=1.2)
        with audio.cue("grow", pan=0.3): self.play(LaggedStart(*[FadeIn(s) for s in c2], lag_ratio=0.08), FadeIn(l2), FadeIn(d2), run_time=1.2)
        ov = SurroundingRectangle(VGroup(*c1[0:3], *c2[0:3]), color=K, buff=0.06, stroke_width=4)
        with audio.cue("grow"): self.play(Create(ov), run_time=0.7)
        e = Mx(r"k(x,x^{(i)})", r"=", r"\min(x,x^{(i)})", size=38)
        fit(e, 5.2); e.move_to([0, -1.35, 0])
        with audio.cue("draw"): self.play(Write(e), run_time=1.6)
        bx = SurroundingRectangle(e[2], color=K, buff=0.1, stroke_width=4)
        with audio.cue("grow"): self.play(Create(bx), run_time=0.5)
        r2, t2 = self.card(r"Exactly equals the infinite-dimensional dot product", -2.35, 24, 0.8)
        with audio.cue("grow", pan=0.3): self.play(Create(r2), Write(t2), run_time=1.2)
        n1 = self.note_in(audio, r"Tractable $k$ even when $\phi$ is intractable.", -3.25, 22)
        self.wait(1.4)
        return items + [n0, r1, t1, c1, l1, d1, c2, l2, d2, ov, e, bx, r2, t2, n1]

    # C - Gaussian / RBF kernel, eq 5.84
    def scene_c(self, audio):
        items = self.heading_in(audio, "The Gaussian Kernel")
        n0 = self.note_in(audio, "The most commonly used kernel:", 2.35, 24)
        e = Mx(r"k(\boldsymbol{u},\boldsymbol{v})", r"=", r"\mathcal{N}(\boldsymbol{u}-\boldsymbol{v};0,\sigma^{2}\boldsymbol{I})", size=38)
        fit(e, 5.8); e.move_to([-0.3, 1.45, 0])
        n84 = T("(5.84)", 28).move_to([3.3, 1.45, 0])
        with audio.cue("draw"): self.play(Write(e), run_time=2.2)
        self.play(FadeIn(n84), run_time=0.25)
        box = SurroundingRectangle(e[2], color=K, buff=0.1, stroke_width=4)
        with audio.cue("grow"): self.play(Create(box), run_time=0.6)
        ax = self.axes([-3.5, 3.5, 1], [0, 0.5, 1], 5.2, 1.6, [0, -0.1, 0])
        bell = ax.plot(gauss(0, 1.0), x_range=[-3.5, 3.5], color=K, stroke_width=7)
        with audio.cue("draw"): self.play(Create(ax), run_time=0.6)
        with audio.cue("slide", pan=0.3): self.play(Create(bell), run_time=1.3)
        ul = Mx(r"\boldsymbol{u}", size=28).next_to(ax.c2p(0, 0), DOWN, buff=0.1)
        vl = Mx(r"\boldsymbol{v}", size=28).next_to(ax.c2p(2.2, 0), DOWN, buff=0.1)
        dv = dashed(Line(ax.c2p(2.2, 0), ax.c2p(2.2, gauss(0, 1.0)(2.2)), color=K, stroke_width=3), 8, 0.5)
        with audio.cue("grow"): self.play(FadeIn(ul), FadeIn(vl), Create(dv), run_time=0.7)
        r1, t1 = self.card(r"Also the \textbf{radial basis function} (RBF) kernel", -1.65, 24, 0.8)
        with audio.cue("grow", pan=-0.3): self.play(Create(r1), Write(t1), run_time=1.2)
        r2, t2 = self.card(r"Value decreases along lines in $\boldsymbol{v}$ space radiating from $\boldsymbol{u}$", -2.6, 21, 0.8)
        with audio.cue("grow", pan=0.3): self.play(Create(r2), Write(t2), run_time=1.3)
        n1 = self.note_in(audio, "A dot product in an infinite-dimensional space.", -3.4, 22)
        self.wait(1.4)
        return items + [n0, e, n84, box, ax, bell, ul, vl, dv, r1, t1, r2, t2, n1]

    # D - template matching
    def scene_d(self, audio):
        items = self.heading_in(audio, "Template Matching")
        n0 = self.note_in(audio, r"A training example $\boldsymbol{x}$ with label $y$ becomes a template:", 2.35, 21)
        ax = self.axes([-3, 3, 1], [-2, 2, 1], 4.6, 2.6, [0, 0.55, 0])
        tmpl = Dot(ax.c2p(-0.4, 0.2), radius=0.15, color=K).set_z_index(5)
        ring1 = dashed(Circle(radius=0.55, color=K, stroke_width=4).move_to(tmpl), 16, 0.5)
        ring2 = dashed(Circle(radius=1.05, color=K, stroke_width=3).move_to(tmpl), 24, 0.4)
        others = [Square(side_length=0.2, color=K, stroke_width=3).move_to(ax.c2p(x, y)) for x, y in [(2.0, 1.2), (1.8, -1.3), (-2.3, -1.2)]]
        with audio.cue("draw"): self.play(Create(ax), run_time=0.6)
        with audio.cue("grow", pan=-0.3): self.play(GrowFromCenter(tmpl), Create(ring1), Create(ring2), run_time=1.0)
        with audio.cue("grow", pan=0.3): self.play(*[GrowFromCenter(o) for o in others], run_time=0.7)
        tl = Mx(r"\boldsymbol{x}", size=26).next_to(tmpl, DOWN, buff=0.12)
        near = Dot(ax.c2p(0.4, 0.5), radius=0.12, color=K).set_z_index(5)
        nl = Mx(r"\boldsymbol{x}'", size=26).next_to(near, UP, buff=0.1)
        with audio.cue("grow"): self.play(FadeIn(tl), GrowFromCenter(near), FadeIn(nl), run_time=0.7)
        link = Line(tmpl.get_center(), near.get_center(), color=K, stroke_width=5)
        with audio.cue("slide"): self.play(Create(link), run_time=0.6)
        r1, t1 = self.card(r"Test point $\boldsymbol{x}'$ near $\boldsymbol{x}$: large kernel response", -1.45, 22, 0.8)
        with audio.cue("grow", pan=-0.3): self.play(Create(r1), Write(t1), run_time=1.3)
        r2, t2 = self.card(r"Large weight on the associated label $y$", -2.4, 24, 0.8)
        with audio.cue("grow", pan=0.3): self.play(Create(r2), Write(t2), run_time=1.2)
        n1 = self.note_in(audio, "Prediction: training labels weighted by similarity.", -3.3, 22)
        self.wait(1.4)
        return items + [n0, ax, tmpl, ring1, ring2] + others + [tl, near, nl, link, r1, t1, r2, t2, n1]

    # E - kernel machines, cost, support vectors
    def scene_e(self, audio):
        items = self.heading_in(audio, "Kernel Machines")
        r1, t1 = self.card(r"Kernel trick enhances many linear models: \textbf{kernel methods}", 2.15, 22, 0.8)
        with audio.cue("grow", pan=-0.3): self.play(Create(r1), Write(t1), run_time=1.3)
        r2, t2 = self.card(r"Drawback: decision cost is linear in training examples", 1.2, 22, 0.8)
        with audio.cue("grow", pan=0.3): self.play(Create(r2), Write(t2), run_time=1.3)
        e = Mx(r"\alpha_i\,k(\boldsymbol{x},\boldsymbol{x}^{(i)})", size=34).move_to([0, 0.3, 0])
        with audio.cue("draw"): self.play(Write(e), run_time=1.2)
        bars = VGroup(); labels = VGroup()
        vals = [0, 0.9, 0, 0, 0.6, 0, 0.75, 0, 0, 0]
        for i, v in enumerate(vals):
            x = -2.25 + 0.5 * i
            base = Line([x - 0.15, -1.35, 0], [x + 0.15, -1.35, 0], color=K, stroke_width=4)
            bars.add(base)
            if v > 0:
                bars.add(Rectangle(width=0.3, height=v, stroke_color=K, stroke_width=3, fill_color=K, fill_opacity=1).move_to([x, -1.35 + v / 2, 0]))
        with audio.cue("slide"): self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.06), run_time=1.3)
        al = Mx(r"\alpha_i", size=28).move_to([-3.1, -1.0, 0])
        ml = T("mostly zeros", 22).move_to([0.0, -1.85, 0])
        with audio.cue("grow"): self.play(FadeIn(al), FadeIn(ml), run_time=0.6)
        r3, t3 = self.card(r"Nonzero $\alpha_i$: \textbf{support vectors}", -2.65, 26, 0.8)
        with audio.cue("grow", pan=-0.3): self.play(Create(r3), Write(t3), run_time=1.2)
        n1 = self.note_in(audio, "Training cost is also high for large datasets (section 5.9).", -3.5, 20)
        self.wait(1.4)
        return items + [r1, t1, r2, t2, e, bars, al, ml, r3, t3, n1]

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
    Page_140().render()
