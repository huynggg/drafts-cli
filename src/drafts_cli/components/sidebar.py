from textual import on
from textual.containers import VerticalGroup
from textual.widgets import Input, ListItem
from textual.app import ComposeResult

from components import DraftsList
from components.draft_item import DraftItem
from database import Draft
from utilities import logger


class SideBar(VerticalGroup):
    """The left bar containing the draft list and a search bar"""

    def compose(self) -> ComposeResult:
        search_bar = Input(placeholder="Search...", type="text", id="search")
        search_bar.can_focus = False
        search_bar.border_title = "🔍"
        yield search_bar
        with DraftsList(id="draft-list"):
            # NOTE: Soft delete
            drafts_list = Draft.select().order_by(Draft.modified_at.desc())
            for draft in drafts_list:
                yield ListItem(DraftItem(content=draft.content, modified=str(draft.modified_at), id=f"draft-{draft.id}"))

    @on(Input.Changed, "#search")
    def on_search_bar_change(self, search_term: Input.Changed) -> None:
        logger.debug(search_term.value)
        list_view = self.query_one(DraftsList)
        # Populate the list with new items
        list_view.refresh_draft_list(search_term.value)
