from __future__ import annotations

from rich.console import RenderableType

from textual.app import App, ComposeResult
from textual.widgets import Static
from textual.widget import Widget

from tui_sim.utils import isfloat


class SimpleIndicator(Widget):
    DEFAULT_CSS = """
    SimpleIndicator {
        layout: grid;
        grid-size: 4;
        grid-columns: 1fr 1fr;
        background: $panel;
        height: 1;
        width: 100%;
        margin: 0;
        padding: 0;
    }

    SimpleIndicator > .label {
        text-style: bold;
    }

    SimpleIndicator > .indicator {
        content-align: right middle;
        color: rgb(0,215,255);
    }

    SimpleIndicator > .units {
        text-style: italic;
    }
    """

    def __init__(self,  value: float, units='', ndigits=0, classes=''):

        self._classes = classes
        self.value = round(value, ndigits)
        self.units = units
        self.ndigits = ndigits
        self.widgets = []

        super().__init__()

    def compose(self) -> ComposeResult:

        self.widgets.append(Static(f'{self.value} ', classes='indicator'))
        yield self.widgets[-1]

        self.widgets.append(Static(f' {self.units}', classes='units'))
        yield self.widgets[-1]

    def update(self, value):
        ndigits = self.ndigits
        if isfloat(value) and ndigits is not None:
            self.value = round(value, ndigits)
        else:
            self.value = value

        self.widgets[0].update(f'{self.value}')
