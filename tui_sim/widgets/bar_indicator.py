from __future__ import annotations

from rich.console import RenderableType

from textual.app import ComposeResult
from textual.widgets import Static
from textual.widget import Widget

from tui_sim.utils import clip, determine_alarm_state


class ProgressBar(Widget):

    DEFAULT_CSS = """
    ProgressBar {
        height: auto;
    }
    """

    BAR_INDICATOR_COLOR = 'purple4'
    INDICATOR_COLOR = 'turquoise2'
    ALARM_CRITICAL_COLOR = 'deep_pink2'
    ALARM_WARNING_COLOR = 'wheat1'

    def __init__(
            self,
            total: float,
            completed: float,
            *,
            alarm_state : int = 0,
            name: str | None = None,
            id: str | None = None,
            classes: str | None = None,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes)
        self.total = total
        self.completed = completed
        self.alarm_state = alarm_state

    def render(self) -> RenderableType:
        completed = self.completed
        total = self.total
        color = (ProgressBar.BAR_INDICATOR_COLOR,
                 ProgressBar.ALARM_WARNING_COLOR,
                 ProgressBar.ALARM_CRITICAL_COLOR)[self.alarm_state]

        _bar_ = "━"
        _bar = "╸"
        bar_ = "╺"

        width, height = self.container_size
        pct = completed / total
        halves = int(clip(round(width * pct * 2), 0, width * 2))
        filled = _bar_ * (halves//2)
        if halves % 2:
            filled += _bar
            empty = _bar_
        else:
            empty = bar_
        empty += _bar_ * (width - len(filled) - 1)
        return f'[{color}]{filled}[/{color}][grey27]{empty}[/grey27]'

    def update(self, completed, alarm_state):
        self.completed = completed
        self.alarm_state = alarm_state
        self.refresh(layout=True)


class BarIndicator(Widget):

    DEFAULT_CSS = """
    BarIndicator {
        layout: grid;
        grid-size: 4;
        grid-columns: 2fr 1fr 1fr 4fr;
        background: $panel;
        height: 1;
        width: 100%;
        margin: 0;
        padding: 0;
    }
    
    BarIndicator > .label {
        text-style: bold;
    }
    
    BarIndicator > .indicator {
        content-align: right middle;
        color: rgb(0,215,255);
    }
    
    BarIndicator > .units {
        text-style: italic;
    }
    """

    def __init__(self, name: str, value: float, units='', ndigits=2,
                 xmin=None, xmax=None,
                 lowlow=None, low=None, high=None, highhigh=None,
                 classes=''):

        self._classes = classes
        self.value = round(value, ndigits)
        self.units = units
        self.ndigits = ndigits
        self.xmin = xmin
        self.xmax = xmax
        self.low = low
        self.high = high
        self.lowlow = lowlow
        self.highhigh = highhigh
        self.widgets = []

        super().__init__(name=name)

    def compose(self) -> ComposeResult:
        value = self.value
        xmin, xmax = self.xmin, self.xmax
        alarm_state = determine_alarm_state(value, self.lowlow, self.low, self.high, self.highhigh)

        self.widgets.append(Static(str(self.name), classes='label'))
        yield self.widgets[-1]

        self.widgets.append(Static(f'{self.value} ', classes='indicator'))
        yield self.widgets[-1]

        self.widgets.append(Static(f' {self.units}', classes='units'))
        yield self.widgets[-1]

        if xmin is not None and xmax is not None:
            pct = clip((value - xmin) / (xmax - xmin), 0.0, 1.0)
            self.widgets.append(ProgressBar(total=1, completed=pct, alarm_state=alarm_state))
            yield self.widgets[-1]

    def update(self, value):
        self.value = round(value, self.ndigits)
        xmin, xmax = self.xmin, self.xmax
        alarm_state = determine_alarm_state(value, self.lowlow, self.low, self.high, self.highhigh)

        self.widgets[1].update(f'{self.value}')
        if xmin is not None and xmax is not None:
            pct = clip((value - xmin) / (xmax - xmin), 0.0, 1.0)
            self.widgets[3].update(completed=pct, alarm_state=alarm_state)
