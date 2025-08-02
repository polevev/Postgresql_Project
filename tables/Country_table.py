# Таблица Телефоны и особые действия с ней.
import re
from dbtable import *

class CountryTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + '"Country"'

    def columns(self):
        return {"id": ["serial", "PRIMARY KEY"],
                "Short_Name": ["varchar(10)", "NOT NULL", "CHECK (length(Short_Name)=3)"],
                "full_Name": ["varchar(30)", "NOT NULL"],
                "reg_ion": ["varchar(20)", "NOT NULL"]}

    def primary_key(self):
        return ['id']

    def table_constraints(self):
        return ["CONSTRAINT reg_ion UNIQUE (reg_ion)"]

    def column_names_without_id(self):
        res = sorted(self.columns().keys(), key = lambda x: x)
        if 'id' in res:
            res.remove('id')
        return res

    def select_by_id(self, val):
        sql = f"SELECT id, full_Name FROM {self.table_name()} WHERE id = " + "%s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (val,))
        return cur.fetchone()

    def select_name_by_id(self, val):
        sql = f"SELECT full_Name FROM {self.table_name()} WHERE id = " + "%s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (val,))
        return cur.fetchone()

    def select_by_name(self, val):
        sql = "SELECT id FROM " + self.table_name()
        sql += " WHERE reg_ion = %(reg_ion)s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, {"reg_ion": val})
        return cur.fetchone()

    '''def insert_one(self, val):
        sql = "INSERT INTO " + self.table_name() + "VALUES(%(ID)s,%(Short_Name)s,%(full_Name)s,%(reg_ion)s)"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, {"Full_Name": val})'''

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

    def delete_by_ID(self, val):
        sql = f"DELETE FROM {self.table_name()} WHERE ID =" + " %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (val,))
        self.dbconn.conn.commit()

    def update(self, vals):
        sql = f"UPDATE {self.table_name()} SET full_Name = " + "%(full_Name)s WHERE ID = %(id)s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, {"Full_Name": vals[0], "ID": vals[1]})
        self.dbconn.conn.commit()

    def find_by_position(self, num):
        sql = "SELECT * FROM " + self.table_name()
        sql += " ORDER BY full_Name"
        sql += " LIMIT 1 OFFSET %(offset)s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, {"offset": int(num) - 1})
        return cur.fetchone()