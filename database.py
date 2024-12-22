import os
import logging
from textual.logging import TextualHandler
from peewee import SqliteDatabase, Model, TextField, DateTimeField, BooleanField, AutoField
from datetime import datetime

# Configure logging
logging.basicConfig(
    level="NOTSET",
    handlers=[TextualHandler()],
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Path to the database file
DB_PATH = 'drafts.db'

# Initialize the database
db = SqliteDatabase(DB_PATH)


# Base model class
class BaseModel(Model):
    class Meta:
        database = db


# Draft model
class Draft(BaseModel):
    id = AutoField()
    content = TextField()  # The main content of the draft
    created_at = DateTimeField(default=datetime.utcnow)  # Timestamp for creation
    accessed_at = DateTimeField(default=datetime.utcnow)  # Timestamp for last accessed
    modified_at = DateTimeField(default=datetime.utcnow)  # Timestamp for last modification
    starred = BooleanField(default=False)  # Whether the draft is starred
    deleted = BooleanField(default=False)  # Whether the draft is marked as deleted

    # Overriding the save method to update data before saving
    # Can be used for data validation
    def save(self, *args, **kwargs):
        # Automatically update `modified_at` before saving
        self.modified_at = datetime.utcnow()
        super().save(*args, **kwargs)

    @classmethod
    def access_draft(cls, draft_id: int) -> "Draft":
        """Preferred way to access a draft by id.
        This will also update the accessed_at
        """
        draft = Draft.get_by_id(draft_id)
        draft.accessed_at = datetime.utcnow
        return draft


# Function to initialize the database
def initialize_db():
    # Check if the database file exists
    if not os.path.exists(DB_PATH):
        logger.info(f"Database file {DB_PATH} does not exist. Creating...")
    else:
        logger.info(f"Database file {DB_PATH} already exists.")

    # Connect to the database and create tables
    with db:
        db.create_tables([Draft], safe=True)
        logger.info("Database and tables created successfully.")
