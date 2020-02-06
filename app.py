# Official libraries
from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import yaml

# Auxiliar files
from helpers import markdown_parser as mdp
from helpers import counting

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
        my_answered_form = request.form
        print(my_answered_form)
        survey_markdown = my_answered_form['survey']
        print(survey_markdown)
        md_dict = mdp.markdown_parser(survey_markdown)
        print(md_dict)
        query_fmt = """
        INSERT INTO Surveys ( markdown_str, type_str, question_str, option_1_str, option_2_str, option_3_str, option_4_str, option_5_str ) 
        VALUES ('{markdown_str}', '{type_str}', '{question_str}', '{option_1_str}', '{option_2_str}', '{option_3_str}', '{option_4_str}', '{option_5_str}');
        """
        if md_dict["is_format_ok"]:
            cur = mysql.connection.cursor()
            # Add the survey
            query = query_fmt.format(**md_dict)
            print(query)
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
    last_survey_id = counting.last(mysql)
    survey_id = int(survey_id)
    # Update to last survey id
    if (survey_id<1) or (survey_id>last_survey_id):
        survey_id = last_survey_id
    # Return the page
    if request.method == "GET":
        # Get the data for last survey
        survey_dict = counting.get_survey(mysql, survey_id)
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
            print(query)
            cur.execute(query)
            mysql.connection.commit()
        cur.close()
        return render_template('index.html')
    else:
        print(request.method)
        print("HOW THE HELL DID YOU GET HERE?")

@app.route('/bar_chart/', methods=['GET'])
@app.route('/bar_chart/<survey_id>', methods=['GET'])
def bar_chart(survey_id=-1):
    last_survey_id = counting.last()
    survey_id = int(survey_id)
    # Update to last survey id
    if (survey_id<1) or (survey_id>last_survey_id):
        survey_id = last_survey_id
    # Plot the answers
    survey_answers = {"Pregunta 1":10, "Pregunta 2":20, "Pregunta 3":30}
    cur = mysql.connection.cursor()
    cur.execute("SELECT question_str FROM surveyQuestions WHERE survey_id=1")
    mysql_data = cur.fetchall()
    print(type(mysql_data), mysql_data)
    title  = mysql_data[0][0]
    chart_data = {}
    chart_data["title"] = title
    chart_data["xLabel"] = "Opciones"
    chart_data["yLabel"] = "Número de Respuestas"
    chart_data["data.labels"] = ["Opcion 1", "Opcion 2", "Opcion 3"]
    chart_data["data.datasets.data"] = [2, 4, 6]
    return render_template('bar_chart.html', data=chart_data)

    
if __name__ == '__main__':
    app.run(debug=DEBUG_MODE)