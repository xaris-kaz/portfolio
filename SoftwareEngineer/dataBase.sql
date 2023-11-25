drop database if exists diploma_projects_app;
create database diploma_projects_app;
use diploma_projects_app;

CREATE TABLE users (
   id  int NOT NULL AUTO_INCREMENT,
   user_name  text DEFAULT NULL,
   password  text DEFAULT NULL,
   role  text DEFAULT NULL,
  PRIMARY KEY ( id )
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

create table professors(
   id  int NOT NULL AUTO_INCREMENT,
   full_name text DEFAULT NULL,
   specialty text DEFAULT NULL,
   user_name text DEFAULT NULL,
   PRIMARY KEY(id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

create table students(
   id  int NOT NULL AUTO_INCREMENT,
   full_name text DEFAULT NULL,
   year_of_studies int DEFAULT NULL,
   curent_average_grade double DEFAULT NULL,
   remaining_courses int DEFAULT NULL,
   user_name text DEFAULT NULL,
   PRIMARY KEY(id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;


create table subjects(
   id  int NOT NULL AUTO_INCREMENT,
   title text DEFAULT NULL,
   objectives text DEFAULT NULL,
   professor_id  int NOT NULL,
   PRIMARY KEY(id),
   FOREIGN KEY (professor_id) REFERENCES professors(id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

create table thesis(
   id  int NOT NULL AUTO_INCREMENT,
   implementation_grade double DEFAULT NULL,
   report_grade double DEFAULT NULL,
   presentation_grade double DEFAULT NULL,
   total_grade double DEFAULT NULL,
   professor_id  int NOT NULL,
   subject_id  int NOT NULL,
   student_id  int NOT NULL,
   PRIMARY KEY(id),
   FOREIGN KEY (professor_id) REFERENCES professors(id),
   FOREIGN KEY (student_id) REFERENCES students(id),
   FOREIGN KEY (subject_id) REFERENCES subjects(id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;




create table applications(
   id  int NOT NULL AUTO_INCREMENT,
   student_id int,
   subject_id  int NOT NULL,
   PRIMARY KEY(id),
   FOREIGN KEY (student_id) REFERENCES students(id),
   FOREIGN KEY (subject_id) REFERENCES subjects(id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;


