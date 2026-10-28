import os, sys, importlib
from pathlib import Path
from manim import *
sys.path.insert(0, str(Path(__file__).resolve().parent))
_PG = os.environ.get("PAGE", "135")
_mod = importlib.import_module(f"page_{_PG}")
_Base = getattr(_mod, f"Page_{_PG}")
config.pixel_width = 1440; config.pixel_height = 1440; config.frame_rate = 60
config.frame_width = 8.0; config.frame_height = 8.0


class Content(_Base):
    def construct(self):
        self.camera.background_color = _mod.WHITE_BG; config.background_color = _mod.WHITE_BG
        audio = _mod.CueLogger(self, _mod.ASMRSync(self, self.PAGE_NO))
        self.wait(0.4)
        for sc in (self.scene_a, self.scene_b, self.scene_c, self.scene_d, self.scene_e):
            self.next_scene(audio, sc(audio))
        audio.finish()
