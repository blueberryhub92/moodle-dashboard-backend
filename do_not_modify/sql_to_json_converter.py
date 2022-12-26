class SQLToJSONConverter:
    # noinspection PyMethodMayBeStatic
    def convert_to_json(self, sql_result, sql_cursor) -> list:
        columns = list(map(lambda x: x[0], sql_cursor.description))
        json_result = []
        for entry in sql_result:
            json_object = {}
            for (index, column) in enumerate(columns):
                json_object[column] = entry[index]
            json_result.append(json_object)
        return json_result