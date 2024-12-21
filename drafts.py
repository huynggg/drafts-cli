# from rich.syntax import Syntax
# from rich.traceback import Traceback
# from textual.reactive import var
from textual import on
from textual.app import App, ComposeResult
from textual.events import Key
from textual.containers import VerticalGroup, Horizontal
from textual.widgets import Footer, Header, Input, ListView, ListItem, Label, TextArea


class DraftsList(ListView):
    def on_key(self, event: Key) -> None:
        if event.key == "j":
            self.action_cursor_down()
        elif event.key == "k":
            self.action_cursor_up()

    @on(ListView.Selected)
    def handle_list_view_selected(self, event: ListView.Selected) -> None:
        editor = self.app.query_one("#editor")
        # Get the id of the text
        draft_id = event.item.query_one(Label).id
        # Update the content of the text area
        editor.text = f'Selected draft {draft_id}'
        editor.focus()
        # editor.text += "\n"
        editor.scroll_right()
        editor.refresh()


class SideBar(VerticalGroup):
    """The left bar containing the draft list and a search bar"""

    def compose(self) -> ComposeResult:
        # search_bar = Input(placeholder="Search", type="text", id="search")
        # search_bar.can_focus = False
        yield Input(placeholder="Search", type="text", id="search")
        with DraftsList():
            yield ListItem(Label("Test\nTest\nTest", id="item-1"))
            yield ListItem(Label("Two", id="item-2"))
            yield ListItem(Label("Three", id="item-3"))


class DraftsApp(App):
    """Text Editor in the command line"""

    CSS_PATH = "drafts.tcss"
    BINDINGS = [
        ("ctrl+q", "quit", "Quit"),
        ("ctrl+l, cmd+l", "search", "Search"),
    ]

    def compose(self) -> ComposeResult:
        """Compose the UI of the app"""
        yield Header()
        with Horizontal():
            yield SideBar()
            yield TextArea.code_editor(id="editor")
        yield Footer()

    def action_search(self):
        search_bar = self.query_one("#search", Input).focus()
        search_bar.can_focus = True
        search_bar.focus()

    def on_key(self, event: Key):
        if event.key == "tab":
            self.query_one("#search", Input).can_focus = False

    def on_mount(self) -> None:
        # Focus on the search on start
        self.query_one("#search", Input).focus()


if __name__ == "__main__":
    app = DraftsApp()
    app.run()
