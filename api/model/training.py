import sqlite3
import threading
import uuid

from string import ascii_letters
from random import choices


lock = threading.Lock()


class TrainingModel:
    def __init__(self):
        con = sqlite3.connect("data.db", check_same_thread=False)
        con.row_factory = sqlite3.Row
        con.isolation_level = None
        self.db = con.cursor()
        self.create_table("training")

    def create_table(self, table):
        create = f"""
        CREATE TABLE IF NOT EXISTS `{table}`(
            {table}_id TEXT PRIMARY KEY,
            {table}_quiz_id TEXT,
            {table}_title TEXT,
            {table}_content TEXT,
            {table}_stars VARCHAR(255),
            {table}_created DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
        with lock:
            self.db.execute(create)
            
    def insert(self, table, quiz_id, title, content, stars):
        colms = (f"{table}_id", f"{table}_quiz_id", f"{table}_title",
                 f"{table}_content", f"{table}_stars")
        colms_sql = "`{}`,`{}`,`{}`,`{}`,{}".format(colms[0], colms[1], colms[2], 
                                                    colms[3], colms[4])
        training_id = uuid.uuid4()
        values = training_id, quiz_id, title, content, stars
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
    
    def get_record_by_quiz_id(self, table, quiz_id):
        executed = f"SELECT * FROM {table} WHERE `{table}_quiz_id`= '{quiz_id}'"
        with lock:
            for x in self.db.execute(executed):
                return dict(x)
        return {}
    
    
    def update_record(self, table, id, quiz_id, title, content, stars):
        executed = f"""
        UPDATE `{table}` SET `{table}_quiz_id`='{quiz_id}', `{table}_title`='{title}',
        `{table}_content`='{content}', `{table}_stars`='{stars}'
        WHERE `{table}_id`='{id}'
        """
        with lock:
            self.db.execute(executed)
            
    def delete_record(self, table, id):
        executed = f"DELETE FROM `{table}` WHERE `{table}_id`='{id}'"
        with lock:
            self.db.execute(executed)
    
    