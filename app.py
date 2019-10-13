from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import yaml

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
# Test the connection
print("Must test the connection")

DEBUG_MODE = True

@app.route('/')
def index():
    if request.method == "POST":
        details = request.form
        firstName = details['fname']
        lastName = details['lname']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO MyUsers(firstName, lastName) VALUES (%s, %s)", (firstName, lastName))
        mysql.connection.commit()
        cur.close()
        return "success"
    return render_template('index.html')

@app.route('/new/', methods=['GET', 'POST'])
def new():
    if request.method == "POST":
        details = request.form
        survey_markdown = details['survey']
        print(survey_markdown)
        cur = mysql.connection.cursor()
        cur.execute('''INSERT INTO Surveys(question_markdown) VALUES ("{0}");'''.format(survey_markdown))
        mysql.connection.commit()
        cur.close()
        return render_template('index.html')
    return render_template('create_survey.html')

@app.route('/line_chart/', methods=['GET'])
def line_chart():
    return render_template('line_chart.html')

@app.route('/bar_chart/', methods=['GET'])
def bar_chart():
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

@app.route('/xy_chart/', methods=['GET'])
def xy_chart():
    return render_template('xy_chart.html')

@app.route('/radar_chart/', methods=['GET'])
def radar_chart():
    return render_template('radar_chart.html')

if __name__ == '__main__':
    app.run(debug=DEBUG_MODE)