from textual.widgets import Static, Label
from textual.app import ComposeResult
from drafts_cli.utilities import format_timestamp


class DraftItem(Static):
    def __init__(self, id: int, content: str = "", modified: str = "") -> None:
        super().__init__()
        self.content_text = content
        self.modified = format_timestamp(modified)
        self.id = id

    def compose(self) -> ComposeResult:
        yield Label(f'[b]{self.content_text[0:20]}[/b]')
        yield Label(self.content_text[10:40])
        yield Label(self.modified)
