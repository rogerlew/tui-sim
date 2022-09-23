from __future__ import annotations

from time import time

from textual import layout
from textual.app import App, ComposeResult
from textual.widgets import Header, Button, Static
from textual.widget import Widget

import sys
sys.path.append('../../../')

from tui_sim.widgets import AlarmTile, StaticFooter, SimpleIndicator, BarIndicator, GroupIndicator


from model import RandomModel


class TuiSim(Widget):

    DEFAULT_CSS = """
    TuiSim {
    }
    """

    def __init__(self, num_phasors) -> None:
        self.model = RandomModel()

        self.status = StaticFooter('Model Initialized')

        super().__init__()

    def compose(self) -> ComposeResult:
        self.indicator = GroupIndicator(self.model.x, label='Values', units='furlongs', lowlow=8, low=16, high=111, highhigh=119)
        yield self.indicator
        yield self.status

    def step(self) -> None:
        self.indicator.update(self.model.x)
        self.update_status()

    def is_running(self) -> bool:
        return self.update_timer._active._value

    def update_status(self) -> None:
        self.status.update(f'[{self.model.k}]')

    def on_mount(self) -> None:
        self.t0 = time()
        self.update_timer = self.set_interval(1/30.0, self.step)


class TuiSimApp(App):
    def __init__(self, num_phasors=5) -> None:
        self.tui_sim = TuiSim(num_phasors=num_phasors)
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header()
        yield self.tui_sim


if __name__ == "__main__":
    app = TuiSimApp()
    app.run()
