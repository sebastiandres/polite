from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

# Read the config properties
config_file = 'local.yml'
config_dict = yaml.load(open(config_file,"r"), Loader=yaml.FullLoader)
app.config['MYSQL_HOST'] = config_dict["MYSQL_HOST"]
app.config['MYSQL_USER'] = config_dict["MYSQL_HOST"]
app.config['MYSQL_PASSWORD'] = config_dict["MYSQL_HOST"]
app.config['MYSQL_DB'] = config_dict["MYSQL_HOST"]
debug_mode = bool(config_dict["DEBUG_MODE"])

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
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
    return render_template('bar_chart.html')

@app.route('/xy_chart/', methods=['GET'])
def xy_chart():
    return render_template('xy_chart.html')

@app.route('/radar_chart/', methods=['GET'])
def radar_chart():
    return render_template('radar_chart.html')

if __name__ == '__main__':
    app.run(debug=True)