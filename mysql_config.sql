###################
# CREATE DATABASE #
###################
CREATE DATABASE SURVEY_LITE;
USE SURVEY_LITE;

################
# TABLE SURVEY #
################
CREATE TABLE Surveys
(
  survey_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  markdown_str VARCHAR(2000) NOT NULL,
  type_str VARCHAR(2000) NOT NULL,
  question_str VARCHAR(2000) NOT NULL,
  option_1_str VARCHAR(2000) NOT NULL,
  option_2_str VARCHAR(2000) NOT NULL,
  option_3_str VARCHAR(2000),
  option_4_str VARCHAR(2000),
  option_5_str VARCHAR(2000),
  creation_date DATETIME DEFAULT NOW()
);

INSERT INTO surveys ( markdown_str, type_str, question_str, option_1_str,	option_2_str ) 
VALUES ('Gato: * Milo * Chispy', 'single', 'Gato', 'Milo', 'Chispy'); 


INSERT INTO surveys ( markdown_str, type_str, question_str, option_1_str, option_2_str, option_3_str, option_4_str, option_5_str ) 
VALUES ('Hamster: v Pitagoras v Socrates v Aristoteles v Platon v Dexter', 'multiple', "Hamster", "Pitagoras", "Socrates", "Aristoteles", "Platon", "Dexter");
      
SELECT * FROM Surveys

########################
# TABLE SURVEY ANSWERS #
########################

CREATE TABLE survey_answers
(
  survey_id INT NOT NULL,
  option_number INT NOT NULL,
  survey_datetime DATETIME DEFAULT NOW(),
  FOREIGN KEY (survey_id) REFERENCES Surveys(survey_id)
);

INSERT INTO survey_answers (survey_id, option_number) 
VALUES (1, 1), (2, 2);

INSERT INTO survey_answers (survey_id, option_number, survey_datetime) 
VALUES (1, 1, "2019-10-07 21:34:44"), (1, 1, "2019-10-07 21:34:44"), (1, 2, "2019-10-07 21:34:40");

select * from survey_answers