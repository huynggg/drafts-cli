import pytest
from drafts_cli.app import DraftsApp
from drafts_cli.database import Draft
from .setup_test import setup_test_db


@pytest.mark.asyncio
async def test_content_editing(setup_test_db):
    app = DraftsApp()
    async with app.run_test() as pilot:
        # Check empty on start
        assert app.editor.text == ""

        # Adding text
        await pilot.click("#editor")
        await pilot.press("a", "b", "c")
        assert app.editor.text == "abc"

        # Removing one character
        await pilot.press("backspace")
        assert app.editor.text == "ab"

        # Adding text back
        await pilot.press("e", "f")
        assert app.editor.text == "abef"


@pytest.mark.asyncio
async def test_save_content(setup_test_db):
    app = DraftsApp()
    async with app.run_test() as pilot:
        # Confirm that the count is zero
        count_initial = Draft.select().count()
        assert count_initial == 0

        # Write something to the editor then save
        await pilot.click("#editor")
        await pilot.press("t", "e", "s", "t")
        await pilot.press("ctrl+s")
        # Compare with the db
        # Count should now be 1
        count = Draft.select().count()
        assert count == 1
        # Content comparison
        content = Draft.select().first().content
        assert app.editor.text == content
        assert app.editor.text == "test"


@pytest.mark.asyncio
async def test_update_content(setup_test_db):
    app = DraftsApp()
    async with app.run_test() as pilot:
        # Write something to the editor then save
        await pilot.click("#editor")
        await pilot.press("t", "e", "s", "t")
        await pilot.press("ctrl+s")

        # Content comparison
        content_initial = Draft.select().first().content
        assert app.editor.text == content_initial

        # Now delete 2 characters
        await pilot.press("backspace", "backspace")
        assert app.editor.text == "te"
        # Then save
        await pilot.press("ctrl+s")

        content_saved = Draft.select().first().content
        assert app.editor.text == content_saved
        assert app.editor.text == "te"


@pytest.mark.asyncio
async def test_delete_content(setup_test_db):
    app = DraftsApp()
    async with app.run_test() as pilot:
        # Write something to the editor then save
        await pilot.click("#editor")
        await pilot.press("t", "e", "s", "t")
        await pilot.press("ctrl+s")
        # Count should be 1
        count = Draft.select().count()
        assert count == 1
        # Now delete and compare
        query = Draft.delete()
        delete_count = query.execute()
        assert delete_count == 1

        # Count should be 1
        count_after_delete = Draft.select().count()
        assert count_after_delete == 0
