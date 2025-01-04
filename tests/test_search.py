import pytest
from drafts_cli.app import DraftsApp
from .setup_test import setup_test_db


@pytest.mark.asyncio
async def test_search_found(setup_test_db):
    app = DraftsApp()
    async with app.run_test() as pilot:
        # Confirm draft list has no item initially
        draft_list = app.side_bar.draft_list
        assert len(draft_list.children) == 0
        # Write 1st draft: test
        await pilot.click("#editor")
        await pilot.press("t", "e", "s", "t")
        await pilot.press("ctrl+s")

        # Write 2nd draft: st
        await pilot.press("ctrl+n")
        await pilot.press("s", "t")
        await pilot.press("ctrl+s")
        # List should have 2 items now
        assert len(draft_list.children) == 2

        # Change to search input
        await pilot.press("ctrl+l")
        # Type in "te"
        await pilot.press("t", "e")
        # This search term should show only 1
        assert len(draft_list.children) == 1

        # Escape then ctrl+l to get back to the search bar
        await pilot.press("escape")
        await pilot.press("ctrl+l")
        # Type in search term "st"; this term should match 2 item
        await pilot.press("s", "t")
        assert len(draft_list.children) == 2


@pytest.mark.asyncio
async def test_search_not_found(setup_test_db):
    app = DraftsApp()
    async with app.run_test() as pilot:
        # Confirm draft list has no item initially
        draft_list = app.side_bar.draft_list
        assert len(draft_list.children) == 0
        # Write 1st draft: test
        await pilot.click("#editor")
        await pilot.press("t", "e", "s", "t")
        await pilot.press("ctrl+s")

        # Write 2nd draft: st
        await pilot.press("ctrl+n")
        await pilot.press("s", "t")
        await pilot.press("ctrl+s")
        # List should have 2 items now
        assert len(draft_list.children) == 2

        # Escape then ctrl+l to get back to the search bar
        await pilot.press("ctrl+l")
        # Type in search term "a"; this term should match none
        await pilot.press("a")
        assert len(draft_list.children) == 0
