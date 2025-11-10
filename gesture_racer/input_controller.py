import sys
from typing import Iterable


class InputController:
    def __init__(self, movement_keys: Iterable[str] = ("w", "a", "s", "d")):
        self.movement_keys = list(movement_keys)
        self.backend = None
        if sys.platform.startswith("win"):
            # Fallback to pynput even on Windows for simplicity; could add ctypes-based mode later.
            from pynput.keyboard import Controller
            self.backend = Controller()
        else:
            # macOS / Linux
            from pynput.keyboard import Controller
            self.backend = Controller()
        self._pressed = set()

    def press(self, key: str):
        try:
            self.backend.press(key)
        except Exception:
            # Ignore press errors (e.g., missing Accessibility permission)
            pass

    def release(self, key: str):
        try:
            self.backend.release(key)
        except Exception:
            pass

    def release_all(self):
        for k in list(self._pressed):
            self.release(k)
        self._pressed.clear()

    def apply_actions(self, move: str, turn: str):
        desired = set()
        # Movement
        if move == "forward":
            desired.add("w")
        elif move in ("brake", "reverse"):
            desired.add("s")
        # Turning
        if turn == "left":
            desired.add("a")
        elif turn == "right":
            desired.add("d")

        # Release keys that are no longer needed
        for k in list(self._pressed):
            if k not in desired:
                self.release(k)
                self._pressed.discard(k)

        # Press keys that are newly required
        for k in desired:
            if k not in self._pressed:
                self.press(k)
                self._pressed.add(k)