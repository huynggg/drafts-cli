from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import Label, Button
from textual.screen import ModalScreen

from drafts_cli.messages import ConfirmationMessage


# Confirmation widget
class ConfirmationModal(ModalScreen):
    BINDINGS = [
        Binding("y", "yes", "Yes", show=False),
        Binding("n", "no", "No", show=False),
    ]

    def __init__(self, action: str, message: str) -> None:
        super().__init__()
        self.action = action
        self.message = message

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Label(self.message)
            with Horizontal():
                yield Button("[u]N[/u]o", id="no")
                yield Button("[u]Y[/u]es", id="yes", variant="error")

    def action_no(self) -> None:
        self.post_message(ConfirmationMessage(action=self.action, confirmation=False))
        self.dismiss()

    def action_yes(self) -> None:
        self.app.post_message(ConfirmationMessage(action=self.action, confirmation=True))

    @on(Button.Pressed, "#yes")
    def confirmed_button(self, event: Button.Pressed) -> None:
        self.app.post_message(ConfirmationMessage(action=self.action, confirmation=True))
        # self.dismiss()

    @on(Button.Pressed, "#no")
    def cancel_button(self, event: Button.Pressed) -> None:
        self.post_message(ConfirmationMessage(action=self.action, confirmation=False))
        self.dismiss()
