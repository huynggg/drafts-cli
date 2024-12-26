from textual.widgets import ListItem, Static, Label
from textual.containers import VerticalGroup
from textual.app import ComposeResult


class DraftItem(VerticalGroup):
    def __init__(self, content: str = "", footer: str = "") -> None:
        super().__init__()
        self.content_text = content
        self.footer = footer

    def compose(self) -> ComposeResult:
        yield Label(self.content_text[0:20])
        yield Static(self.content_text[10:40])
        yield Label(self.footer)
