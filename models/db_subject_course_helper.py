class DbSubjectCourseHelper():
    @staticmethod
    def get_subject_list_from_db(dbData):
        return dbData.get_list_from_table_json('select * from subjects', lambda x: x['subject'])

    @staticmethod
    def get_course_list_from_db(dbData):
        return dbData.get_list_from_table_json('select * from courses',
                                        lambda x: str(x['subject']) + str(x['catalog_number']))

    @staticmethod
    def get_course_list_by_subject_from_db(dbData, subject):
        return dbData.get_list_from_table_json('select * from courses where subject="' + subject + '"',
                                               lambda x: str(x['subject']) + str(x['catalog_number']))

    @staticmethod
    def get_course_info_from_db(dbData, subject, catalog_number):
        return dbData.query_table_for_dict(
            'select * from courses where subject="' + subject + '" and catalog_number="' + catalog_number + '"')
