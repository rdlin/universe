import requests
import json
import ast

WATERLOO_API = 'https://api.uwaterloo.ca/v2/'
WATERLOO_API_KEY = 'b90f031fa651186849e95363ad68b726'

def get_prereqs(subject, catalog_number):
    r = requests.get(WATERLOO_API + 'courses/' + subject + '/' + catalog_number + '/prerequisites.json?key=' + WATERLOO_API_KEY)
    prereq_json = r.json()
    if 'prerequisites_parsed' not in prereq_json['data']:
        return ("", "")
    prereqs_parsed = prereq_json['data']['prerequisites_parsed']
    prereqs_string = prereq_json['data']['prerequisites']
    #print prereqs_parsed
    prereq_list = []
    for prereq in prereqs_parsed:
        prereq_list.append(prereq)

    # cause the api is inconsistent

    if isinstance(prereq_list, list) and isinstance(prereq_list[0], int):
        prereq_list = [prereq_list]

    #print prereq_list
    #print prereqs_string
    prereq_string_list = [str(prereq) for prereq in prereq_list]
    prereq_list_string = "||".join(prereq_string_list)
    print prereq_list_string
    return prereq_list_string

def prereqs_met(courses_taken, prereq_list_string):
    #TODO: accept wildcards i.e. CS4XX

    #decode
    prereq_list_string_list = prereq_list_string.split("||")
    prereq_list = [ast.literal_eval(prereq) for prereq in prereq_list_string_list]

    # remove duplicates
    list(set(courses_taken))

    num_prereqs = 0
    for prereq in prereq_list:
        if isinstance(prereq, list):
            num_prereqs += prereq[0]
        else:
            num_prereqs += 1
    #print "num_prereqs", num_prereqs

    for course in courses_taken:
        # take first matching prerequisite
        # TODO: make this the most constrained prerequiste
        matched_req_list = [req for req in prereq_list if course in req]
        if len(matched_req_list) == 0:
            continue
        matched_req = matched_req_list[0]
        index = prereq_list.index(matched_req)
        #print "index", index
        #print "matched_req", matched_req
        if isinstance(matched_req, list):
            matched_req[0] = matched_req[0] - 1
            if matched_req[0] == 0:
                prereq_list.pop(index)
        else:
            prereq_list.pop(index)
        #print "prereq_list", prereq_list

    if len(prereq_list) == 0:
        print 'has prereqs'
        return True
    print 'no prereqs'
    return False

get_prereqs('CS', '246')
#prereqs_met(['CS136', 'PHYS275'], get_prereqs('CS', '246'))



