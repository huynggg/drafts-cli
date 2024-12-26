from textual.widgets import Static, Label
from textual.app import ComposeResult


class DraftItem(Static):
    def __init__(self, id: int, content: str = "", footer: str = "") -> None:
        super().__init__()
        self.content_text = content
        self.footer = footer
        self.id = id

    def compose(self) -> ComposeResult:
        yield Label(self.content_text[0:20])
        yield Label(self.content_text[10:40])
        yield Label(self.footer)
