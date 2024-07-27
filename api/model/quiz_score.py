import sqlite3
import threading
import uuid

from string import ascii_letters
from random import choices


lock = threading.Lock()


class QuizScoreModel:
    def __init__(self):
        con = sqlite3.connect("data.db", check_same_thread=False)
        con.row_factory = sqlite3.Row
        con.isolation_level = None
        self.db = con.cursor()
        self.create_table("quiz_score")

    def create_table(self, table):
        create = f"""
        CREATE TABLE IF NOT EXISTS `{table}`(
            {table}_id TEXT PRIMARY KEY,
            {table}_user_id TEXT,
            {table}_quiz_id TEXT,
            {table}_quiz_score VARCHAR(255),
            {table}_created DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
        with lock:
            self.db.execute(create)