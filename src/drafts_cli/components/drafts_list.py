from textual import on
from textual.widgets import ListView, ListItem, Label
from textual.binding import Binding

from components import ConfirmationModal
from components.draft_item import DraftItem
from database import Draft
from utilities import extract_draft_id


class DraftsList(ListView):
    BINDINGS = [
        Binding("ctrl+d", "delete", "Delete"),
        Binding("k", "cursor_up", "Up"),
        Binding("j", "cursor_down", "Down"),
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

        # selected_draft = event.item.query_one(ListItem)
        # Extract the id then update the editor's opened draft id variable
        editor.draft_id = extract_draft_id(event.item.id)
        # self.notify(str(editor.draft_id))
        # Get the content from the db
        draft = Draft.access_draft(editor.draft_id)
        # Update the content of the text area
        editor.focus()
        editor.text = draft.content
        editor.cursor_location = editor.document.end

    async def refresh_draft_list(self, search_term: str = "") -> None:
        # await self.notify(f'{self.clear()}')
        # for child in self.children:
        #     self.notify(f'{child}')
        self.notify(f'before: {len(self)}')
        self.notify(f'{type(self)}')
        # self.query_one(DraftsList).clear()
        await self.clear()
        self.notify(f'after: {len(self)}')
        # self.notify(f'{(self.children)}')
        self.notify(f'{type(self)}')
        # # NOTE: Soft delete
        # drafts_list = Draft.select().order_by(Draft.modified_at.desc())
        # new_items = []
        # if len(self) == 0:
        #     for draft in drafts_list:
        #         if search_term.lower() in draft.content.lower():
        #             # self.append(ListItem(DraftItem(content=draft.content, footer=str(draft.modified_at)), id=f'draft-{draft.id}', classes="draft-item"))
        #             new_items.append(ListItem(DraftItem(content=draft.content, footer=str(draft.modified_at)), id=f'draft-{draft.id}', classes="draft-item"))
        #     self.extend(new_items)
