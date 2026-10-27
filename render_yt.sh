#!/bin/bash
cd ~/Documents/dpvisual
PAGES="125 126 127 128 129 130"
FPS=30
OUT=assets/user-data/output
mkdir -p "$OUT" /tmp/yt

CHK=$(find . -type f -name chapter5_style.py -not -path './.venv/*' | head -1)
COMMON_PARENT=$(cd "$(dirname "$(dirname "$CHK")")" && pwd)
export PYTHONPATH="$COMMON_PARENT:$PWD"

# runner: 16:9 2K plus cue logging, no page file is edited
cat > /tmp/yt_run.py << 'PY'
import sys, json, importlib.util
from pathlib import Path
from manim import config, Scene

page, fps = sys.argv[1], int(sys.argv[2])
path = Path(f"scenes/chapter05/page_{page}.py")

config.input_file = str(path)
config.pixel_width = 2560
config.pixel_height = 1440
config.frame_rate = fps
config.frame_height = 8.0
config.frame_width = 8.0 * 16 / 9

import common.asmr_sync as asm

CUR, LOG = {}, []
CUE_FILE = f"/tmp/yt_cues_{page}.json"

_orig_render = Scene.render
def _render(self, *a, **k):
    CUR["scene"] = self
    return _orig_render(self, *a, **k)
Scene.render = _render

def apply_cfg():
    config.pixel_width = 2560
    config.pixel_height = 1440
    config.frame_rate = fps
    config.frame_height = 8.0
    config.frame_width = 8.0 * 16 / 9

_orig_init = Scene.__init__
def _init(self, *a, **k):
    apply_cfg()
    _orig_init(self, *a, **k)
Scene.__init__ = _init

def now():
    s = CUR["scene"]
    try: return float(s.renderer.time)
    except Exception: return float(s.time)

class Ctx:
    def __init__(self, e, c): self.e, self.c = e, c
    def __enter__(self):
        self.e["t"] = now()
        return self.c.__enter__()
    def __exit__(self, *x):
        self.e["end"] = now()
        r = self.c.__exit__(*x)
        json.dump(LOG, open(CUE_FILE, "w"))
        return r

_orig_cue = asm.ASMRSync.cue
def _cue(self, name, *a, **k):
    e = {"t": now(), "end": now(), "name": name,
         "glyphs": k.get("glyphs", 0), "pan": k.get("pan", 0.0)}
    LOG.append(e)
    return Ctx(e, _orig_cue(self, name, *a, **k))
asm.ASMRSync.cue = _cue

spec = importlib.util.spec_from_file_location(f"page_{page}", path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
apply_cfg()
print('render size:', config.pixel_width, 'x', config.pixel_height)
scene = getattr(mod, f"Page_{page}")()
scene.render()
json.dump(LOG, open(CUE_FILE, "w"))
print("cues:", len(LOG))
PY

FAIL=0
for P in $PAGES; do
  if [ -f /tmp/yt/p$P.mp4 ] && [ -f /tmp/yt_cues_$P.json ]; then
    echo "=== page $P already rendered, skipping ==="
    continue
  fi
  if [ ! -f scenes/chapter05/page_$P.py ]; then
    echo "MISSING scenes/chapter05/page_$P.py"; FAIL=1; continue
  fi
  echo "=== rendering page $P at 2560x1440 ==="
  rm -f /tmp/yt_cues_$P.json
  python3 /tmp/yt_run.py $P $FPS > /tmp/yt_render_$P.log 2>&1
  RC=$?
  if [ $RC -ne 0 ] || [ ! -f /tmp/yt_cues_$P.json ]; then
    echo "PAGE $P FAILED (exit $RC). Last log lines:"; tail -25 /tmp/yt_render_$P.log; FAIL=1; continue
  fi
  V=$(find media/videos/page_$P -name "Page_$P.mp4" -not -path "*partial_movie_files*" -print0 | xargs -0 ls -t | head -1)
  cp "$V" /tmp/yt/p$P.mp4
  W=$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=p=0 /tmp/yt/p$P.mp4)
  if [ "$W" != "2560" ]; then echo "PAGE $P is ${W}px wide, not 2560. Aborting."; rm -f /tmp/yt/p$P.mp4; FAIL=1; continue; fi
  echo "page $P: $(ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate -of csv=p=0 /tmp/yt/p$P.mp4)  $(ffprobe -v error -show_entries format=duration -of csv=p=0 /tmp/yt/p$P.mp4) s"
