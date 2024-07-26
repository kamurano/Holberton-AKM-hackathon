import sqlite3
import threading
import uuid

from string import ascii_letters
from random import choices


lock = threading.Lock()


class UserModel:
    def __init__(self):
        con = sqlite3.connect("data.db", check_same_thread=False)
        con.row_factory = sqlite3.Row
        con.isolation_level = None
        self.db = con.cursor()
        self.create_table("users")

    def create_table(self, table):
        create = f"""
        CREATE TABLE IF NOT EXISTS `{table}`(
            {table}_id TEXT PRIMARY KEY,
            {table}_fname VARCHAR(30),
            {table}_sname VARCHAR(30),
            {table}_email VARCHAR(50) NOT NULL UNIQUE,
            {table}_password VARCHAR(256) NOT NULL,
            {table}_is_active BOOLEAN DEFAULT FALSE,
            {table}_is_admin BOOLEAN DEFAULT FALSE,
            {table}_created DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
        with lock:
            self.db.execute(create)

    def insert(self, table, fname, sname, email, password, is_admin=False):
        colms = (f"{table}_id", f"{table}_fname", f"{table}_sname",
                 f"{table}_email", f"{table}_password", f"{table}_is_admin")
        colms_sql = "`{}`,`{}`,`{}`,`{}`,`{}`,{}".format(colms[0], colms[1], colms[2], 
                                                                colms[3], colms[4], colms[5])
        user_id = uuid.uuid4()
        values = user_id, fname, sname , email, password, is_admin 
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

    def get_record_by_email(self, table, email):
        executed = f"SELECT * FROM {table} WHERE `{table}_email` = '{email}'"
        with lock:
            for x in self.db.execute(executed):
                return dict(x)
            
    def get_user_active_status(self, table, email):
        executed = f"SELECT `{table}_is_active` FROM {table} WHERE `{table}_email` = '{email}'"
        with lock:
            for x in self.db.execute(executed):
                return dict(x)
            
    def activate_email(self, table, email):
        executed = f"UPDATE {table} SET `{table}_is_active`= TRUE WHERE `{table}_email` = '{email}'"
        with lock:
            self.db.execute(executed)