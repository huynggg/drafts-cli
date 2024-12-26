import time
from textual import on
from textual.binding import Binding
from textual.app import App, ComposeResult
from textual.events import Key
from textual.containers import Horizontal
from textual.widgets import Footer, Input, Label, TextArea

from database import Draft, initialize_db
from messages import ConfirmationMessage
from components import DraftsList, SideBar, Editor, DraftItem
from utilities import logger, extract_draft_id


class DraftsApp(App):
    """Text Editor in the command line"""

    CSS_PATH = "app.tcss"
    BINDINGS = [
        Binding("ctrl+l", "search", "Search"),
        Binding("ctrl+n", "new", "New"),
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

    # For some reason, this cannot be put in the ConfirmationModal

    @on(ConfirmationMessage)
    def handle_draft_delete(self, message: ConfirmationMessage):
        if message.action == "delete_draft" and message.confirmation is True:
            # Current screen is the modal; need to pop() to go back to main screen
            self.pop_screen()
            list_view = self.query_one("#draft-list", DraftsList)
            try:
                # Highlighted child is ListItem, then query for Label to get the ID
                highlighted_item_id = extract_draft_id(list_view.highlighted_child.query_one(DraftItem).id)
                # NOTE: need to check if the draft exists?
                # Also, do soft delete here
                highlighted_draft = Draft.access_draft(highlighted_item_id)
                if highlighted_draft.delete_instance():
                    # Remove the ListItem by index
                    list_view.pop(list_view.index)
                    # Toast
                    self.notify("Draft was deleted!", timeout=4)
                    # Check if the deleted draft is also being opened in the editor
                    editor = self.query_one("#editor")
                    if highlighted_item_id == editor.draft_id:
                        # Then clear the editor and update the current opened draft_id
                        # Otherwise, the user would try to save to a draft that was deleted
                        editor.draft_id = None
                        editor.text = ""
            except AttributeError:
                self.notify("Failed to delete draft ")


if __name__ == "__main__":
    # Initialize db on start
    initialize_db()
    app = DraftsApp()
    app.run()
