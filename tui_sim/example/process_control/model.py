
import random

from tui_sim.utils import clip


class ProcessControlModel:
    def __init__(self):
        self.k = 0

        self.alarm_low_a = ''
        self.alarm_high_a = ''
        self.alarm_low_b = ''
        self.alarm_high_b = ''

        self.a = 0
        self.b = 0

        self.a_vel = 0
        self.b_vel = 0

        self.score = 0

    @property
    def no_alarms_active(self):
        return not self.alarm_low_a and \
               not self.alarm_low_b and \
               not self.alarm_high_a and \
               not self.alarm_high_b

    def step(self):
        self.a_vel = clip(self.a_vel + random.normalvariate(0, 0.5), -5, 5)
        self.b_vel = clip(random.normalvariate(0, 0.5), -5, 5)

        self.a += self.a_vel
        self.b += self.b_vel

        self.alarm_low_a = self.a < -100
        self.alarm_high_a = self.a > 100

        self.alarm_low_b = self.b < -100
        self.alarm_high_b = self.b > 100

        if self.no_alarms_active:
            self.score += abs(self.a) + abs(self.b)

        self.k += 1
