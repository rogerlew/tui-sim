from __future__ import annotations

from typing import Iterable, List

from rich.styled import Styled
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich.table import Table
from rich import box
from rich.console import RenderableType, ConsoleRenderable

from textual.app import App, ComposeResult
from textual.widgets import Static
from textual.widget import Widget

from tui_sim.utils import clip, determine_alarm_state


class GroupIndicator(Widget):

    DEFAULT_CSS = """
    GroupIndicator {
        height: auto;
        margin: 1 1;
    }
    """

    BAR_INDICATOR_COLOR = 'purple4'
    INDICATOR_COLOR = 'turquoise2'
    ALARM_CRITICAL_COLOR = 'deep_pink2'
    ALARM_WARNING_COLOR = 'wheat1'

    def __init__(
        self,
        x: List[float] | None = None,
        label: str = "",
        units: str = "",
        ndigits: int = 0,
        lowlow: float | None = None,
        low: float | None = None,
        high: float | None = None,
        highhigh: float | None = None,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes)
        if x is None:
            x = []
        self.x = x
        self.units = units
        self.ndigits = ndigits
        self.lowlow = lowlow
        self.low = low
        self.high = high
        self.highhigh = highhigh
        self.label = label

    def render(self) -> RenderableType:
        """Get a rich renderable for the widget's content.

        Returns:
            RenderableType: A rich renderable.
        """
        lowlow, low, high, highhigh = self.lowlow, self.low, self.high, self.highhigh
        ndigits = self.ndigits
        tbl = Table.grid(expand=True)
        tbl.add_column(width=7)

        z = [Text(self.label, justify='left', style='b')]
        for v in self.x:
            alarm_state = determine_alarm_state(v, lowlow, low, high, highhigh)
            alarm_style = (GroupIndicator.BAR_INDICATOR_COLOR,
                           GroupIndicator.ALARM_WARNING_COLOR,
                           GroupIndicator.ALARM_CRITICAL_COLOR)[alarm_state]
            if alarm_state == 0:
                z.append(Text('  '))
            else:
                z.append(Text(' !', style=alarm_style))
            _v = round(v, ndigits)
            z.append(Text.from_markup(f'[{GroupIndicator.INDICATOR_COLOR}]{_v:>7}[/{GroupIndicator.INDICATOR_COLOR}] [i]{self.units}[/i]'))
            tbl.add_column(width=2)
            tbl.add_column(width=12)

        z.append(Text(' ' * 99, overflow='crop'))
        tbl.add_column()
        tbl.add_row(*z)

        return tbl

    def update(self, x: List[float]):
        self.x = x
        self.refresh(layout=True)
