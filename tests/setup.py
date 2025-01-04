import pytest
from drafts_cli.database import Draft, initialize_db


@pytest.fixture
def setup_test_db():
    """Set up an in-memory test database."""
    db = initialize_db('drafts_test.db')  # Configure `db` for testing
    yield  # Test cases execute here
    db.drop_tables([Draft])  # Clean up after tests
    db.close()
