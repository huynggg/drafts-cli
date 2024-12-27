from typing import Iterable
from textual import on
from textual.binding import Binding
from textual.app import App, ComposeResult, SystemCommand
from textual.screen import Screen
from textual.events import Key
from textual.containers import Horizontal
from textual.widgets import Footer, Input, TextArea

from database import Draft, initialize_db
from messages import ConfirmationMessage
from components import DraftsList, SideBar, Editor, DraftItem
from utilities import logger


class DraftsApp(App):
    """Text Editor in the command line"""

    CSS_PATH = "app.tcss"
    BINDINGS = [
        Binding("ctrl+l", "search", "Search", key_display="ctrl+l"),
        Binding("ctrl+n", "new", "New", key_display="ctrl+n"),
        Binding("ctrl+p", "command_palette", "Open Command Palette", key_display="ctrl+p", show=False),
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

    def on_mount(self) -> None:
        # Focus on the search on start
        self.query_one("#editor", TextArea).focus()

    # Add this "create new" command to the command pallete
    def get_system_commands(self, screen: Screen) -> Iterable[SystemCommand]:
        yield from super().get_system_commands(screen)
        yield SystemCommand("New", "Create new draft", self.action_new)
        yield SystemCommand("Search", "Search draft", self.action_search)

    @on(Key)
    def on_key(self, event: Key):
        if event.key == "tab" or event.key == "shift+tab":
            self.query_one("#search", Input).can_focus = False

    @on(ConfirmationMessage)
    # For some reason, this cannot be put in the ConfirmationModal
    def handle_draft_delete(self, message: ConfirmationMessage):
        if message.action == "delete_draft" and message.confirmation is True:
            # Current screen is the modal; need to pop() to go back to main screen
            self.pop_screen()
            list_view = self.query_one("#draft-list", DraftsList)
            try:
                # Highlighted child is ListItem, then query for Label to get the ID
                highlighted_item_id = list_view.highlighted_child.query_one(DraftItem).id
                # NOTE: need to check if the draft exists?
                # Also, do soft delete here
                highlighted_draft = Draft.access_draft(highlighted_item_id)
                if highlighted_draft.delete_instance():
                    # Remove the ListItem by index
                    list_view.pop(list_view.index)
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

    @on(ConfirmationMessage)
    # For some reason, this cannot be put in the ConfirmationModal
    def handle_save_draft(self, message: ConfirmationMessage):
        if message.action == "save_draft" and message.confirmation is True:
            self.pop_screen()
            try:
                self.query_one("#editor", Editor).action_save()
            except Exception:
                self.notify("Failed to save draft")


if __name__ == "__main__":
    # Initialize db on start
    initialize_db()
    app = DraftsApp()
    app.run()