done

if [ $FAIL -ne 0 ]; then
  echo "At least one page failed. Fix it and run: bash render_yt.sh (finished pages are skipped)."
  exit 1
fi

rm -f /tmp/yt/list.txt; ARGS=""
for P in $PAGES; do
  echo "file '/tmp/yt/p$P.mp4'" >> /tmp/yt/list.txt
  ARGS="$ARGS $P:$(ffprobe -v error -show_entries format=duration -of csv=p=0 /tmp/yt/p$P.mp4)"
done
ffmpeg -y -v error -f concat -safe 0 -i /tmp/yt/list.txt -c copy /tmp/yt/joined.mp4
echo "Joined video: $(ffprobe -v error -show_entries format=duration -of csv=p=0 /tmp/yt/joined.mp4) s"

cat > /tmp/yt_sfx.py << 'PY'
import sys, json, wave
import numpy as np
SR = 44100
LEAD = 0.04
pairs = [a.split(":") for a in sys.argv[2:]]
cues, off = [], 0.0
for p, dur in pairs:
    for c in json.load(open(f"/tmp/yt_cues_{p}.json")):
        c = dict(c); c["t"] += off; c["end"] = c.get("end", c["t"] + 0.8) + off
        cues.append(c)
    off += float(dur)
cues.sort(key=lambda c: c["t"])
N = int((off + 0.5) * SR); L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(11)
def tt(d): return np.arange(int(d * SR)) / SR
def atk(t, a=0.003): return np.minimum(t / a, 1)
def put(sig, start, pan, gain):
    i = int(max(0.0, start) * SR)
    if i >= N: return
    j = min(N, i + len(sig))
    pl = np.cos((pan + 1) * np.pi / 4); pr = np.sin((pan + 1) * np.pi / 4)
    seg = sig[:j - i] * gain
    L[i:j] += seg * pl * 1.414; R[i:j] += seg * pr * 1.414
def mix(a, b):
    n = max(len(a), len(b)); o = np.zeros(n); o[:len(a)] += a; o[:len(b)] += b; return o
def marimba(f, d=0.5):
    t = tt(d)
    return (np.sin(2*np.pi*f*t)*np.exp(-t*7) + 0.35*np.sin(2*np.pi*4*f*t)*np.exp(-t*30)) * atk(t)
def bell(f, d=0.9):
    t = tt(d)
    return np.sin(2*np.pi*f*t + 3.0*np.exp(-t*5)*np.sin(2*np.pi*3.5*f*t)) * np.exp(-t*4.5) * atk(t, 0.002)
def boing(d=0.45):
    t = tt(d); f = 300 + 520*np.exp(-t*16) + 45*np.sin(2*np.pi*20*t)*np.exp(-t*9)
    return np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t*8) * atk(t, 0.002)
def whistle(f0, f1, d=0.4):
    t = tt(d); f = f0 + (f1 - f0) * (t / d) ** 0.8
    s = np.sin(2*np.pi*np.cumsum(f)/SR) + 0.2*np.sin(4*np.pi*np.cumsum(f)/SR)
    return s * np.sin(np.pi * t / d) ** 0.6
def thump(d=0.35):
    t = tt(d); f = 45 + 100*np.exp(-t*28)
    return np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t*9) * atk(t, 0.002)
