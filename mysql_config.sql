# TABLE SURVEY #
CREATE TABLE Surveys
(
  survey_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  question_markdown VARCHAR(2000)
);

INSERT INTO Surveys (	) 
VALUES ('Gato: Milo o Chispy'), ('Hamster: Pitagoras o Socrates');

SELECT * FROM Surveys


# TABLE QUESTIONS #
CREATE TABLE SurveyQuestions
(
  survey_id INT NOT NULL PRIMARY KEY,
  question_str VARCHAR(200),
  question_type VARCHAR(100),
  number_of_options INT
);

INSERT INTO SurveyQuestions (survey_id, question_str, question_type, number_of_options) 
VALUES (1, "Gato:", "radio", 2), (2, "Hamster", "checkbox", 2);

SELECT * FROM SurveyQuestions

# TABLE SURVEYOPTIONS #
CREATE TABLE SurveyOptions
(
  survey_id INT NOT NULL,
  option_number INT,
  option_text VARCHAR(200),
  FOREIGN KEY (survey_id) REFERENCES Surveys(survey_id),
  PRIMARY KEY(survey_id, option_number)  
);

INSERT INTO SurveyOptions (survey_id, option_number, option_text) 
VALUES (1, 1, "Milo"), (1, 2, "Chispy"), (2, 1, "Pitagoras"), (2, 2, "Socrates");

UPDATE SurveyOptions
SET option_text="Chispy" 
WHERE survey_id=1 AND option_number=2;

SELECT * FROM SurveyOptions

# TABLE SURVEY ANSWERS #
CREATE TABLE SurveyAnswers
(
  survey_id INT NOT NULL,
  option_number INT,
  survey_datetime DATETIME,
  FOREIGN KEY (survey_id) REFERENCES Surveys(survey_id)
);

INSERT INTO SurveyAnswers (survey_id, option_number, survey_datetime) 
VALUES (1, 1, "2019-10-07 21:34:44"), (1, 1, "2019-10-07 21:34:44"), (1, 2, "2019-10-07 21:34:40");

SELECT * FROM SurveyAnswers