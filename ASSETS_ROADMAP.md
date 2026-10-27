# DPVisual — Chapter 5+ Asset & Infrastructure Roadmap

Tracking doc for building reusable animation infrastructure before continuing
page-by-page builds. Update the Status column as we go.

Status legend: `TODO` · `IN PROGRESS` · `DONE` · `BLOCKED`

---

## 1. High Impact

| # | Task | Output file(s) | Status | Notes |
|---|------|------------------|--------|-------|
| 1.1 | Shared style/helpers module — `txt()`, `formula()`, `mono()`, `fit_width()`, `type_in()`, `dust_wipe()`, `clear_scene()`, `make_footer()` | `common/chapter5_style.py` | TODO | Every chapter05 page currently redefines these inline. Centralize so all pages import one source of truth. |
| 1.2 | Icon / shape library for recurring ML visuals: neuron/node, small neural-net diagram, dataset table, loss curve, gradient arrow, matrix/grid, pixel grid, parse-tree node | `common/ml_shapes.py` | TODO | Standardize so the same concept looks identical across every page instead of being improvised per-scene. |
| 1.3 | Color-to-concept mapping, locked in as constants | `common/palette.py` | TODO | e.g. CYAN = input/data, GREEN = correct/output, RED = error/missing/anomaly, YELLOW = key formula, PURPLE = probability/distribution. Import everywhere instead of re-picking per page. |

---

## 2. Medium Impact

| # | Task | Output file(s) | Status | Notes |
|---|------|------------------|--------|-------|
| 2.1 | Reusable "build-up" animation preset — layered neural-net node reveal (layer by layer, connecting lines animate in) | `common/anim_presets.py` | TODO | Needed soon for backprop / CNN / RNN diagrams later in the chapter. |
| 2.2 | Reusable "highlight pulse" preset — draw attention to one term in a formula or one box in a diagram | `common/anim_presets.py` | TODO | Same file as 2.1. |
| 2.3 | Refactor `page_96.py`–`page_101.py` to import from the new common modules (optional backfill) | `scenes/chapter05/page_9*.py` | TODO | Not required for new pages to work, but keeps the whole chapter visually/code-consistent. Can be deferred. |

---

## 3. Music — Generation & Alignment

| # | Task | Output file(s) | Status | Notes |
|---|------|------------------|--------|-------|
| 3.1 | Source open-source piano/guitar/drum samples or loops (royalty-free / CC0) | `assets/audio/raw/` | TODO | Need to pick a concrete source (e.g. Freesound, OpenGameArt, or a free soundfont + render chain) — decide library before downloading. |
| 3.2 | Build or assemble the actual Chapter 5 music track (intro → beat-drop → rising build) per the piano+guitar+drums prompt | `assets/audio/chapter05_theme.wav` (or per-page variants) | TODO | Depends on 3.1. May use a generator (Flow/MusicFX) output as source, or fully open-source instruments if generator output isn't usable commercially. |
| 3.3 | Music–animation alignment system: a small script/helper that takes total scene runtime (sum of `run_time`/`wait()` calls) and either trims/stretches the track or outputs marker timestamps (intro end, beat-drop, build points) to sync against | `common/music_sync.py` | TODO | Needed so every page's render automatically know where the "drop" should land relative to the first zoom transition. |
| 3.4 | Mux audio into rendered page video (ffmpeg step) | `render.py` (extend) or `common/mux_audio.py` | TODO | Final step tying video + synced audio together per page. |

---

## 4. Next Page Render

| # | Task | Status | Notes |
|---|------|--------|-------|
| 4.1 | Page 102 — build using the new common modules once 1.1–1.3 are done | TODO | Blocked on section 1 being complete. |

---

## Build Order (recommended)

1. `common/palette.py` (1.3) — quick, everything else depends on it
2. `common/chapter5_style.py` (1.1) — core helpers, imports palette
3. `common/ml_shapes.py` (1.2) — diagram pieces, imports palette + style
4. `common/anim_presets.py` (2.1, 2.2) — imports palette + style
5. Page 102 render using all of the above (4.1)
6. Music sourcing (3.1) → track build (3.2) → sync system (3.3) → mux step (3.4)
7. Optional: backfill pages 96–101 (2.3)

---

_Last updated: start of session — nothing built yet._
