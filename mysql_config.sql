###################
# CREATE DATABASE #
###################
CREATE DATABASE POLITE;
USE POLITE;

################
# TABLE SURVEY #
################
CREATE TABLE surveys
(
  survey_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  markdown_str VARCHAR(2000) NOT NULL,
  type_str VARCHAR(2000) NOT NULL,
  question_str VARCHAR(2000) NOT NULL,
  option_1_str VARCHAR(2000) NOT NULL,
  option_2_str VARCHAR(2000),
  option_3_str VARCHAR(2000),
  option_4_str VARCHAR(2000),
  option_5_str VARCHAR(2000),
  question_datetime DATETIME DEFAULT NOW()
);

INSERT INTO surveys ( markdown_str, type_str, question_str, option_1_str,	option_2_str ) 
VALUES ('¿Qué fue primero?: * El huevo * La gallina', 'radio', '¿Qué fue primero?', 'El huevo', 'La gallina'); 

INSERT INTO surveys ( markdown_str, type_str, 
                      question_str, option_1_str, option_2_str, option_3_str, option_4_str, option_5_str, question_datetime ) 
VALUES ('¿Cuál es la mejor mascota?: v Perro v Gato v Pitón v Otra', 'checkbox', 
        "¿Cuál es la mejor mascota?", "Perro", "Gato", "Pitón", "Otra", "", "2020-01-01 00:00:01");
      
SELECT * FROM surveys;

########################
# TABLE SURVEY ANSWERS #
########################

CREATE TABLE survey_answers
(
  survey_id INT NOT NULL,
  option_number INT NOT NULL,
  answer_datetime DATETIME DEFAULT NOW(),
  FOREIGN KEY (survey_id) REFERENCES surveys(survey_id)
);

INSERT INTO survey_answers (survey_id, option_number) 
VALUES (1, 2), (1, 1), (1, 1), (1, 2), (1, 2), (1, 2), (1, 2);

INSERT INTO survey_answers (survey_id, option_number, answer_datetime) 
VALUES (2, 1, "2020-01-01 00:01:01"),
       (2, 2, "2020-01-01 00:01:01"),
       (2, 4, "2020-01-01 00:01:01"),
       (2, 3, "2020-01-01 00:01:01"),
       (2, 3, "2020-01-01 00:01:01"),
       (2, 3, "2020-01-01 00:01:01"),
       (2, 3, "2020-01-01 00:01:01"),
       (2, 3, "2020-01-01 00:01:01"),
       (2, 3, "2020-01-01 00:01:01"),
       (2, 3, "2020-01-01 00:01:01"),
       (2, 3, "2020-01-01 00:01:01");

select * from survey_answers;