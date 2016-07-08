class DbProgramFacultyHelper():
    @staticmethod
    def get_faculty_list_from_db(dbData):
        return dbData.get_list_from_table_json('select distinct faculty from programs', lambda x: str(x['faculty'][11:]))

    @staticmethod
    def get_program_list_from_db(dbData):
        return dbData.get_list_from_table_json('select * from programs', lambda x: str(x['program']))