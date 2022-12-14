from __future__ import annotations

import sys
from functools import partial
from typing import cast, Iterable

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal  # pragma: no cover

import rich.repr
from rich.console import RenderableType
from rich.text import Text, TextType

from textual import events
from textual.css._error_tools import friendly_list
from textual.message import Message
from textual.reactive import Reactive
from textual.widgets import Static

ButtonVariant = Literal["default", "primary", "success", "warning", "error"]
_VALID_BUTTON_VARIANTS = {"default", "primary", "success", "warning", "error"}


class InvalidButtonVariant(Exception):
    pass


class Button(Static, can_focus=True):
    """A simple clickable button."""

    DEFAULT_CSS = """
    Button {
        width: auto;
        min-width: 16;
        height: 3;
        background: $panel;
        color: $text;      
        border: none;        
        border-top: tall $panel-lighten-2;
        border-bottom: tall $panel-darken-3;
        content-align: center middle;        
        text-style: bold;      
    }

    Button.-disabled {
        opacity: 0.4;
        text-opacity: 0.7;
    }

    Button:focus { 
    }

    Button:hover {
    }
    
    Button.-selected {
        background: $panel;
        border-bottom: tall $panel-lighten-2;
        border-top: tall $panel-darken-2;                
        tint: $background 30%;
    }

    Button.-active {
        border-top: tall $panel-lighten-1;
        background: $panel-darken-2;
        color: $text;
    }

    /* Primary variant */
    Button.-primary {
        background: $primary;
        color: $text;
        border-top: tall $primary-lighten-3;
        border-bottom: tall $primary-darken-3;

    }

    Button.-primary:hover {
        background: $primary-darken-2;
        color: $text;
        border-top: tall $primary-lighten-2;
    }

    Button.-primary.-active {
        background: $primary;
        border-bottom: tall $primary-lighten-3;
        border-top: tall $primary-darken-3;
    }


    /* Success variant */
    Button.-success {
        background: $success;
        color: $text;
        border-top: tall $success-lighten-2;
        border-bottom: tall $success-darken-3;
    }

    Button.-success:hover {
        background: $success-darken-2;
        color: $text;
    }

    Button.-success.-active {
        background: $success;
        border-bottom: tall $success-lighten-2;
        border-top: tall $success-darken-2;
    }


    /* Warning variant */
    Button.-warning {
        background: $warning;
        color: $text;
        border-top: tall $warning-lighten-2;
        border-bottom: tall $warning-darken-3;
    }

    Button.-warning:hover {
        background: $warning-darken-2;
        color: $text;

    }

    Button.-warning.-active {
        background: $warning;
        border-bottom: tall $warning-lighten-2;
        border-top: tall $warning-darken-2;
    }


    /* Error variant */
    Button.-error {
        background: $error;
        color: $text;
        border-top: tall $error-lighten-2;
        border-bottom: tall $error-darken-3;

    }

    Button.-error:hover {
        background: $error-darken-1;
        color: $text;

    }

    Button.-error.-active {
        background: $error;
        border-bottom: tall $error-lighten-2;
        border-top: tall $error-darken-2;
    }

    """

    ACTIVE_EFFECT_DURATION = 0.3
    """When buttons are clicked they get the `-active` class for this duration (in seconds)"""

    class Pressed(Message, bubble=True):
        @property
        def button(self) -> Button:
            return cast(Button, self.sender)

    def __init__(
            self,
            label: TextType | None = None,
            disabled: bool = False,
            selected: bool = False,
            variant: ButtonVariant = "default",
            attr: str | None = None,
            *,
            name: str | None = None,
            id: str | None = None,
            classes: str | None = None,
    ):
        """Create a Button widget.

        Args:
            label (str): The text that appears within the button.
            disabled (bool): Whether the button is disabled or not.
            variant (ButtonVariant): The variant of the button.
            name: The name of the button.
            id: The ID of the button in the DOM.
            classes: The CSS classes of the button.
        """
        super().__init__(name=name, id=id, classes=classes)

        if label is None:
            label = self.css_identifier_styled

        self.label = label
        self.attr = attr

        self.disabled = disabled
        if disabled:
            self.add_class("-disabled")

        self.selected = selected
        if selected:
            self.add_class("-selected")

        self.variant = variant

    label: Reactive[RenderableType] = Reactive("")
    variant = Reactive.init("default")
    disabled = Reactive(False)
    selected = Reactive(False)

    def __rich_repr__(self) -> rich.repr.Result:
        yield from super().__rich_repr__()
        yield "variant", self.variant, "default"
        yield "disabled", self.disabled, False
        yield "selected", self.selected, False

    def watch_mouse_over(self, value: bool) -> None:
        """Update from CSS if mouse over state changes."""
        if not self.disabled:
            self.app.update_styles(self)

    def validate_variant(self, variant: str) -> str:
        if variant not in _VALID_BUTTON_VARIANTS:
            raise InvalidButtonVariant(
                f"Valid button variants are {friendly_list(_VALID_BUTTON_VARIANTS)}"
            )
        return variant

    def watch_variant(self, old_variant: str, variant: str):
        self.remove_class(f"_{old_variant}")
        self.add_class(f"-{variant}")

    def watch_disabled(self, disabled: bool) -> None:
        self.set_class(disabled, "-disabled")
        self.can_focus = not disabled

    def watch_selected(self, selected: bool) -> None:
        self.set_class(selected, "-selected")

    def validate_label(self, label: RenderableType) -> RenderableType:
        """Parse markup for self.label"""
        if isinstance(label, str):
            return Text.from_markup(label)
        return label

    def render(self) -> RenderableType:
        try:
            label = self.label.copy()
        except AttributeError:
            label = self.label 
        label = Text.assemble(" ", label, " ")
        label.stylize(self.text_style)
        return label

    async def _on_click(self, event: events.Click) -> None:
        event.stop()
        self.press()

    def press(self) -> None:
        """Respond to a button press."""
        if self.disabled or not self.display:
            return
        # Manage the "active" effect:
        self._start_active_affect()
        # ...and let other components know that we've just been clicked:
        self.emit_no_wait(Button.Pressed(self))

    def _start_active_affect(self) -> None:
        """Start a small animation to show the button was clicked."""
        self.add_class("-active")
        self.set_timer(
            self.ACTIVE_EFFECT_DURATION, partial(self.remove_class, "-active")
        )

    async def _on_key(self, event: events.Key) -> None:
        if event.key == "enter" and not self.disabled:
            self._start_active_affect()
            await self.emit(Button.Pressed(self))

    def get_pseudo_classes(self) -> Iterable[str]:
        """Pseudo classes for a widget.

        Returns:
            Iterable[str]: Names of the pseudo classes.

        """
        if self.selected:
            yield 'selected'

        for cls in super().get_pseudo_classes():
            if cls == 'hover' and self.disabled:
                continue
            yield cls

    @classmethod
    def success(
            cls,
            label: TextType | None = None,
            disabled: bool = False,
            *,
            name: str | None = None,
            id: str | None = None,
            classes: str | None = None,
    ) -> Button:
        """Utility constructor for creating a success Button variant.

        Args:
            label (str): The text that appears within the button.
            disabled (bool): Whether the button is disabled or not.
            name: The name of the button.
            id: The ID of the button in the DOM.
            classes: The CSS classes of the button.

        Returns:
            Button: A Button widget of the 'success' variant.
        """
        return Button(
            label=label,
            disabled=disabled,
            variant="success",
            name=name,
            id=id,
            classes=classes,
        )

    @classmethod
    def warning(
            cls,
            label: TextType | None = None,
            disabled: bool = False,
            *,
            name: str | None = None,
            id: str | None = None,
            classes: str | None = None,
    ) -> Button:
        """Utility constructor for creating a warning Button variant.

        Args:
            label (str): The text that appears within the button.
            disabled (bool): Whether the button is disabled or not.
            name: The name of the button.
            id: The ID of the button in the DOM.
            classes: The CSS classes of the button.

        Returns:
            Button: A Button widget of the 'warning' variant.
        """
        return Button(
            label=label,
            disabled=disabled,
            variant="warning",
            name=name,
            id=id,
            classes=classes,
        )

    @classmethod
    def error(
            cls,
            label: TextType | None = None,
            disabled: bool = False,
            *,
            name: str | None = None,
            id: str | None = None,
            classes: str | None = None,
    ) -> Button:
        """Utility constructor for creating an error Button variant.

        Args:
            label (str): The text that appears within the button.
            disabled (bool): Whether the button is disabled or not.
            name: The name of the button.
            id: The ID of the button in the DOM.
            classes: The CSS classes of the button.

        Returns:
            Button: A Button widget of the 'error' variant.
        """
        return Button(
            label=label,
            disabled=disabled,
            variant="error",
            name=name,
            id=id,
            classes=classes,
        )
