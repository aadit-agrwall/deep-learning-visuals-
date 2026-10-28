from manim import *
import numpy as np

K = "#000000"
PAPER = "#FFFFFF"
WHITE_BG = PAPER
ACCENT = "#1F4FFF"   # the ONLY extra color: use it to show change (firing, selection)

VIEWS = {
    "iso":    (62 * DEGREES, -50 * DEGREES),
    "flat":   (0.0,          -90 * DEGREES),   # looks exactly like a 2D scene
    "top":    (0.01,         -90 * DEGREES),
    "side":   (90 * DEGREES, -90 * DEGREES),
    "front":  (90 * DEGREES,   0 * DEGREES),
    "back34": (68 * DEGREES, -130 * DEGREES),
    "low":    (80 * DEGREES,  -60 * DEGREES),
    "high":   (35 * DEGREES,  -60 * DEGREES),
}


def _view(name):
    if name not in VIEWS:
        raise ValueError(f"unknown view '{name}', choose from {list(VIEWS)}")
    return VIEWS[name]


def _bw(mob, fill=0.9, sw=1.5):
    mob.set_fill(PAPER, opacity=fill)
    mob.set_stroke(K, width=sw)
    return mob


def _unit(v):
    v = np.array(v, dtype=float)
    n = np.linalg.norm(v)
    return v / n if n > 1e-9 else np.array([0.0, 0.0, 1.0])


# ---------------------------------------------------------------- primitives
def box(size=(1, 1, 1), at=ORIGIN, sw=3):
    p = Prism(dimensions=list(size), fill_color=PAPER, fill_opacity=0.9,
              stroke_color=K, stroke_width=sw)
    return p.move_to(np.array(at, dtype=float))


def cylinder(radius=0.6, height=1.6, at=ORIGIN, direction=OUT):
    c = Cylinder(radius=radius, height=height, direction=direction, resolution=(20, 24))
    return _bw(c, 0.9, 1.2).move_to(np.array(at, dtype=float))


def sphere(radius=0.7, at=ORIGIN):
    s = Sphere(radius=radius, resolution=(14, 28))
    return _bw(s, 0.9, 1.0).move_to(np.array(at, dtype=float))


def cone(radius=0.6, height=1.4, at=ORIGIN, direction=OUT):
    c = Cone(base_radius=radius, height=height, direction=direction, show_base=True)
    return _bw(c, 0.9, 1.2).move_to(np.array(at, dtype=float))


def torus(major=1.0, minor=0.35, at=ORIGIN):
    t = Torus(major_radius=major, minor_radius=minor)
    return _bw(t, 0.9, 1.0).move_to(np.array(at, dtype=float))


def arrow3d(a, b, thickness=0.025, color=K):
    return Arrow3D(start=np.array(a, dtype=float), end=np.array(b, dtype=float),
                   thickness=thickness, color=color)


def segment(a, b, width=3, color=K, dashed=False):
    a = np.array(a, dtype=float); b = np.array(b, dtype=float)
    if dashed:
        return DashedLine(a, b, color=color, stroke_width=width)
    return Line(a, b, color=color, stroke_width=width)


def axes3d(xr=(-3, 3, 1), yr=(-3, 3, 1), zr=(0, 3, 1), lengths=(6, 6, 3)):
    return ThreeDAxes(x_range=list(xr), y_range=list(yr), z_range=list(zr),
                      x_length=lengths[0], y_length=lengths[1], z_length=lengths[2],
                      axis_config={"color": K, "stroke_width": 2, "include_ticks": False})


def grid_floor(half=3, step=1, z=0.0, opacity=0.22):
    g = VGroup()
    for v in np.arange(-half, half + 1e-6, step):
        g.add(Line([v, -half, z], [v, half, z], color=K, stroke_width=1, stroke_opacity=opacity))
        g.add(Line([-half, v, z], [half, v, z], color=K, stroke_width=1, stroke_opacity=opacity))
    return g


def curve3d(fn, t_range=(0, 1), color=K, width=5):
    return ParametricFunction(lambda t: np.array(fn(t), dtype=float),
                              t_range=list(t_range), color=color, stroke_width=width)


# ------------------------------------------------------------------ surfaces
def surface(fn, u_range=(-2.5, 2.5), v_range=(-2.5, 2.5), res=(22, 22)):
    return Surface(lambda u, v: np.array([u, v, fn(u, v)]),
                   u_range=list(u_range), v_range=list(v_range), resolution=res,
                   fill_color=PAPER, fill_opacity=0.85, stroke_color=K, stroke_width=1,
                   checkerboard_colors=False)


def bowl_surface(k=0.15, rng=2.5, res=(22, 22)):
    return surface(lambda u, v: k * (u * u + v * v), (-rng, rng), (-rng, rng), res)


