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
        grid-columns: 2fr 1fr 1fr 4fr;
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

    def __init__(self,
                 name: str | None = None,
                 value: str | float | bool | None = '',
                 units: str = '',
                 ndigits: int = 0,
                 attr: str | None = None,
                 *,
                 id: str | None = None,
                 classes: str | None = None,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes)

        self.units = units
        self.ndigits = ndigits
        self._update(value)
        self._value_widget = Static(f'{self.value} ', classes='indicator')
        self._units_widget = Static(f' {self.units}', classes='units')
        self.attr = attr

    def compose(self) -> ComposeResult:
        yield Static(str(self.name), classes='label')

        yield self._value_widget

        yield self._units_widget

    def _update(self, value):
        ndigits = self.ndigits
        if isfloat(value) and ndigits is not None:
            self.value = round(value, ndigits)
        else:
            self.value = value

    def update(self, value):
        self._update(value)
        self._value_widget.update(f'{self.value}')
