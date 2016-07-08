class DbReqHelper:
    @staticmethod
    def get_prereq_from_db(dbData, subject, catalog_number):
        return dbData.query_table_for_dict(
            'select prereqs_desc from courses where subject="' + subject + '" and catalog_number="' + catalog_number + '"')

    @staticmethod
    def get_prereq_string_from_db(dbData, subject, catalog_number):
        r = dbData.query_table_for_dict(
            'select * from courses where subject="' + subject + '" and catalog_number="' + catalog_number + '"')
        # return str(r)
        return r[0]['prereqs']

    @staticmethod
    def get_coreq_string_from_db(dbData, subject, catalog_number):
        r = dbData.query_table_for_dict(
            'select * from courses where subject="' + subject + '" and catalog_number="' + catalog_number + '"')
        # return str(r)
        return r[0]['coreqs']

    @staticmethod
    def update_prereq_to_db(dbData, prereqs, subject, catalog_number):
        query = 'update courses set prereqs="' + prereqs[0] + '", prereqs_desc="' + prereqs[
            1] + '" where subject="' + subject + '" and catalog_number="' + catalog_number + '"'

        dbData.execute_sql('update courses set prereqs="' + prereqs[0] + '", prereqs_desc="' + prereqs[
            1] + '" where subject="' + subject + '" and catalog_number="' + catalog_number + '"')
        r = dbData.query_table_for_dict(
            'select prereqs_desc from courses where subject="' + subject + '" and catalog_number="' + catalog_number + '"')

    @staticmethod
    def get_antireq_from_db(dbData, subject, catalog_number):
        return dbData.query_table_for_dict(
            'select antireqs from courses where subject="' + subject + '" and catalog_number="' + catalog_number + '"')

    @staticmethod
    def update_antireq_to_db(dbData, antireqs, subject, catalog_number):
        dbData.execute_sql(
            'update courses set antireqs="' + antireqs + '" where subject="' + subject + '" and catalog_number="' + catalog_number + '"')

    @staticmethod
    def get_coreq_from_db(dbData, subject, catalog_number):
        return dbData.query_table_for_dict(
            'select coreqs from courses where subject="' + subject + '" and catalog_number="' + catalog_number + '"')

    @staticmethod
    def update_coreq_to_db(dbData, coreqs, subject, catalog_number):
        dbData.execute_sql(
            'update courses set coreqs="' + coreqs + '" where subject="' + subject + '" and catalog_number="' + catalog_number + '"')

