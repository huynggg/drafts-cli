# from rich.syntax import Syntax
# from rich.traceback import Traceback
from textual.app import App, ComposeResult
from textual.containers import VerticalGroup, Horizontal
# from textual.reactive import var
from textual.widgets import Footer, Header, Input, ListView, ListItem, Label, TextArea


class NavBar(VerticalGroup):
    """The left bar containing the draft list and a search bar"""

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Search", type="text", id="search")
        with ListView():
            yield ListItem(Label("One"))
            yield ListItem(Label("Two"))
            yield ListItem(Label("Three"))


class DraftsEditor(App):
    """Text Editor in the command line"""

    CSS_PATH = "drafts.tcss"
    BINDINGS = [
        ("ctrl+q", "quit", "Quit"),
        ("ctrl+l", "search", "Search"),
    ]

    def compose(self) -> ComposeResult:
        """Compose the UI of the app"""
        with Horizontal():
            yield Header()
            yield NavBar()
            yield TextArea()
            yield Footer()

    def action_search(self):
        self.query_one("#search", Input).focus()


if __name__ == "__main__":
    app = DraftsEditor()
    app.run()
