# Таблица персоны и особые действия с ней
import re
from dbtable import *

class PlayersTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + '"Players"'

    def columns(self):
        return {"id": ["serial", "PRIMARY KEY"],
                "Surname": ["varchar(15)", "NOT NULL"],
                "Name": ["varchar(15)", "NOT NULL"],
                "country_id": ["integer", "NOT NULL", 'REFERENCES public."Country"(id) ON DELETE CASCADE'],
                "team_id": ["integer", "NOT NULL"]}

    def primary_key(self):
        return ['id']

    def table_constraints(self):
        return ["CONSTRAINT roster UNIQUE (Surname, Name)"]

    def column_names_without_id(self):
        res = sorted(self.columns().keys(), key = lambda x: x)
        if 'id' in res:
            res.remove('id')
        return res

    def all_by_Country_id(self, pid):
        sql = f"SELECT id, Surname, Name FROM {self.table_name()} WHERE country_id = %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (pid,))
        return cur.fetchall()

    def delete_by_c_ID(self, val):
        sql = "DELETE FROM " + self.table_name()
        sql += " WHERE country_id = %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (val,))
        self.dbconn.conn.commit()

    def select_by_id(self, val):
        sql = f"SELECT id FROM {self.table_name()} WHERE id = " + "%s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (val,))
        return cur.fetchone()
    def delete_by_ID(self, val):
        sql = "DELETE FROM " + self.table_name()
        sql += " WHERE id = %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (val,))
        self.dbconn.conn.commit()

    def add_by_Country_id(self, pid, vals):
        for i in range(0, len(vals)):
            if type(vals[i]) == str:
                vals[i] = "'" + vals[i] + "'"
            else:
                vals[i] = str(vals[i])
        sql = "INSERT INTO " + self.table_name() + "("
        sql += ", ".join(self.column_names_without_id()) + ") VALUES("
        sql += ", ".join(vals) + "," + str(pid) + ")"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        self.dbconn.conn.commit()
        return


    def create(self):
        sql = "CREATE TABLE " + self.table_name() + "("
        arr = [k + " " + " ".join(v) for k, v in self.columns().items()]
        sql += ", ".join(arr + self.table_constraints())
        sql += ")"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        self.dbconn.conn.commit()
        return

    '''def insert_one(self, vals):
        for i in range(0, len(vals)):
            if type(vals[i]) == str:
                vals[i] = re.split(r"'|--|\(|\)", vals[i])[0]
                vals[i] = "'" + vals[i] + "'"
            else:
                vals[i] = str(vals[i])
        sql = "INSERT INTO " + self.table_name() + "("
        sql += ", ".join(self.column_names_without_id()) + ") VALUES("
        sql += ", ".join(vals) + ")"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        self.dbconn.conn.commit()
        return'''
    def insert_one(self, vals):
        for i in range(0, len(vals)):
            if type(vals[i]) == str:
                vals[i] = "'" + vals[i] + "'"
            else:
                vals[i] = str(vals[i])
        sql = "INSERT INTO " + self.table_name() + "("
        sql += ", ".join(self.column_names_without_id()) + ") VALUES("
        sql += ", ".join(vals) + ")"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        self.dbconn.conn.commit()
        return

    def find_by_position(self, num):
        sql = "SELECT * FROM " + self.table_name()
        sql += " ORDER BY full_Name"
        sql += " LIMIT 1 OFFSET %(offset)s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, {"offset": int(num) - 1})
        return cur.fetchone()