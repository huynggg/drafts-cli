# from rich.syntax import Syntax
# from rich.traceback import Traceback
# from textual.reactive import var
import logging
from textual.reactive import reactive, var
from textual.logging import TextualHandler
from textual.app import App, ComposeResult
from textual.events import Key
from textual.containers import VerticalGroup, Horizontal
from textual.widgets import Footer, Header, Input, ListView, ListItem, Label, TextArea
from database import Draft, initialize_db
from helpers import extract_draft_id


# Configure logging
logging.basicConfig(
    level="NOTSET",
    handlers=[TextualHandler()],
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class DraftsList(ListView):
    def on_key(self, event: Key) -> None:
        if event.key == "j":
            self.action_cursor_down()
        elif event.key == "k":
            self.action_cursor_up()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        editor = self.app.query_one("#editor")
        selected_draft = event.item.query_one(Label)
        # Extract the id
        extracted_id = extract_draft_id(selected_draft.id)
        # Update the editor's opened draft id
        editor.draft_id = extracted_id
        # Get the content from the db
        draft = Draft.get_by_id(extracted_id)
        # Update the content of the text area
        editor.focus()
        editor.text = draft.content


class SideBar(VerticalGroup):
    """The left bar containing the draft list and a search bar"""

    def compose(self) -> ComposeResult:
        search_bar = Input(placeholder="Search", type="text", id="search")
        search_bar.can_focus = False
        yield search_bar
        # yield Input(placeholder="Search", type="text", id="search")
        with DraftsList():
            drafts_list = Draft.select()
            for draft in drafts_list:
                truncated_content = draft.content[0:20] + "..."
                yield ListItem(Label(truncated_content.strip(), id=f'draft-{draft.id}'))


class Editor(TextArea):
    # content = var("")
    draft_id = var(-1)


class DraftsApp(App):
    """Text Editor in the command line"""

    CSS_PATH = "drafts.tcss"
    BINDINGS = [
        ("ctrl+q", "quit", "Quit"),
        ("ctrl+l", "search", "Search"),
        ("ctrl+s", "save", "Save"),
    ]

    def compose(self) -> ComposeResult:
        """Compose the UI of the app"""
        yield Header()
        with Horizontal():
            yield SideBar()
            yield Editor.code_editor(id="editor", language="markdown")
        yield Footer()

    def action_search(self) -> None:
        search_bar = self.query_one("#search", Input)
        search_bar.can_focus = True
        search_bar.focus()

    def action_save(self) -> None:
        editor = self.query_one("#editor", Editor)
        # Create a new draft if none selected
        if editor.draft_id == -1:
            Draft.create(content=editor.text)
        else:
            # If there is draft selected, save to that draft instead
            selected_draft = Draft.get_by_id(editor.draft_id)
            selected_draft.content = editor.text
            selected_draft.save()

    def on_key(self, event: Key):
        if event.key == "tab" or event.key == "shift+tab":
            self.query_one("#search", Input).can_focus = False

    def on_mount(self) -> None:
        # Focus on the search on start
        self.query_one("#editor", TextArea).focus()


if __name__ == "__main__":
    # Initialize db on start
    initialize_db()
    app = DraftsApp()
    app.run()
