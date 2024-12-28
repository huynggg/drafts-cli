import os
from peewee import SqliteDatabase, Model, TextField, DateTimeField, BooleanField, AutoField
from datetime import datetime
from utilities import logger


# Path to the database file
DB_PATH = 'drafts.db'
# DB_PATH = os.getenv('DB_PATH', 'drafts.db')  # Use 'drafts.db' if DB_PATH is not set

# Initialize the database
db = SqliteDatabase(None)


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
    def access_draft(cls, draft_id: str) -> "Draft":
        """Preferred way to access a draft by id.
        This will also update the accessed_at
        """
        formated_draft_id = draft_id
        if "draft" in str(draft_id):
            formated_draft_id = draft_id.split("-")[1]
        draft = Draft.get_by_id(formated_draft_id)
        draft.accessed_at = datetime.utcnow()
        draft.save()
        return draft


# Function to initialize the database
def initialize_db(db_path: str) -> SqliteDatabase:
    # Check if the database file exists
    if not os.path.exists(db_path):
        logger.info(f"Database file {db_path} does not exist. Creating...")
    else:
        logger.info(f"Database file {db_path} already exists.")

    # Connect to the database and create tables
    db.init(db_path)
    with db:
        db.create_tables([Draft], safe=True)
        logger.info("Database and tables created successfully.")
        return db
