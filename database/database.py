import sqlite3
from config.settings import DATABASE_FILE


class Database:
    def __init__(self):
        self.db_path = DATABASE_FILE

    def connect(self):
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        return sqlite3.connect(self.db_path)

    def initialize(self):
        schema_path = self.db_path.parent / "schema.sql"

        with self.connect() as conn:
            with open(schema_path, "r", encoding="utf-8") as file:
                conn.executescript(file.read())