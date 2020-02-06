# Polite: A "Poll Lite" system to take surveys.

This repository is hosted at github: https://www.github.com/sebastiandres/surveys_with_flask_and_xkcd_charts

## About the project
This minimally working survey system was created for pycon Colombia 2020, for the talk (in spanish).
It is inspired in the "xkcd philosophy", that can be parephrased as "why doing things simple when you can do it
all by yourself and learn in the process". 

Is a "all free" polling system, built in python, html and sql with the following tools:
* python: flask, flask_mysqldb, pandas
* html: some css and html by hand. xkcd.otf font from XYZ and xkcd_chart javascript library from XYZ. 
* sql: mysql.

## Some links
* https://timqian.com/chart.xkcd/: The charts as xkcd 
* The xkcd font [xkcd.otf]() is a copy of the font provided by XYZ at the repo https://github.com/ivanov/xkcd-font/blob/master/xkcd.otf.
*The xkcd javascript chart library, xkcd_chart.jss is a copy of the librery provided by XYZ at the repo.
* The font and javascript are included to reduce the external dependencies. Copyright (and awesomeness) belongs to the original creators. 

## Installation
The required libraries can be installed using conda, with the provided xyz.yaml file:
```
conda install yaml
```
To activate the environment, use source/conda as usual
```
source activate polite
```

To run in local, you'll need to install mysql, and run the commands at mysql_config.sql. 
It should create two tables:
surveys( columns_here)
survey_answers (columns)

## Execution
After all that, you should be able to run the app:
```
python polite.py
```

## Test
You can test a working (freely!) version at sebastiandres.pythoneverywhere.com/