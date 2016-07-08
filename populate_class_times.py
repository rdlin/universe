import requests
import json
import ast

WATERLOO_API = 'https://api.uwaterloo.ca/v2/'
WATERLOO_API_KEY = 'b90f031fa651186849e95363ad68b726'

def get_classes(subject, catalog_number):
    r = requests.get(WATERLOO_API + 'courses/' + subject + '/' + catalog_number + '/schedule.json?key=' + WATERLOO_API_KEY)
    classes_json = r.json()
    if len(classes_json['data']) == 0:
        print str(json.dumps({}))
        return json.dumps({})
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
                location = class_json["classes"][0]["location"]["building"] + class_json["classes"][0]["location"]["room"]
                if len(class_json["classes"][0]["instructors"]) > 0:
                    instructor = class_json["classes"][0]["instructors"][0]
            print enrollment_capacity, enrollment_total, start_time, end_time, days, location, instructor

get_classes('CS', '136')