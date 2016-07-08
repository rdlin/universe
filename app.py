from flask import Flask, render_template, send_from_directory
from flask_flatpages import FlatPages
from flask_frozen import Freezer
from flask import request
import json
import requests
import re

from models import DbData, ReqHelper, DbUserHelper, DbReqHelper, DbSubjectCourseHelper, DbProgramFacultyHelper, \
    DbSchedulesHelper

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = 'content'
POST_DIR = 'posts'
WATERLOO_API = 'https://api.uwaterloo.ca/v2/'
WATERLOO_API_KEY = 'REDACTED'

app = Flask(__name__)
flatpages = FlatPages(app)
freezer = Freezer(app)
app.config.from_object(__name__)

dbData = DbData('table.db')

'''
WEBSITE
'''


@app.route("/posts/")
def posts():
    posts = [p for p in flatpages if p.path.startswith(POST_DIR)]
    posts.sort(key=lambda item: item['date'], reverse=False)
    return render_template('posts.html', posts=posts)


@app.route('/posts/<name>/')
def post(name):
    path = '{}/{}'.format(POST_DIR, name)
    post = flatpages.get_or_404(path)
    return render_template('post.html', post=post)


@app.route('/static/images/<path:path>')
def send_js(path):
    return send_from_directory('static/images', path)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/blog')
