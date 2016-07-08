import ast
import re

class ReqHelper:
    @staticmethod
    def are_prereqs_met(previous_courses_taken, prereq_list_string, current_courses_taken=[], coreq_string=''):
        # TODO: accept wildcards i.e. CS4XX

        if prereq_list_string == "":
            return True

        # decode
        prereq_list_string_list = prereq_list_string.split("||")
        prereq_list = [ast.literal_eval(prereq) for prereq in prereq_list_string_list]

        num_prereqs = 0
        for prereq in prereq_list:
            if isinstance(prereq, list):
                num_prereqs += prereq[0]
            else:
                num_prereqs += 1
        # print "num_prereqs", num_prereqs

        if coreq_string:
            if current_courses_taken:
                for course in current_courses_taken:
                    req_catalog_number = re.findall('\d+', course)[0]
                    req_subject = re.findall('[A-Z]+', course)[0]
                    course_str = req_subject + ' ' + req_catalog_number
                    # return catalog_number, subject
                    if course_str in coreq_string:
                        previous_courses_taken.append(course)

        # remove duplicates
        previous_courses_taken = list(set(previous_courses_taken))

        for course in previous_courses_taken:
            # take first matching prerequisite
            # TODO: make this the most constrained prerequiste
            matched_req_list = [req for req in prereq_list if course in req]
            if len(matched_req_list) == 0:
                continue
            matched_req = matched_req_list[0]
            index = prereq_list.index(matched_req)
            # print "index", index
            # print "matched_req", matched_req
            if isinstance(matched_req, list):
                matched_req[0] = matched_req[0] - 1
                if matched_req[0] == 0:
                    prereq_list.pop(index)
            else:
                prereq_list.pop(index)
                # print "prereq_list", prereq_list

        if len(prereq_list) == 0:
            print 'has prereqs'
            return True
        print 'no prereqs'
        return False

    @staticmethod
    def parse_prereqs_from_json(prereq_json, subject, catalog_number):
        if 'prerequisites_parsed' not in prereq_json['data']:
            return ('', '')
        prereqs_parsed = prereq_json['data']['prerequisites_parsed']
        prereqs_string = prereq_json['data']['prerequisites']
        # print prereqs_parsed
        prereq_list = []
        for prereq in prereqs_parsed:
            prereq_list.append(prereq)

        # cause the api is inconsistent

        if isinstance(prereq_list, list) and isinstance(prereq_list[0], int):
            prereq_list = [prereq_list]

        # print prereq_list
        # print prereqs_string

        # for single reqs
        temp_prereq_list = []
        for req in prereq_list:
            if not isinstance(req, list):
                temp_prereq_list.append([1, req])
            else:
                temp_prereq_list.append(req)
        prereq_list = temp_prereq_list

        prereq_string_list = [str(prereq) for prereq in prereq_list]
        prereq_list_string = "||".join(prereq_string_list)
        print prereq_list_string

        return (prereq_list_string, prereqs_string)

    @staticmethod
    def is_antireq_met(antireq_str, courses):
        if courses == '':
            return False
        courses_list = courses.split(",")
        for course in courses_list:
            # return course
            req_catalog_number = re.findall('\d+', course)[0]
            req_subject = re.findall('[A-Z]+', course)[0]
            course_str = req_subject + ' ' + req_catalog_number
            # return catalog_number, subject
            if course_str in antireq_str:
                return True
        return False