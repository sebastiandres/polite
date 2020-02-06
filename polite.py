# Official libraries
from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import yaml

# Auxiliar files
from helpers import markdown_parser as mdp
from helpers import sql

# Parameters
config_file = 'local.yml'

# Initialize
app = Flask(__name__)

# Read the config properties
config_dict = yaml.load(open(config_file,"r"), Loader=yaml.FullLoader)
app.config['MYSQL_HOST'] = config_dict["MYSQL_HOST"]
app.config['MYSQL_USER'] = config_dict["MYSQL_USER"]
app.config['MYSQL_PASSWORD'] = config_dict["MYSQL_PASSWORD"]
app.config['MYSQL_DB'] = config_dict["MYSQL_DB"]
DEBUG_MODE = bool(config_dict["DEBUG_MODE"])

# Apply the configuration
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new/', methods=['GET', 'POST'])
def new():
    if request.method == "GET":
        return render_template('new_survey.html')
    elif request.method == "POST":
        md_dict = {"is_format_ok":False}
        while not md_dict["is_format_ok"]:
            my_answered_form = request.form
            survey_markdown = my_answered_form['survey']
            md_dict = mdp.markdown_parser(survey_markdown)
            query_fmt = """
            INSERT INTO Surveys ( markdown_str, type_str, question_str, option_1_str, option_2_str, option_3_str, option_4_str, option_5_str ) 
            VALUES ('{markdown_str}', '{type_str}', '{question_str}', '{option_1_str}', '{option_2_str}', '{option_3_str}', '{option_4_str}', '{option_5_str}');
            """
            if md_dict["is_format_ok"]:
                cur = mysql.connection.cursor()
                # Add the survey
                query = query_fmt.format(**md_dict)
                cur.execute(query)
                mysql.connection.commit()
                cur.close()
                return render_template('index.html')
            else:
                print("Wrong format")
    else:
        print(request.method)
        print("HOW THE HELL DID YOU GET HERE?")
 
@app.route('/survey/', methods=['GET', 'POST'])
@app.route('/survey/<survey_id>', methods=['GET', 'POST'])
def survey(survey_id=-1):
    last_survey_id = sql.last_survey_id(mysql)
    survey_id = int(survey_id)
    # Update to last survey id
    if (survey_id<1) or (survey_id>last_survey_id):
        survey_id = last_survey_id
    # Return the page
    if request.method == "GET":
        # Get the data for last survey
        survey_dict = sql.get_survey_data(mysql, survey_id)
        return render_template('survey.html', data=survey_dict)
    elif request.method == "POST":
        my_answered_form = request.form.to_dict()
        answer_list = eval(str(request.form)[19:-1])
        query_fmt = """
        INSERT INTO Survey_Answers ( survey_id, option_number ) 
        VALUES ({survey_id}, {option_number});
        """
        cur = mysql.connection.cursor()
        for (survey_id, option_number) in answer_list:
            query = query_fmt.format(survey_id=survey_id, option_number=option_number)
            cur.execute(query)
            mysql.connection.commit()
        cur.close()
        return render_template('index.html')
    else:
        print(request.method)
        print("HOW THE HELL DID YOU GET HERE?")

@app.route('/data/', methods=['GET'])
@app.route('/data/<survey_id>', methods=['GET'])
def data(survey_id=-1):
    last_survey_id = sql.last_survey_id(mysql)
    survey_id = int(survey_id)
    # Update to last survey id
    if (survey_id<1) or (survey_id>last_survey_id):
        survey_id = last_survey_id
    # Return the page
    if request.method == "GET":
        # Get the data for last survey
        survey_dict = sql.get_survey_data(mysql, survey_id)
        answer_df = sql.get_answers_data(mysql, survey_id)
        survey_dict["df"] = answer_df.to_html().replace("&lt;","<").replace("&gt;",">")
        return render_template('data.html', data=survey_dict)
    else:
        print(request.method)
        print("HOW THE HELL DID YOU GET HERE?")

@app.route('/bar_chart/', methods=['GET'])
@app.route('/bar_chart/<survey_id>', methods=['GET'])
def bar_chart(survey_id=-1):
    # Update to last survey id, if needed
    last_survey_id = sql.last_survey_id(mysql)
    survey_id = int(survey_id) # survey_id is a string originally
    if (survey_id<1) or (survey_id>last_survey_id):
        survey_id = last_survey_id
    # Plot the answers
    survey_dict = sql.get_survey_data(mysql, survey_id)
    count_df = sql.get_answers_count(mysql, survey_id)
    title  = survey_dict["question_str"]
    chart_data = {}
    chart_data["title"] = title + ":"
    chart_data["survey_id"] = survey_id
    chart_data["xLabel"] = "Options"
    chart_data["yLabel"] = "# Answers"
    chart_data["data.labels"] = list(count_df.index)
    chart_data["data.datasets.data"] = list(count_df.values)
    print(chart_data)
    return render_template('bar_chart.html', data=chart_data)

@app.route('/pie_chart/', methods=['GET'])
@app.route('/pie_chart/<survey_id>', methods=['GET'])
def pie_chart(survey_id=-1):
    # Update to last survey id, if needed
    last_survey_id = sql.last_survey_id(mysql)
    survey_id = int(survey_id) # survey_id is a string originally
    if (survey_id<1) or (survey_id>last_survey_id):
        survey_id = last_survey_id
    # Plot the answers
    survey_dict = sql.get_survey_data(mysql, survey_id)
    count_df = sql.get_answers_count(mysql, survey_id)
    title  = survey_dict["question_str"]
    chart_data = {}
    chart_data["title"] = title + ":"
    chart_data["survey_id"] = survey_id
    chart_data["xLabel"] = "Options"
    chart_data["yLabel"] = "# Answers"
    chart_data["data.labels"] = list(count_df.index)
    chart_data["data.datasets.data"] = list(count_df.values)
    print(chart_data)
    return render_template('pie_chart.html', data=chart_data)

if __name__ == '__main__':
    app.run(debug=DEBUG_MODE)