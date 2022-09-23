
from typing import List

from dataclasses import dataclass

import numpy as np
import math
import random

tau = math.pi * 2

@dataclass
class Phasor:
    amplitude: float = 1
    phase: float = 0
    frequency: float = 1

    def __call__(self, t):
        return np.sin(tau * t / self.frequency + self.phase) * self.amplitude


class Model:
    k: int = 0
    dt: float = 0.01
    phasors: List[Phasor] = []

    def __init__(self, num_phasors: int):
        for i in range(num_phasors):
            self.phasors.append(Phasor(random.uniform(1, 10),
                                             random.uniform(0.05, 10),
                                             random.uniform(0, tau)))

    @property
    def time(self) -> float:
        return self.k * self.dt

    def step(self) -> None:
        self.k += 1

    @property
    def values(self) -> List[float]:
        t = self.time
        values = [p(t) for p in self.phasors]
        values.append(np.mean(values))
        return values


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    phasor = Phasor(1, 0, 1)
    t = np.linspace(0, 10, 100)
    plt.plot(t, phasor(t))
    plt.show()
