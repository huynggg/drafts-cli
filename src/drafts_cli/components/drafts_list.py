from textual import on
from textual.widgets import ListView, ListItem
from textual.binding import Binding

from drafts_cli.components import ConfirmationModal
from drafts_cli.components.draft_item import DraftItem
from drafts_cli.database import Draft


class DraftsList(ListView):
    BINDINGS = [
        Binding("j", "cursor_down", "Down"),
        Binding("k", "cursor_up", "Up"),
        Binding("ctrl+d", "delete", "Delete", key_display="ctrl+d"),
    ]

    def on_mount(self) -> None:
        self.border_title = "Drafts"

    def action_delete(self) -> None:
        if self.index is not None:
            self.app.push_screen(ConfirmationModal(message="Delete this draft?", action="delete_draft"))
        else:
            self.app.notify("Delete failed - No draft selected")

    @on(ListView.Selected)
    def on_list_view_selected(self, event: ListView.Selected) -> None:
        editor = self.app.query_one("#editor")
        selected_draft = event.item.query_one(DraftItem)
        # Update the editor's opened draft id variable
        editor.draft_id = selected_draft.id
        # Get the content from the db
        draft = Draft.access_draft(editor.draft_id)
        # Update the content of the text area
        editor.focus()
        editor.text = draft.content
        editor.cursor_location = editor.document.end

        # Marking the draft item visually
        # NOTE: Previously went with watching draft_id then update, but failed on save
        # Remove the class for all the draft items first
        for item in self.children:
            item.get_child_by_type(DraftItem).remove_class("draft-selected")
        # Then add the class to the selected one
        selected_draft.add_class("draft-selected")

    def refresh_draft_list(self, search_term: str = "") -> None:
        self.clear()
        drafts_list = Draft.select().order_by(Draft.modified_at.desc())
        for draft in drafts_list:
            if search_term.lower() in draft.content.lower():
                self.append(ListItem(DraftItem(content=draft.content, modified=str(draft.modified_at), id=f'draft-{draft.id}')))