def riser(d=1.5):
    t = tt(d); f = 220 * (6.5 ** (t / d)); ph = 2*np.pi*np.cumsum(f)/SR
    s = np.sin(ph) + 0.4*np.sin(2*ph) + 0.5*np.sin(ph*1.005)
    return s * (t / d) ** 1.6 * np.minimum((d - t) / 0.03, 1)
SC = [523.25, 587.33, 659.25, 783.99, 880.0, 1046.5, 1174.7, 1318.5]
def hit(): return mix(thump(0.4) * 1.2, bell(1568, 1.0) * 0.5)

k = 0
for c in cues:
    name = c["name"]; t0 = max(0.0, c["t"] - LEAD)
    d = max(0.05, float(c["end"]) - float(c["t"]))
    pan = max(-0.8, min(0.8, float(c.get("pan", 0) or 0)))
    if name == "grow":
        if d > 1.2:
            n = int(min(14, d / 0.18))
            for i in range(n):
                put(marimba(SC[(k + i) % len(SC)], 0.22), t0 + d * 0.95 * i / n, rng.uniform(-0.4, 0.4), 0.24)
            k += n
        else:
            put(mix(boing(), bell(1760, 0.6) * 0.35), t0, pan, 0.42)
    elif name == "zoom":
        if d < 1.0:
            put(hit(), t0, 0.0, 0.42)
        else:
            put(riser(max(d - 0.05, 0.3)), t0, 0.0, 0.26)
            put(hit(), t0 + d - 0.06, 0.0, 0.42)
    elif name == "wipe":
        put(whistle(1100, 380, min(0.45, d)), t0, 0.0, 0.26)
    elif name == "draw":
        n = int(max(1, min(5, d / 0.28)))
        for i in range(n):
            f = SC[(k + 2 * i) % len(SC)]
            put(mix(marimba(f, 0.45), bell(f * 2, 0.4) * 0.25), t0 + d * 0.8 * i / n, pan, 0.30)
        k += 2
    elif name == "slide":
        n = int(max(3, min(7, d / 0.22)))
        for i in range(n):
            put(marimba(SC[(k + i) % len(SC)], 0.3), t0 + d * 0.9 * i / n, pan, 0.22)
        k += 1
    elif name == "type":
        g = max(int(c.get("glyphs", 0)), 8)
        n_b = int(max(3, min(g // 2, d / 0.075))); span = d * 0.95
        idx = int(rng.integers(0, 4))
        for n in range(n_b):
            idx = int(np.clip(idx + rng.integers(-1, 3), 0, len(SC) - 1))
            put(marimba(SC[idx], 0.16), t0 + span * n / n_b, rng.uniform(-0.3, 0.3), 0.13)

x = np.stack([L, R], axis=1); x = np.tanh(1.4 * x)
fi = np.minimum(np.arange(N) / (SR * 0.2), 1); fo = np.minimum((N - np.arange(N)) / (SR * 1.5), 1)
x *= (fi * fo)[:, None]; x = x / max(np.max(np.abs(x)), 1e-6) * 0.8
w = wave.open(sys.argv[1], "wb")
w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((x * 32767).astype(np.int16).tobytes()); w.close()
print("SFX cues used:", len(cues))
PY

python3 /tmp/yt_sfx.py /tmp/yt/sfx_all.wav $ARGS

FINAL="$OUT/deep_learning_p125-130_2k.mp4"
ffmpeg -y -v error -i /tmp/yt/joined.mp4 -i /tmp/yt/sfx_all.wav -map 0:v -map 1:a -c:v copy \
  -af "highpass=f=80,aecho=0.8:0.45:60|120:0.18|0.10,alimiter=limit=0.9" \
  -c:a aac -b:a 256k -shortest -movflags +faststart "$FINAL"

echo "Size / fps:"; ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate -of csv=p=0 "$FINAL"
echo "Streams:";    ffprobe -v error -show_entries stream=codec_type -of csv=p=0 "$FINAL"
echo "Duration:";   ffprobe -v error -show_entries format=duration -of csv=p=0 "$FINAL"
open "$FINAL"
