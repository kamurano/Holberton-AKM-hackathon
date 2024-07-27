import sqlite3
import threading
import uuid

from string import ascii_letters
from random import choices


lock = threading.Lock()


class QuizModel:
    def __init__(self):
        con = sqlite3.connect("data.db", check_same_thread=False)
        con.row_factory = sqlite3.Row
        con.isolation_level = None
        self.db = con.cursor()
        self.create_table("quiz")

    def create_table(self, table):
        create = f"""
        CREATE TABLE IF NOT EXISTS `{table}`(
            {table}_id TEXT PRIMARY KEY,
            {table}_avg_score VARCHAR(255),
            {table}_questions TEXT,
            {table}_question_description TEXT,
            {table}_answers TEXT,
            {table}_correct_answers TEXT,
            {table}_stars VARCHAR(255),
            {table}_created DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
        with lock:
            self.db.execute(create)