class LowPassFilter:
    """Simple exponential smoothing filter for scalar values."""

    def __init__(self, alpha: float = 0.2, initial=None):
        self.alpha = max(0.0, min(1.0, alpha))
        self.value = initial

    def update(self, x):
        if self.value is None:
            self.value = x
        else:
            self.value = self.alpha * x + (1.0 - self.alpha) * self.value
        return self.value