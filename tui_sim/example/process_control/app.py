from __future__ import annotations

from time import time

from textual import layout
from textual.app import App, ComposeResult
from textual.widgets import Header, Button, Static
from textual.widget import Widget

import sys
sys.path.append('../../../')

from tui_sim.widgets import AlarmTile, StaticFooter, SimpleIndicator, BarIndicator

from model import ProcessControlModel


class TuiSim(Widget):

    DEFAULT_CSS = """
    TuiSim {
        layout: grid;
        grid-size: 2;
    }
    """

    def __init__(self, num_phasors) -> None:
        self.model = ProcessControlModel()

        self.status = StaticFooter('Model Initialized')

        super().__init__()

    def compose(self) -> ComposeResult:
        yield self.status

        yield layout.Vertical(
            AlarmTile('A LOW (WITH A VERY VERY LONG TITLE)', 0, id='a_low'),
            AlarmTile('A HIGH', 0, id='a_high'),
            BarIndicator('', self.model.a, units='V', xmin=-100, xmax=100, low=-100, high=100, id='a'),
            SimpleIndicator(self.model.a_vel, 'V/s', id='a_vel'),
            Button('flip', id='flip_a'),
            classes='panel'
        )

        yield layout.Vertical(
            AlarmTile('B LOW', 0, id='b_low'),
            AlarmTile('B HIGH', 0, id='b_high'),
            BarIndicator('', self.model.a, units='V', xmin=-100, xmax=100, low=-100, high=100, id='b'),
            SimpleIndicator(self.model.a_vel, 'V/s', id='b_vel'),
            Button('flip', id='flip_b'),
            classes='panel'
        )

    def step(self) -> None:
        model = self.model
        model.step()

        self.query_one('#a').update(model.a)
        self.query_one('#a_vel').update(model.a_vel)

        self.query_one('#b').update(model.b)
        self.query_one('#b_vel').update(model.b_vel)

        self.query_one('#a_low').update(model.alarm_low_a)
        self.query_one('#a_high').update(model.alarm_high_a)

        self.query_one('#b_low').update(model.alarm_low_b)
        self.query_one('#b_high').update(model.alarm_high_b)

        self.update_status()

    def is_running(self) -> bool:
        return self.update_timer._active._value

    def update_status(self) -> None:
        self.status.update(f'[{self.model.k}] Score: {round(self.model.score)}')

    def on_mount(self) -> None:
        self.t0 = time()
        self.update_timer = self.set_interval(1/30.0, self.step)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'flip_a':
            self.model.a_vel *= -1
        if event.button.id == 'flip_b':
            self.model.b_vel *= -1


class TuiSimApp(App):
    def __init__(self, num_phasors=5) -> None:
        self.tui_sim = TuiSim(num_phasors=num_phasors)
        super().__init__(css_path='stylesheet.css')

    def compose(self) -> ComposeResult:
        yield Header()
        yield self.tui_sim


if __name__ == "__main__":
    app = TuiSimApp()
    app.run()
