class DbSchedulesHelper():
    @staticmethod
    def insert_blank_schedule_into_db(dbData, subject, catalog_number):
        dbData.execute_sql(
            'insert into courses_classes (subject, catalog_number, enrollment_capacity, enrollment_total, start_time, end_time, days, location, instructor) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)' % (
                '"' + str(subject) + '"', '"' + str(catalog_number) + '"', '""', '""', '""', '""', '""', '""', '""'))

    @staticmethod
    def insert_class_info_into_db(dbData, subject, catalog_number, enrollment_capacity, enrollment_total, start_time, end_time, days, location, instructor):
        dbData.execute_sql(
            'insert into courses_classes (subject, catalog_number, enrollment_capacity, enrollment_total, start_time, end_time, days, location, instructor) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)' % (
                '"' + str(subject) + '"', '"' + str(catalog_number) + '"',
                '"' + str(enrollment_capacity) + '"', '"' + str(enrollment_total) + '"',
                '"' + str(start_time) + '"',
                '"' + str(end_time) + '"', '"' + str(days) + '"', '"' + str(location) + '"',
                '"' + str(instructor) + '"'))

    @staticmethod
    def get_schedule_from_db(dbData, subject, catalog_number):
        return dbData.query_table_for_dict(
            'select * from courses_classes where subject="' + subject + '" and catalog_number="' + catalog_number + '"')

