import sqlite3 as sql
import requests
import json
from collections import namedtuple
import pdb

con = sql.connect("table.db")
con.row_factory = sql.Row

cur = con.cursor()
cur.execute("select * from subjects")

r = [dict((cur.description[i][0], value) \
          for i, value in enumerate(row)) for row in cur.fetchall()]
cur.connection.close()

subjects = []

for entry in r:
    subjects.append(entry['subject'])

print subjects

WATERLOO_API = 'https://api.uwaterloo.ca/v2/'
WATERLOO_API_KEY = 'b90f031fa651186849e95363ad68b726'

for subject in subjects:
    params = (('key',WATERLOO_API_KEY))
    r = requests.get(WATERLOO_API + 'courses/' + subject + '.json?key=' + WATERLOO_API_KEY)
    #print r.json()
    course_json = r.json()
    if course_json and course_json['data']:
        for course in course_json['data']:
            course_id = course['course_id']
            catalog_number = course['catalog_number']
            #print subject, catalog_number
            #r = requests.get(WATERLOO_API + 'courses/' + subject + '/' + catalog_number + '.json?key=' + WATERLOO_API_KEY)
            #course = r.json()['data']
            #pdb.set_trace()
            title = course['title']
            description = course['description']
            #antireqs = ''
            #coreqs = ''
            #if course.get('antirequisites'):
            #    antireqs = course['antirequisites']
            #if course.get('corequisites'):
            #    coreqs = course['corequisites']
            print (course_id, subject, catalog_number, title, description)
            try:
                with sql.connect("table.db") as con:
                    cur = con.cursor()

                    cur.execute("INSERT INTO courses (course_id, subject, catalog_number, title, description)\
                    VALUES(?, ?, ?, ?, ?)", (course_id, subject, catalog_number, title, description))

                    con.commit()
                    print "Record successfully added"
            except:
                con.rollback()
                print "error in insert operation"