def blog():
    return render_template('blog.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


'''
UniVerse
'''


@app.route('/universe')
def info():
    return "Welcome to Universe!"


'''
USERS
'''


@app.route('/universe/users/create', methods=['GET'])
def create_user():
    student_id = request.args.get('student_id')
    name = request.args.get('name')
    return DbUserHelper.create_user(student_id, name)


@app.route('/universe/users/show')
def show_users():
    return render_template("list.html", rows=DbUserHelper.query_users(dbData))


'''
SUBJECTS AND COURSES
'''


@app.route('/universe/subjects/list')
def show_subjects_list():
    return DbSubjectCourseHelper.get_subject_list_from_db(dbData)


@app.route('/universe/courses/all')
def show_courses():
    return dbData.get_all_from_table_json('courses')


@app.route('/universe/courses/list')
def show_courses_list():
    return DbSubjectCourseHelper.get_course_list_from_db(dbData)


@app.route('/universe/courses/list/<subject>')
def show_courses_list_by_subject(subject):
    return DbSubjectCourseHelper.get_course_list_by_subject_from_db(dbData, subject)


@app.route('/universe/courses/info/<subject>/<catalog_number>')
def show_course_info(subject, catalog_number):
    r = DbSubjectCourseHelper.get_course_info_from_db(dbData, subject, catalog_number)

    if r:
        return json.dumps(r);


'''
PROGRAMS AND FACULTIES
'''


@app.route('/universe/faculties/list')
def show_faculties_list():
    return DbProgramFacultyHelper.get_faculty_list_from_db(dbData)


@app.route('/universe/programs/list')
def show_programs_list():
    return DbProgramFacultyHelper.get_program_list_from_db(dbData)


@app.route('/universe/programs/all')
def show_programs():
    return dbData.get_all_from_table_json('programs')


'''
SCHEDULES
'''


@app.route('/universe/terms/all')
def show_terms():
    return dbData.get_all_from_table_json('terms')


@app.route('/universe/subjects/all')
def show_subjects():
    return dbData.get_all_from_table_json('subjects')


def update_classes(subject, catalog_number):
    r = requests.get(
        WATERLOO_API + 'courses/' + subject + '/' + catalog_number + '/schedule.json?key=' + WATERLOO_API_KEY)
    classes_json = r.json()
    if len(classes_json['data']) == 0:
        # insert blank entry for now
        DbSchedulesHelper.insert_blank_schedule_into_db(dbData, subject, catalog_number)
    else:
        for class_json in classes_json["data"]:
            if not "LEC" in class_json["section"]:
                continue
            enrollment_capacity = class_json["enrollment_capacity"]
            enrollment_total = class_json["enrollment_total"]
            start_time = ""
            end_time = ""
            days = ""
            location = ""
            instructor = ""
            if len(class_json["classes"]) > 0:
                start_time = class_json["classes"][0]["date"]["start_time"]
                end_time = class_json["classes"][0]["date"]["end_time"]
                days = class_json["classes"][0]["date"]["weekdays"]
                location = class_json["classes"][0]["location"]["building"] + class_json["classes"][0]["location"][
                    "room"]
                if len(class_json["classes"][0]["instructors"]) > 0:
                    instructor = class_json["classes"][0]["instructors"][0]
                    # print enrollment_capacity, enrollment_total, start_time, end_time, days, location, instructor

                    DbSchedulesHelper.insert_class_info_into_db(dbData, subject, catalog_number, enrollment_capacity,
                                                                enrollment_total, start_time, end_time, days, location,
                                                                instructor)


@app.route('/universe/courses/info/schedule/<subject>/<catalog_number>')
def get_class_schedule(subject, catalog_number):
    r = DbSchedulesHelper.get_schedule_from_db(dbData, subject, catalog_number)
    if len(r) == 0:
        update_classes(subject, catalog_number)
        r = DbSchedulesHelper.get_schedule_from_db(dbData, subject, catalog_number)
        if len(r) == 1:
            if r[0]["instructor"] == "":
                r = []
        return json.dumps(r)
    if r:
        if len(r) == 1:
            if r[0]["instructor"] == "":
                r = []
        return json.dumps(r)
    return "400: Something bad happened"


'''
REQUISITES
'''


def get_prereqs(subject, catalog_number):
    r = requests.get(
        WATERLOO_API + 'courses/' + subject + '/' + catalog_number + '/prerequisites.json?key=' + WATERLOO_API_KEY)
    prereq_json = r.json()

    return ReqHelper.parse_prereqs_from_json(prereq_json, subject, catalog_number)


@app.route('/universe/courses/info/prereqs/<subject>/<catalog_number>')
def get_prereq_str(subject, catalog_number):
    r = DbReqHelper.get_prereq_from_db(dbData, subject, catalog_number)
    if r and not r[0]['prereqs_desc']:
        prereqs = get_prereqs(subject, catalog_number)
        DbReqHelper.update_prereq_to_db(dbData, prereqs, subject, catalog_number)
        return json.dumps(r[0])
    if r:
        return json.dumps(r[0])
    return "400: Something bad happened"


# TODO: i know this is inconsistent, will fix later
@app.route('/universe/courses/info/meets_prereqs/<subject>/<catalog_number>')
def get_prereq_met(subject, catalog_number):
    courses = request.args.get('courses')
    get_prereq_str(subject, catalog_number)
    if courses:
        courses_list = courses.split(",")
    else:
        courses_list = []
    prereq_str = DbReqHelper.get_prereq_string_from_db(dbData, subject, catalog_number)
    prereqs_met = ReqHelper.are_prereqs_met(courses_list, prereq_str)
    return json.dumps({"result": str(prereqs_met)})


@app.route('/universe/courses/info/meets_reqs/<subject>/<catalog_number>')
def can_take_course(subject, catalog_number):
    curr_courses = request.args.get('current_courses')
    prev_courses = request.args.get('previous_courses')
    if not curr_courses:
        current_courses_list = []
    else:
        current_courses_list = curr_courses.split(",")
    if not prev_courses:
        prev_courses_list = []
    else:
        prev_courses_list = prev_courses.split(",")
    get_prereq_str(subject, catalog_number)
    get_coreq_str(subject, catalog_number)
    get_antireq_str(subject, catalog_number)

    prereq_str = DbReqHelper.get_prereq_string_from_db(dbData, subject, catalog_number)
    coreq_str = DbReqHelper.get_coreq_string_from_db(dbData, subject, catalog_number)

    both_courses = ''
    if curr_courses and prev_courses:
        both_courses = ",".join([curr_courses, prev_courses])
    elif curr_courses:
        both_courses = curr_courses
    elif prev_courses:
        both_courses = prev_courses

    #antireqs_met = ReqHelper.is_antireq_met(subject, catalog_number, both_courses)
    prereqs_met = ReqHelper.are_prereqs_met(prev_courses_list, prereq_str, current_courses_list, coreq_str)
    if prereqs_met: #and not antireqs_met:
        return json.dumps({"result": str(True)})
    return json.dumps({"result": str(False)})


'''
TODO: parse req trees to avoid string matching bugs
'''


def get_antireqs(subject, catalog_number):
    r = requests.get(
        WATERLOO_API + 'courses/' + subject + '/' + catalog_number + '.json?key=' + WATERLOO_API_KEY)
    antireq_json = r.json()
    if 'antirequisites' not in antireq_json['data'] or not antireq_json['data']['antirequisites']:
        return ''
    return antireq_json['data']['antirequisites']


@app.route('/universe/courses/info/antireqs/<subject>/<catalog_number>')
def get_antireq_str(subject, catalog_number):
    r = DbReqHelper.get_antireq_from_db(dbData, subject, catalog_number)
    if r and not r[0]['antireqs']:
        antireqs = get_antireqs(subject, catalog_number)
        DbReqHelper.update_antireq_to_db(dbData, antireqs, subject, catalog_number)
        r = DbReqHelper.get_antireq_from_db(dbData, subject, catalog_number)
        return json.dumps(r[0])
    if r:
        return json.dumps(r[0])
    return "400: Something bad happened"


@app.route('/universe/courses/info/meets_antireqs/<subject>/<catalog_number>')
def get_antireq_met(subject, catalog_number):
    courses = request.args.get('courses')
    if not courses:
        courses_list = ''
    get_antireq_str(subject, catalog_number)
    r = DbReqHelper.get_antireq_from_db(dbData, subject, catalog_number)
    # return str(r)
    antireq_str = r[0]['antireqs']
    return json.dumps({"result": str(ReqHelper.is_antireq_met(antireq_str, courses))})


def get_coreqs(subject, catalog_number):
    r = requests.get(
        WATERLOO_API + 'courses/' + subject + '/' + catalog_number + '.json?key=' + WATERLOO_API_KEY)
    coreq_json = r.json()
    if 'corequisites' not in coreq_json['data'] or not coreq_json['data']['corequisites']:
        return ''
    return coreq_json['data']['corequisites']


@app.route('/universe/courses/info/coreqs/<subject>/<catalog_number>')
def get_coreq_str(subject, catalog_number):
    r = DbReqHelper.get_coreq_from_db(dbData, subject, catalog_number)
    if r and not r[0]['coreqs']:
        coreqs = get_coreqs(subject, catalog_number)
        DbReqHelper.update_coreq_to_db(dbData, coreqs, subject, catalog_number)
        r = DbReqHelper.get_coreq_from_db(dbData, subject, catalog_number)
        return json.dumps(r[0])
    if r:
        return json.dumps(r[0])
    return "400: Something bad happened"


# TODO: i know this is inconsistent, will fix later
@app.route('/universe/courses/info/meets_coreqs/<subject>/<catalog_number>/<courses>')
def get_coreq_met(subject, catalog_number, courses):
    courses_list = courses.split(",")
    r = DbReqHelper.get_coreq_from_db(dbData, subject, catalog_number)
    coreq_str = r[0]['coreqs']
    for course in courses_list:
        # return course
        req_catalog_number = re.findall('\d+', course)[0]
        req_subject = re.findall('[A-Z]+', course)[0]
        course_str = req_subject + ' ' + req_catalog_number
        # return catalog_number, subject
        if course_str in coreq_str:
            return json.dumps({"result": str(True)})
    return json.dumps({"result": str(False)})


if __name__ == '__main__':
    app.run()
