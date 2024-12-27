from rich.style import Style
from textual import on
from textual.events import Key
from textual.reactive import var
from textual.widgets import TextArea, ListView
from textual.binding import Binding
from textual.widgets.text_area import TextAreaTheme

from database import Draft
from components import DraftsList, ConfirmationModal

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
    is_saved = var(True)

    BINDINGS = [
        Binding("ctrl+l", "search", "Search"),
        Binding("ctrl+n", "new", "New"),
        Binding("ctrl+s", "save", "Save"),
    ]

    def on_mount(self) -> None:
        self.border_title = "Editor"
        self.register_theme(custom_theme)
        self.theme = "custom_theme"

    @on(Key)
    def save_confirmation(self, event: Key) -> None:
        if event.key == "escape" and self.is_saved is False:
            self.notify("Not saved")
            # Pull up the modal and save
            self.app.push_screen(ConfirmationModal(message="Save this draft?", action="save_draft"))

    @on(TextArea.Changed, "#editor")
    def update_save_state(self, event: TextArea.Changed) -> None:
        # self.app.notify(f'{self.is_saved}')
        self.is_saved = False

    def action_save(self) -> None:
        # Get current search term to keep the list filtered
        current_search_term = self.app.query_one("#search").value
        draft_list = self.app.query_one(DraftsList)
        # self.notify(f'{draft_list}')
        # Create a new draft if none selected
        if self.draft_id is None:
            new_draft = Draft.create(content=self.text)
            # Update the draft_id to prevent creating new drafts on save
            self.draft_id = new_draft.id
            self.is_saved = True
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
            self.is_saved = True
            self.app.notify("Draft saved!", timeout=2)
