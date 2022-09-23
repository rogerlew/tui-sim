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


class ValveGroupIndicator(Widget):

    DEFAULT_CSS = """
    ValveGroupIndicator {
        height: auto;
        margin: 1 1;
    }
    """

    INDICATOR_COLOR = 'turquoise2'
    VALVE = '\u25B6\u25C0'
    VALVE_0 = 'bright_green'
    VALVE_1 = 'bright_red'

    def __init__(
        self,
        x: List[float] | None = None,
        label: str = "",
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes)
        if x is None:
            x = []
        self.x = x
        self.label = label

    def render(self) -> RenderableType:
        """Get a rich renderable for the widget's content.

        Returns:
            RenderableType: A rich renderable.
        """
        x = self.x

        tbl = Table.grid(expand=True)
        tbl.add_column(width=7)

        z = [Text(self.label, justify='left', style='b')]
        for v in x:
            z.append(Text('       \u25B6\u25C0     ',
                          style=(ValveGroupIndicator.VALVE_0, ValveGroupIndicator.VALVE_1)[v > 0.1]))
            tbl.add_column(width=14)

        z.append(Text(' ' * 99, overflow='crop'))
        tbl.add_column()
        tbl.add_row(*z)

        z = [Text('    ')]
        for v in x:
            z.append(Text.from_markup(f'      [{ValveGroupIndicator.INDICATOR_COLOR}]{round(v * 100):>3}[/{ValveGroupIndicator.INDICATOR_COLOR}] [i]%    [/i]'))

        z.append(Text(' ' * 99, overflow='crop'))
        tbl.add_row(*z)

        return tbl

    def update(self, x: List[float]):
        self.x = x
        self.refresh(layout=True)
