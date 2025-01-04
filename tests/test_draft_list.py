import pytest
from drafts_cli.app import DraftsApp
from .setup_test import setup_test_db


@pytest.mark.asyncio
async def test_add_new_draft(setup_test_db):
    app = DraftsApp()
    async with app.run_test() as pilot:
        draft_list = app.side_bar.draft_list
        # Number of ListItem should also be 0
        assert len(draft_list.children) == 0

        # Now add a draft then count
        await pilot.press("ctrl+n")
        await pilot.press("t", "e", "s", "t")
        await pilot.press("ctrl+s")
        assert len(draft_list.children) == 1

        # Add another one
        await pilot.press("ctrl+n")
        await pilot.press("a", "b", "c")
        await pilot.press("ctrl+s")
        assert len(draft_list.children) == 2


@pytest.mark.asyncio
async def test_delete_draft(setup_test_db):
    app = DraftsApp()
    async with app.run_test() as pilot:
        draft_list = app.side_bar.draft_list
        # Number of ListItem should also be 0
        assert len(draft_list.children) == 0

        # Now add a draft then count
        await pilot.press("ctrl+n")
        await pilot.press("t", "e", "s", "t")
        await pilot.press("ctrl+s")
        assert len(draft_list.children) == 1

        # Now delete the item & count
        await pilot.press("escape")
        await pilot.press("down")  # select the first
        await pilot.press("ctrl+d")
        await pilot.press("n")
        # Should still 1 since we chose No
        assert len(draft_list.children) == 1
        # Try again, chose Yes
        await pilot.press("ctrl+d")
        await pilot.press("y")
        assert len(draft_list.children) == 0


@pytest.mark.asyncio
async def test_selecting_draft(setup_test_db):
    app = DraftsApp()
    async with app.run_test() as pilot:
        draft_list = app.side_bar.draft_list
        # Number of ListItem should also be 0
        assert len(draft_list.children) == 0
        # Now add a new draft
        await pilot.press("ctrl+n")
        await pilot.press("t", "e", "s", "t")
        await pilot.press("ctrl+s")
        # Add another one
        await pilot.press("ctrl+n")
        await pilot.press("a", "b", "c")
        await pilot.press("ctrl+s")

        # Focus the draft List then pick the second one
        await pilot.press("escape")
        await pilot.press("down", "down")  # select the 2nd
        await pilot.press("enter")
        # Should be the first one added
        assert app.editor.text == "test"
        # Now escape then go down 1 to pick the latest
        await pilot.press("escape")
        await pilot.press("n")  # To escape without saving the current draft
        # Need to go up since the highlighted item is currently 2nd
        await pilot.press("up")  # select the 1st
        await pilot.press("enter")
        assert app.editor.text == "abc"
