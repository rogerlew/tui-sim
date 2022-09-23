from __future__ import annotations

from typing import Iterable

from rich.styled import Styled
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich import box
from rich.console import RenderableType, ConsoleRenderable

from textual.app import App, ComposeResult
from textual.widgets import Static
from textual.widget import Widget


class AlarmTile(Widget):

    DEFAULT_CSS = """
    AlarmTile {
        height: auto;
        margin: 1 1;
    }
    """

    ALARM_WARNING_COLOR = 'wheat1'
    ALARM_TIME_NORMAL = 'white on grey23'
    ALARM_TILE_WARNING = f'{ALARM_WARNING_COLOR} on dark_goldenrod blink2'
    ALARM_CRITICAL_COLOR = 'deep_pink2'
    ALARM_TILE_CRITICAL = f'{ALARM_CRITICAL_COLOR} on magenta blink2'

    def __init__(
        self,
        label: str = "",
        alarm_state: int = 0,
        height: int = 4,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes)
        self.height = height
        self.label = label
        self.alarm_state = alarm_state

    def render(self) -> RenderableType:
        """Get a rich renderable for the widget's content.

        Returns:
            RenderableType: A rich renderable.
        """
        alarm_style = (AlarmTile.ALARM_TIME_NORMAL,
                       AlarmTile.ALARM_TILE_WARNING,
                       AlarmTile.ALARM_TILE_CRITICAL)[self.alarm_state]
        return Panel(Text(self.label, justify='center'),
                     box=box.SQUARE,  height=self.height, style=alarm_style)

    def update(self, alarm_state: str):
        self.alarm_state = alarm_state
        self.refresh(layout=True)
