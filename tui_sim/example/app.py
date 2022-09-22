from __future__ import annotations

from time import time

from textual import layout
from textual.app import App, ComposeResult
from textual.widgets import Header, Button
from textual.widget import Widget

import sys
sys.path.append('../../')

from tui_sim.widgets.bar_indicator import BarIndicator
from tui_sim.widgets.static_footer import StaticFooter

from model import Model


class TuiSim(Widget):
    def __init__(self, num_phasors) -> None:
        model = Model(num_phasors)

        phasor_indicators = []
        for i, v in enumerate(model.values):
            phasor_indicators.append(
                BarIndicator(f'Phasor {i}', v, xmin=-10, xmax=10)
            )
        self.model = model
        self.phasor_indicators = phasor_indicators
        self.status = StaticFooter('Model Initialized')

        super().__init__()

    def compose(self) -> ComposeResult:
        yield self.status

        yield layout.Vertical(
            *self.phasor_indicators,
            layout.Horizontal(
                Button('Pause', id='pause'),
                Button('Play', id='play'),
            ),
            classes='panel'
        )

    def step(self) -> None:
        model = self.model
        model.step()
        values = model.values
        for v, p_ind in zip(values, self.phasor_indicators):
            p_ind.update_value(v)

        self.update_status()

    def is_running(self) -> bool:
        return self.update_timer._active._value

    def update_status(self) -> None:
        self.status.update(f'[{self.model.k}] {"Running" if self.is_running else "Paused"}')

    def on_mount(self) -> None:
        self.t0 = time()
        self.update_timer = self.set_interval(1/100.0, self.step)
        self.update_timer.pause()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'pause':
            self.update_timer.pause()
        if event.button.id == 'play':
            self.update_timer.resume()

        self.update_status()


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
