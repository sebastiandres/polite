# Surveys ( markdown_str, type_str, question_str, option_1_str, option_2_str, option_3_str, option_4_str, option_5_str )
def last(mysql):
    """
    """
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT max(survey_id) FROM surveys')
    value = list(cursor)[0][0]
    print(value)
    return value

def get_survey(mysql, survey_id):
    """
    """
    column_list = ["survey_id", "type_str", "question_str", "option_1_str", "option_2_str", "option_3_str", "option_4_str", "option_5_str"]
    query_fmt = 'SELECT {column_list} FROM surveys where survey_id={survey_id}'
    query = query_fmt.format(column_list=", ".join(column_list), survey_id=survey_id)
    print(query)
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    survey_dict = dict(zip(column_list, list(cursor)[0]))
    print(survey_dict)
    return survey_dict
