# from rich.syntax import Syntax
# from rich.traceback import Traceback
# from textual.reactive import var
import logging
from textual import on
from textual.reactive import var
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
    BINDINGS = [
        ("ctrl+d", "delete", "Delete"),
        ("k", "cursor_up", "Up"),
        ("j", "cursor_down", "Down"),
    ]

    def on_mount(self) -> None:
        self.border_subtitle = "Drafts"

    def action_delete(self) -> None:
        try:
            # Highlighted child is ListItem, then query for Label to get the ID
            highlighted_item_id = extract_draft_id(self.highlighted_child.query_one(Label).id)
            hightlighted_note = Draft.get(Draft.id == highlighted_item_id)
            if hightlighted_note.delete_instance():
                # Remove the ListItem by index
                self.pop(self.index)
                # Check if the deleted draft is also being opened in the editor
                editor = self.app.query_one("#editor")
                if highlighted_item_id == editor.draft_id:
                    # Then clear the editor and update the current opened draft_id
                    editor.draft_id = None
                    editor.text = ""
        except AttributeError:
            logger.debug("No more item to delete")
            return

    @on(ListView.Selected)
    def on_list_view_selected(self, event: ListView.Selected) -> None:
        editor = self.app.query_one("#editor")
        selected_draft = event.item.query_one(Label)
        # Extract the id then update the editor's opened draft id variable
        editor.draft_id = extract_draft_id(selected_draft.id)
        # Get the content from the db
        draft = Draft.get_by_id(editor.draft_id)
        # Update the content of the text area
        editor.focus()
        editor.text = draft.content

    def refresh_draft_list(self, search_term: str = "") -> None:
        drafts_list = Draft.select().order_by(Draft.modified_at.desc())
        self.clear()
        for draft in drafts_list:
            if search_term in draft.content:
                truncated_content = draft.content[0:20] + "..."
                self.append(ListItem(Label(truncated_content.strip(), id=f'draft-{draft.id}')))


class SideBar(VerticalGroup):
    """The left bar containing the draft list and a search bar"""

    def compose(self) -> ComposeResult:
        search_bar = Input(placeholder="Search", type="text", id="search")
        search_bar.can_focus = False
        yield search_bar
        # yield Input(placeholder="Search", type="text", id="search")
        with DraftsList(id="draft-list"):
            drafts_list = Draft.select().order_by(Draft.modified_at.desc())
            for draft in drafts_list:
                truncated_content = draft.content[0:20] + "..."
                yield ListItem(Label(truncated_content.strip(), id=f'draft-{draft.id}'))

    @on(Input.Changed, "#search")
    def on_search_bar_change(self, search_term: Input.Changed) -> None:
        logger.debug(search_term.value)
        list_view = self.query_one(ListView)
        # Populate the list with new items
        list_view.refresh_draft_list(search_term.value)


class Editor(TextArea):
    draft_id = var(None)
    BINDINGS = [
        ("ctrl+q", "quit", "Quit"),
        ("ctrl+l", "search", "Search"),
        ("ctrl+n", "new", "New"),
        ("ctrl+s", "save", "Save"),
    ]

    def on_mount(self) -> None:
        self.border_subtitle = "Editor"

    def action_save(self) -> None:
        # Get current search term to keep the list filtered
        current_search_term = self.app.query_one("#search").value
        draft_list = self.app.query_one(DraftsList)
        # Create a new draft if none selected
        if self.draft_id is None:
            new_draft = Draft.create(content=self.text)
            # Update the draft_id to prevent creating new drafts on save
            self.draft_id = new_draft.id
            if new_draft:
                draft_list.refresh_draft_list(current_search_term)
        else:
            # If there is draft selected, save to that draft instead
            selected_draft = Draft.get_by_id(self.draft_id)
            selected_draft.content = self.text
            selected_draft.save()
            # Reflect the change on sidebar
            draft_list.refresh_draft_list(current_search_term)


class DraftsApp(App):
    """Text Editor in the command line"""

    CSS_PATH = "drafts.tcss"
    BINDINGS = [
        ("ctrl+q", "quit", "Quit"),
        ("ctrl+l", "search", "Search"),
        ("ctrl+n", "new", "New"),
    ]

    def compose(self) -> ComposeResult:
        """Compose the UI of the app"""
        # yield Header()
        with Horizontal():
            yield SideBar()
            yield Editor.code_editor(id="editor", language="markdown")
        yield Footer()

    def action_search(self) -> None:
        search_bar = self.query_one("#search", Input)
        search_bar.can_focus = True
        search_bar.focus()

    def action_new(self) -> None:
        editor = self.query_one("#editor", Editor)
        # Update the draft_id variable to None
        editor.draft_id = None
        # Then clear the editor
        editor.text = ""
        editor.focus()

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
