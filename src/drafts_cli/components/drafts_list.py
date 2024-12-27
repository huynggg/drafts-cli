from textual import on
from textual.widgets import ListView, ListItem
from textual.binding import Binding

from components import ConfirmationModal
from components.draft_item import DraftItem
from database import Draft
from utilities import extract_draft_id


class DraftsList(ListView):
    BINDINGS = [
        Binding("k", "cursor_up", "Up"),
        Binding("j", "cursor_down", "Down"),
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
        draft = Draft.access_draft(extract_draft_id(editor.draft_id))
        # Update the content of the text area
        editor.focus()
        editor.text = draft.content
        editor.cursor_location = editor.document.end

    def refresh_draft_list(self, search_term: str = "") -> None:
        self.clear()
        # NOTE: Soft delete
        drafts_list = Draft.select().order_by(Draft.modified_at.desc())
        for draft in drafts_list:
            if search_term.lower() in draft.content.lower():
                self.append(ListItem(DraftItem(content=draft.content, modified=str(draft.modified_at), id=f'draft-{draft.id}')))
