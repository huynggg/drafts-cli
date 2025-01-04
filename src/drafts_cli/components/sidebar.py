from textual import on
from textual.containers import VerticalGroup
from textual.widgets import Input, ListItem
from textual.app import ComposeResult

from drafts_cli.components import DraftsList
from drafts_cli.components.draft_item import DraftItem
from drafts_cli.database import Draft
from drafts_cli.utilities import logger


class SideBar(VerticalGroup):
    """The left bar containing the draft list and a search bar"""

    def compose(self) -> ComposeResult:
        self.search_bar = Input(placeholder="Search...", type="text", id="search")
        self.search_bar.can_focus = False
        self.search_bar.border_title = "🔍"
        yield self.search_bar
        with DraftsList(id="draft-list") as self.draft_list:
            drafts_list_db = Draft.select().order_by(Draft.modified_at.desc())
            for draft in drafts_list_db:
                yield ListItem(DraftItem(content=draft.content, modified=str(draft.modified_at), id=f"draft-{draft.id}"))

    @on(Input.Changed, "#search")
    def on_search_bar_change(self, search_term: Input.Changed) -> None:
        logger.debug(search_term.value)
        list_view = self.query_one(DraftsList)
        # Populate the list with new items
        list_view.refresh_draft_list(search_term.value)
