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
        height: 4;
        margin: 1 1;
    }
    """

    ALARM_WARNING_COLOR = 'wheat1'
    ALARM_TIME_NORMAL = 'white on grey23'
    ALARM_TILE_WARNING = f'{ALARM_WARNING_COLOR} on dark_goldenrod blink2'
    ALARM_CRITICAL_COLOR = 'deep_pink2'
    ALARM_TILE_CRITICAL = f'{ALARM_CRITICAL_COLOR} on magenta blink2'
    ALARM_TILE_PERMISSIVE = f'dark_sea_green2 on yellow4'

    def __init__(
        self,
        label: str = "",
        alarm_state: int = 0,
        height: int = 4,
        attrs: Iterable[str] | None = None,
        permissive: bool = False,
        critical: bool = False,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        if id is None:
            id = '_'.join(label.lower().split())

        super().__init__(name=name, id=id, classes=classes)
        self.permissive = permissive
        self.critical = critical
        self.attrs = attrs
        self.height = height
        self.label = label
        self.alarm_state = alarm_state

    @property
    def alarm_style(self):
        if self.alarm_state == 0:
            return AlarmTile.ALARM_TIME_NORMAL

        if self.critical:
            return AlarmTile.ALARM_TILE_CRITICAL

        elif self.permissive:
            return AlarmTile.ALARM_TILE_PERMISSIVE

        return AlarmTile.ALARM_TILE_WARNING

    def render(self) -> RenderableType:
        """Get a rich renderable for the widget's content.

        Returns:
            RenderableType: A rich renderable.
        """
        return Panel(Text(self.label, justify='center'),
                     box=box.SQUARE,  height=self.height, style=self.alarm_style)

    def update(self, alarm_state: int):

        self.alarm_state = alarm_state
        self.refresh(layout=True)
