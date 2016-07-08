import sqlite3 as sql
import json

class DbData:
    def __init__(self, name):
        self.name = name

    def query_table_for_dict(self, query):
        con = sql.connect(self.name)
        con.row_factory = sql.Row

        cur = con.cursor()
        cur.execute(query)

        r = [dict((cur.description[i][0], value) \
                  for i, value in enumerate(row)) for row in cur.fetchall()]
        cur.connection.close()
        return r

    def execute_sql(self, query):
        try:
            with sql.connect(self.name) as con:
                cur = con.cursor()

                cur.execute(query)

                con.commit()
                msg = "Done"
                data = {
                    'response': msg
                }
                js = json.dumps(data)
                return True;
        except:
            con.rollback()
            msg = "error in insert operation"
            data = {
                'response': msg
            }
            js = json.dumps(data)
            return False

    def get_list_from_table_json(self, query, entry_function):
        result_dict = self.query_table_for_dict(query)

        faculties = []
        for entry in result_dict:
            faculties.append(entry_function(entry))

        if result_dict:
            return json.dumps(faculties);

    def get_all_from_table_json(self, table):
        result_dict = self.query_table_for_dict("select * from " + table)
        if result_dict:
            return json.dumps(result_dict);