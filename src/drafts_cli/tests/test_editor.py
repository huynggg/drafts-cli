import os
import sys
# To resolve the ImportError issues by adding the project abs path to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import DraftsApp
from database import Draft, initialize_db


@pytest.fixture
def setup_test_db():
    """Set up an in-memory test database."""
    db = initialize_db('drafts_test.db')  # Configure `db` for testing
    yield  # Test cases execute here
    db.drop_tables([Draft])  # Clean up after tests
    db.close()


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
