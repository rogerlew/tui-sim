import asyncio
import aiohttp
from rich.panel import Panel
from rich.text import Text
from textual.app import App
from textual.layouts.grid import GridLayout
from textual.widgets import Placeholder
from textual.widget import Widget


class CustomText(Widget):
    def __init__(
        self, name: str, text: str, title: str = "", subtitle: str = ""
    ) -> None:
        super().__init__(name)
        self.text = text
        self.title = title
        self.subtitle = subtitle

    def render(self) -> Panel:
        text_widget = Text(self.text)
        panel = Panel(text_widget, title=self.title, subtitle=self.subtitle)
        return panel


class DashboardController(App):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.dashboard = None
        self.main = None

    async def on_load(self) -> None:
        self.bind("q", "quit", description="Quit")
        self.bind("enter", "submit", description="Submit")
        self.bind("escape", "reset_focus", show=False)
        self.bind("ctrl+i", "next_tab_index", show=False)
        self.bind("shift+tab", "previous_tab_index", show=False)

    async def on_mount(self):
        self.dashboard = layout_template(grid)
        future = asyncio.ensure_future(main(self))

    async def add_text(
        self, text: str, title: str = "", subtitle: str = "", area="area1"
    ):
        if self.dashboard:
            custom = CustomText("custom_text", text, title, subtitle)
            args = {area: custom}
            self.dashboard.place(**args)
            return custom


async def main(dashboard_controller: DashboardController):
    await dashboard_controller.add_text(
        "Shows automatically before executing aiohttp. Please hover your mouse over the Dashboard",
        area="area1",
    )
    async with aiohttp.ClientSession() as session:
        # Creating a session is fine as it doesn't block Dashboard from updating, but making a request does.
        async with session.get("http://python.org") as response:
            pass
        pass
    await dashboard_controller.add_text(
        "Does not show automatically after executing aiohttp function, text only shows after interacting with the Dashboard",
        area="area2",
    )

if __name__ == "__main__":
    DashboardController().run()