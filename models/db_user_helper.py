from flask import Response
import sqlite3 as sql
import json

class DbUserHelper:
    @staticmethod
    def create_user(student_id, name):
        error = None
        try:
            with sql.connect("table.db") as con:
                cur = con.cursor()

                cur.execute("INSERT INTO users (student_id, name)\
                VALUES(?, ?)", (student_id, name))

                con.commit()
                msg = "Record successfully added"
                data = {
                    'response': msg
                }
                js = json.dumps(data)

                resp = Response(js, status=200, mimetype='application/json')
                return resp;
        except:
            con.rollback()
            msg = "error in insert operation"
            data = {
                'response': msg
            }
            js = json.dumps(data)

            resp = Response(js, status=400, mimetype='application/json')
            return resp;
            # the code below is executed if the request method
            # was GET or the credentials were invalid

    @staticmethod
    def query_users(dbData):
        return dbData.query_table_for_dict('select * from users')