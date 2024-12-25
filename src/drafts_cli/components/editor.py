from rich.style import Style
from textual.reactive import var
from textual.widgets import TextArea
from textual.binding import Binding
from textual.widgets.text_area import TextAreaTheme

from database import Draft
from components import DraftsList

# Saved as an exmaple for future
my_theme = TextAreaTheme(
    # This name will be used to refer to the theme...
    name="my_cool_theme",
    # Basic styles such as background, cursor, selection, gutter, etc...
    base_style=Style(bgcolor="black"),
    cursor_style=Style(color="white", bgcolor="blue"),
    cursor_line_style=Style(bgcolor="yellow"),
    # `syntax_styles` is for syntax highlighting.
    # It maps tokens parsed from the document to Rich styles.
    syntax_styles={
        "string": Style(color="red"),
        "comment": Style(color="magenta"),
    }
)
custom_theme = TextAreaTheme.get_builtin_theme("monokai")
custom_theme.name = "custom_theme"
custom_theme.base_style = Style(bgcolor="black")


class Editor(TextArea):
    draft_id = var(None)
    BINDINGS = [
        Binding("ctrl+l", "search", "Search"),
        Binding("ctrl+n", "new", "New"),
        Binding("ctrl+s", "save", "Save"),
    ]

    def on_mount(self) -> None:
        self.border_title = "Editor"
        self.register_theme(custom_theme)
        self.theme = "custom_theme"

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
                self.app.notify("New draft saved!", timeout=2)
        else:
            # If there is draft selected, save to that draft instead
            selected_draft = Draft.access_draft(self.draft_id)
            selected_draft.content = self.text
            selected_draft.save()
            # Reflect the change on sidebar
            draft_list.refresh_draft_list(current_search_term)
            self.app.notify("Draft saved!", timeout=2)
