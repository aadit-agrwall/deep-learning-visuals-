"""Mixin: logs animation timings for music sync.
Writes assets/audio/raw/page_<PAGE_NO>_events.json while rendering."""
import json
import os


class SyncLogMixin:
    PLAY_MIN = 0.3          # log play() calls at least this long (motion sounds)

    def _now(self):
        try:
            return float(self.renderer.time)
        except Exception:
            return float(self.time)

    def _log(self, kind, t0, t1, n=0):
        ev = getattr(self, "_events", None)
        if ev is None:
            ev = self._events = []
        ev.append({"kind": kind, "t0": t0, "t1": t1, "n": n})
        os.makedirs("assets/audio/raw", exist_ok=True)
        path = "assets/audio/raw/page_%s_events.json" % self.PAGE_NO
        with open(path, "w") as f:
            json.dump(ev, f)

    def _enter(self):
        self._sync_depth = getattr(self, "_sync_depth", 0) + 1

    def _leave(self):
        self._sync_depth -= 1

    def play(self, *args, **kwargs):
        if getattr(self, "_sync_depth", 0) > 0:
            return super().play(*args, **kwargs)
        t0 = self._now()
        r = super().play(*args, **kwargs)
        t1 = self._now()
        if t1 - t0 >= self.PLAY_MIN:
            self._log("play", t0, t1)
        return r

    def type_in(self, *args, **kwargs):
        t0 = self._now()
        self._enter()
        try:
            r = super().type_in(*args, **kwargs)
        finally:
            self._leave()
        mob = args[0] if args else None
        try:
            n = len(mob.submobjects)
        except Exception:
            n = 0
        self._log("type", t0, self._now(), n)
        return r

    def dust_wipe(self, *args, **kwargs):
        t0 = self._now()
        self._enter()
        try:
            r = super().dust_wipe(*args, **kwargs)
        finally:
            self._leave()
        self._log("wipe", t0, self._now())
        return r

    def zoom_pulse(self, *args, **kwargs):
        t0 = self._now()
        self._enter()
        try:
            r = super().zoom_pulse(*args, **kwargs)
        finally:
            self._leave()
        self._log("pulse", t0, self._now())
        return r

    def _fit(self, mob, w):
        if mob.width > w:
            self.fit_width(mob, w)
