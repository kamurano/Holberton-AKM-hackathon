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
            {table}_title TEXT,
            {table}_questions TEXT,
            {table}_question_description TEXT,
            {table}_answers TEXT,
            {table}_correct_answers TEXT,
            {table}_stars INTEGER,
            {table}_created DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
        with lock:
            self.db.execute(create)
            
    def insert(self, table, avg_score, title, questions, question_description, answers, correct_answers, stars):
        colms = (f"{table}_id", f"{table}_avg_score", f"{table}_title", f"{table}_questions",
                 f"{table}_question_description", f"{table}_answers", f"{table}_correct_answers", f"{table}_stars")
        colms_sql = "`{}`,`{}`,`{}`,`{}`,`{}`,`{}`,`{}`,{}".format(colms[0], colms[1], colms[2], 
                                                                    colms[3], colms[4], colms[5], colms[6], colms[7])
        quiz_id = uuid.uuid4()
        values = quiz_id, avg_score, title, questions, question_description, answers, correct_answers, stars
        values_sql = ', '.join(map(lambda x: f"'{x}'" if x != None else "'Null'", values))
        inserted = f"INSERT INTO `{table}` ({colms_sql}) VALUES ({values_sql})"
        with lock:
            self.db.execute(inserted)
            
    def get_all_records(self, table):
        executed = f"SELECT * FROM {table}"
        with lock:
            records = self.db.execute(executed).fetchall()
        return [dict(data) for data in records] if records else []
    
    
    def get_record_by_id(self, table, id):
        executed = f"SELECT * FROM {table} WHERE `{table}_id`= '{id}'"
        with lock:
            for x in self.db.execute(executed):
                return dict(x)
        return {}
    
    def update_record_by_id(self, table, id, avg_score, title, questions, question_description, answers, correct_answers, stars):
        colms = (f"{table}_avg_score", f"{table}_title", f"{table}_questions",
                 f"{table}_question_description", f"{table}_answers", f"{table}_correct_answers", f"{table}_stars")
        colms_sql = f"`{colms[0]}`='{avg_score}',`{colms[1]}`='{title}',`{colms[2]}`='{questions}',`{colms[3]}`='{question_description}',`{colms[4]}`='{answers}',`{colms[5]}`='{correct_answers}',`{colms[6]}`='{stars}'"
        executed = f"UPDATE `{table}` SET {colms_sql} WHERE `{table}_id`='{id}'"
        with lock:
            self.db.execute(executed)
    
    def delete_record_by_id(self, table, id):
        executed = f"DELETE FROM {table} WHERE `{table}_id`='{id}'"
        with lock:
            self.db.execute(executed)