def saddle_surface(k=0.18, rng=2.5, res=(22, 22)):
    return surface(lambda u, v: k * (u * u - v * v) + 1.2, (-rng, rng), (-rng, rng), res)


def gaussian_surface(mu=(0, 0), sigma=1.0, height=2.0, rng=3.0, res=(24, 24)):
    f = lambda u, v: height * np.exp(-((u - mu[0]) ** 2 + (v - mu[1]) ** 2) / (2 * sigma ** 2))
    return surface(f, (-rng, rng), (-rng, rng), res)


# ------------------------------------------------------- data / math objects
def plane_poly(center=ORIGIN, normal=OUT, size=3.0, fill=0.25):
    n = _unit(normal)
    helper = np.array([1.0, 0.0, 0.0]) if abs(n[0]) < 0.9 else np.array([0.0, 1.0, 0.0])
    u = _unit(np.cross(n, helper)); v = np.cross(n, u)
    c = np.array(center, dtype=float)
    pts = [c + size * (a * u + b * v) for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    p = Polygon(*pts, color=K, stroke_width=2)
    p.set_fill(PAPER, opacity=fill)
    return p


def scatter_classes(n=12, seed=3, sep=2.0, spread=0.55, center=ORIGIN):
    """Two classes split by the plane through `center` with normal (1,1,1).
    Returns (pos_group of dots, neg_group of cubes, pos_pts, neg_pts)."""
    rng = np.random.default_rng(seed)
    u = _unit((1, 1, 1)); c = np.array(center, dtype=float)
    pos_pts = [c + u * sep / 2 + rng.normal(0, spread, 3) for _ in range(n)]
    neg_pts = [c - u * sep / 2 + rng.normal(0, spread, 3) for _ in range(n)]
    pos = VGroup(*[Dot3D(p, radius=0.1, color=K) for p in pos_pts])
    neg = VGroup(*[box((0.2, 0.2, 0.2), p, sw=1.5) for p in neg_pts])
    return pos, neg, pos_pts, neg_pts


def bars3d(grid, cell=0.5, gap=0.12, height_scale=1.0, at=ORIGIN):
    g = np.array(grid, dtype=float)
    R, C = g.shape
    if R * C > 100:
        raise ValueError("bars3d: max 100 bars")
    at = np.array(at, dtype=float); out = VGroup()
    for i in range(R):
        for j in range(C):
            h = max(float(g[i, j]) * height_scale, 0.04)
            x = (j - (C - 1) / 2) * (cell + gap)
            y = ((R - 1) / 2 - i) * (cell + gap)
            out.add(box((cell, cell, h), at + np.array([x, y, h / 2]), sw=2))
    return out


def matrix_grid(rows=4, cols=4, cell=0.5, at=ORIGIN, z=0.0):
    at = np.array(at, dtype=float); out = VGroup()
    for i in range(rows):
        for j in range(cols):
            s = Square(side_length=cell, color=K, stroke_width=2)
            s.set_fill(PAPER, opacity=0.95)
            s.move_to(at + np.array([(j - (cols - 1) / 2) * cell, ((rows - 1) / 2 - i) * cell, z]))
            out.add(s)
    return out


def grid_cell(grid, cols, i, j):
    return grid[i * cols + j]


def voxels(shape=(2, 2, 2), cell=0.5, gap=0.06, at=ORIGIN):
    a, b, c = shape
    if a * b * c > 125:
        raise ValueError("voxels: max 125 cells")
    at = np.array(at, dtype=float); out = VGroup()
    for i in range(a):
        for j in range(b):
            for k in range(c):
                p = at + np.array([(i - (a - 1) / 2) * (cell + gap),
                                   (j - (b - 1) / 2) * (cell + gap),
                                   (k - (c - 1) / 2) * (cell + gap)])
                out.add(box((cell, cell, cell), p, sw=1.5))
    return out


def cnn_stack(n=4, w=1.6, h=1.6, depth=0.12, gap=0.35, at=ORIGIN):
    at = np.array(at, dtype=float); out = VGroup()
    for k in range(n):
        out.add(box((depth, w, h), at + np.array([(k - (n - 1) / 2) * gap, 0, 0]), sw=2))
    return out


# ------------------------------------------------------ neural nets (legacy)
def neural_net(layers=(3, 5, 5, 2), gap_x=2.0, spread=1.0):
    pos = []
    for li, n in enumerate(layers):
        cols = int(np.ceil(np.sqrt(n))); rows = int(np.ceil(n / cols)); pts = []
        for k in range(n):
            r, c = divmod(k, cols)
            pts.append(np.array([(li - (len(layers) - 1) / 2) * gap_x,
                                 (c - (cols - 1) / 2) * spread,
                                 ((rows - 1) / 2 - r) * spread]))
        pos.append(pts)
    layer_groups = VGroup(*[VGroup(*[Dot3D(p, radius=0.12, color=K) for p in pts]) for pts in pos])
    edges = VGroup()
    for a, b in zip(pos[:-1], pos[1:]):
        for p in a:
            for q in b:
                edges.add(Line(p, q, color=K, stroke_width=1.2, stroke_opacity=0.35))
    return layer_groups, edges, pos


# ------------------------------------------------------------- Net3D (blue)
class Net3D:
    def __init__(self, layers=(3, 4, 4, 2), gap_x=2.2, spread=1.0, node_r=0.13,
                 max_edges=240, at=ORIGIN):
        self.layers = tuple(layers)
        at = np.array(at, dtype=float)
        self.pos = []
        for li, n in enumerate(self.layers):
            cols = int(np.ceil(np.sqrt(n))); rows = int(np.ceil(n / cols)); pts = []
            for k in range(n):
                r, c = divmod(k, cols)
                pts.append(at + np.array([(li - (len(self.layers) - 1) / 2) * gap_x,
                                          (c - (cols - 1) / 2) * spread,
                                          ((rows - 1) / 2 - r) * spread]))
            self.pos.append(pts)
        self.nodes = [VGroup(*[Dot3D(p, radius=node_r, color=K) for p in pts]) for pts in self.pos]
        total = sum(len(a) * len(b) for a, b in zip(self.pos[:-1], self.pos[1:]))
        stride = max(1, int(np.ceil(total / max(max_edges, 1))))
        self.edges = []
        for a, b in zip(self.pos[:-1], self.pos[1:]):
            pairs = [(p, q) for p in a for q in b][::stride]
            self.edges.append(VGroup(*[Line(p, q, color=K, stroke_width=1.2, stroke_opacity=0.35)
                                       for p, q in pairs]))
        self.group = VGroup(*self.nodes, *self.edges)

    def reveal(self, scene, run=3.0):
        scene.play(LaggedStart(*[FadeIn(g) for g in self.nodes], lag_ratio=0.25), run_time=run * 0.45)
        if self.edges:
            scene.play(*[Create(e, lag_ratio=0.02) for e in self.edges], run_time=run * 0.55)

    def fire_layer(self, scene, i, idx=None, run=0.7):
        grp = self.nodes[i]
        sel = list(grp) if idx is None else [grp[k] for k in idx]
        anims = [d.animate.set_color(ACCENT) for d in sel]
        if i > 0 and len(self.edges[i - 1]) > 0:
            es = list(self.edges[i - 1])
            es = es[::max(1, int(np.ceil(len(es) / 80)))]
            anims += [ShowPassingFlash(e.copy().set_stroke(ACCENT, width=3.5, opacity=1),
                                       time_width=0.8) for e in es]
        if anims:
            scene.play(*anims, run_time=run)

    def forward_pass(self, scene, step=0.7):
        for i in range(len(self.layers)):
            self.fire_layer(scene, i, run=step)

    def reset(self, scene, run=0.5):
        anims = [d.animate.set_color(K) for g in self.nodes for d in g]
        if anims:
            scene.play(*anims, run_time=run)

    def fade(self, scene, run=0.7):
        scene.play(FadeOut(self.group), run_time=run)


# -------------------------------------------------------- Perceptron3D (blue)
class Perceptron3D:
    def __init__(self, n_in=3, gap=2.4, spread=1.2, at=ORIGIN):
        at = np.array(at, dtype=float); self.n_in = n_in
        self.in_pos = [at + np.array([-gap, (k - (n_in - 1) / 2) * spread, 0.0]) for k in range(n_in)]
        self.sum_pos = at.copy(); self.out_pos = at + np.array([gap, 0.0, 0.0])
        self.inputs = VGroup(*[Dot3D(p, radius=0.16, color=K) for p in self.in_pos])
        self.sum_node = sphere(0.34, self.sum_pos)
        self.out_node = box((0.4, 0.4, 0.4), self.out_pos)
        self.w_edges = VGroup(*[Line(p, self.sum_pos, color=K, stroke_width=3) for p in self.in_pos])
        self.out_edge = Line(self.sum_pos, self.out_pos, color=K, stroke_width=3)
        self.group = VGroup(self.inputs, self.w_edges, self.sum_node, self.out_edge, self.out_node)

    def reveal(self, scene, run=1.4):
        scene.play(FadeIn(self.inputs), Create(self.w_edges), FadeIn(self.sum_node),
                   Create(self.out_edge), FadeIn(self.out_node), run_time=run)

    def fire(self, scene, active=None, step=0.7):
        act = list(range(self.n_in)) if active is None else list(active)
        if not act:
            return
        scene.play(*[self.inputs[k].animate.set_color(ACCENT) for k in act], run_time=step * 0.6)
        scene.play(*[ShowPassingFlash(self.w_edges[k].copy().set_stroke(ACCENT, width=5, opacity=1),
                                      time_width=0.8) for k in act], run_time=step)
        scene.play(self.sum_node.animate.set_color(ACCENT), run_time=step * 0.6)
        scene.play(ShowPassingFlash(self.out_edge.copy().set_stroke(ACCENT, width=5, opacity=1),
                                    time_width=0.8), run_time=step)
        scene.play(self.out_node.animate.set_color(ACCENT), run_time=step * 0.6)

    def reset(self, scene, run=0.5):
        parts = list(self.inputs) + [self.sum_node, self.out_node]
        scene.play(*[m.animate.set_color(K) for m in parts], run_time=run)

    def fade(self, scene, run=0.7):
        scene.play(FadeOut(self.group), run_time=run)


# ------------------------------------------------------------------- stage
class Stage3D(ThreeDScene):
    """Use view('flat') for ordinary 2D content, then move to iso/top/side for 3D."""

    def _items(self):
        if not hasattr(self, "_stage"):
            self._stage = []
        return self._stage

    def setup_stage(self, view="iso", zoom=0.85):
        self.camera.background_color = PAPER; config.background_color = PAPER
        self._stage = []; self._cap = None
        phi, theta = _view(view)
        self.set_camera_orientation(phi=phi, theta=theta, zoom=zoom)

    # camera
    def view(self, name, run=2.2, zoom=None):
        phi, theta = _view(name)
        kw = dict(phi=phi, theta=theta, run_time=run, rate_func=smooth)
        if zoom:
            kw["zoom"] = zoom
        self.move_camera(**kw)

    def tour(self, names, run=2.2, hold=0.4):
        for n in names:
            self.view(n, run); self.wait(hold)

    def orbit(self, angle=PI / 2, run=4.0):
        self.move_camera(theta=self.camera.get_theta() + angle, run_time=run, rate_func=smooth)

    def dolly(self, zoom, run=2.0):
        self.move_camera(zoom=zoom, run_time=run, rate_func=smooth)

    def spin(self, run=4.0, rate=0.15):
        self.begin_ambient_camera_rotation(rate=rate)
        self.wait(run)
        self.stop_ambient_camera_rotation()

    # text
    def hud(self, text, size=34, pos=UP * 3.3):
        t = Tex(text, color=K, font_size=size).move_to(pos)
        self.add_fixed_in_frame_mobjects(t)
        return t

    def caption(self, text, size=34, pos=UP * 3.3, run=0.7):
        old = getattr(self, "_cap", None)
        t = Tex(text, color=K, font_size=size)
        if t.width > 7.4:
            t.scale_to_fit_width(7.4)
        t.move_to(pos)
        self.add_fixed_in_frame_mobjects(t)
        if old is not None:
            self.play(FadeOut(old), Write(t), run_time=run)
        else:
            self.play(Write(t), run_time=run)
        self._cap = t
        return t

    def label3d(self, text, pos, size=26):
        t = Tex(text, color=K, font_size=size).move_to(np.array(pos, dtype=float))
        self.add_fixed_orientation_mobjects(t)
        self._items().append(t)
        return t

    # staging
    def reveal(self, *mobs, anim="fade", run=1.0):
        kinds = {"fade": FadeIn, "create": Create, "grow": GrowFromCenter}
        if anim not in kinds:
            raise ValueError(f"anim must be one of {list(kinds)}")
        self.play(*[kinds[anim](m) for m in mobs], run_time=run)
        self._items().extend(mobs)

    def keep(self, *mobs):
        self._items().extend(mobs)

    def clear_scene(self, run=0.7):
        items = list(self._items())
        cap = getattr(self, "_cap", None)
        if cap is not None:
            items.append(cap)
        if items:
            self.play(*[FadeOut(m) for m in items], run_time=run)
        self._stage = []; self._cap = None

    # blue (change) helpers
    def blue(self, mob, run=0.6):
        self.play(mob.animate.set_color(ACCENT), run_time=run)

    def unblue(self, mob, run=0.6):
        self.play(mob.animate.set_color(K), run_time=run)

    def pulse(self, mob, scale=1.35, run=0.8):
        self.play(mob.animate.set_color(ACCENT).scale(scale), run_time=run * 0.5)
        self.play(mob.animate.set_color(K).scale(1 / scale), run_time=run * 0.5)

    def signal(self, a, b, run=0.8, width=6):
        ln = Line(np.array(a, dtype=float), np.array(b, dtype=float), color=ACCENT, stroke_width=width)
        self.play(ShowPassingFlash(ln, time_width=0.6), run_time=run)
