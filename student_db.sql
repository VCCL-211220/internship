DROP DATABASE IF EXISTS students;
CREATE DATABASE students;
USE students;
CREATE TABLE student(
id INT AUTO_INCREMENT,
name VARCHAR(50),
height INT,
PRIMARY KEY (id));
INSERT INTO student(name, height)
VALUES
('Tom',175),
('Alice',168),
('Jack',182),
('Emma',165),
('James',178),
('Sophia',162),
('Michael',185),
('Olivia',170),
('Daniel',177),
('Isabella',160),
('William',181),
('Mia',166),
('Ethan',173),
('Charlotte',169),
('Alexander',188),
('Amelia',164),
('Benjamin',176),
('Harper',167),
('Lucas',180),
('Ella',163);
ALTER TABLE student ADD COLUMN age INT;
ALTER TABLE student DROP COLUMN age;
UPDATE student SET height=180 WHERE name='Tom';
INSERT INTO student(name,height)
VALUES('Kevin',175);
DELETE FROM student WHERE name='Kevin';
SELECT name FROM student;
SELECT name FROM student WHERE height>175;
SELECT name FROM student WHERE height BETWEEN 170 AND 180;
SELECT name FROM student WHERE name LIKE 'A%';
SELECT name FROM student ORDER BY height DESC LIMIT 5;
SELECT COUNT(id) FROM student WHERE height>180;
SELECT AVG(height) FROM student;
