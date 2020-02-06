# Database structures:
# surveys ( survey_id, markdown_str, type_str, question_str, option_1_str, option_2_str, option_3_str, option_4_str, option_5_str, creation_date )
# survey_answers ( survey_id, option_number, survey_datetime )

import pandas as pd

def last_survey_id(mysql):
    """
    """
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT max(survey_id) FROM surveys')
    value = list(cursor)[0][0]
    print(value)
    return value

def get_survey_data(mysql, survey_id):
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

def get_answers_data(mysql, survey_id):
    """
    """
    # Get the question and options text strings
    survey_dict = get_survey_data(mysql, survey_id)
    # Get the answers
    #from IPython import embed; embed()
    column_list = ["survey_id", "option_number"]
    query_fmt = 'SELECT {column_list} FROM survey_answers WHERE survey_id={survey_id}'
    query = query_fmt.format(column_list=", ".join(column_list), survey_id=survey_id)
    print(query)
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    data = list(cursor)
    answer_df = pd.DataFrame(columns=column_list, data=data)
    # Add a column with the reponse
    def get_answer_str(option_number):
        key = "option_{0}_str".format(option_number)
        return survey_dict[key]
    answer_df["answer_str"] = answer_df["option_number"].apply(get_answer_str)
    # Return the answer
    print(answer_df)
    return answer_df

def get_answers_count(mysql, survey_id):
    """
    """
    answer_df = get_answers_data(mysql, survey_id)
    count_df = answer_df["answer_str"].value_counts()
    return count_df

