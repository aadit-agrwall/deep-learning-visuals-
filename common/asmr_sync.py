"""Record ASMR cues from actual Manim time, without changing scene helpers."""

from contextlib import contextmanager
import json
from pathlib import Path


class ASMRSync:
    def __init__(self, scene, page_no):
        self.scene = scene
        self.page_no = str(page_no)
        self.events = []

    @contextmanager
    def cue(self, kind, pan=0.0, **details):
        start = float(self.scene.time)
        yield
        duration = float(self.scene.time) - start
        if duration > 0:
            self.events.append(dict(kind=kind, start=start, duration=duration,
                                    pan=pan, **details))

    def finish(self):
        path = Path(f"assets/audio/raw/page_{self.page_no}_asmr_timeline.json")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(dict(page=self.page_no,
                                       duration=float(self.scene.time),
                                       events=self.events), indent=2) + "\n")

