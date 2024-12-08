-- Step 1: Create the database 
create  DATABASE  sports_meeting_db;
USE sports_meeting_db;

-- Step 2: Create tables

-- Create STUDENT table
CREATE TABLE STUDENT (
    sid INT AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(50),
    nationality VARCHAR(50),
    dateofbirth DATE
);

-- Create SPORTSMEETING table
CREATE TABLE SPORTSMEETING (
    smid INT AUTO_INCREMENT PRIMARY KEY,
    meetingname VARCHAR(100),
    startdate DATE,
    enddate DATE
);

-- Create SCHOOL table
CREATE TABLE SCHOOL (
    schoolid INT AUTO_INCREMENT PRIMARY KEY,
    schoolname VARCHAR(100)
);

-- Create SCHOOLSPORTSMEETING table
CREATE TABLE SCHOOLSPORTSMEETING (
    schoolid INT,
    smid INT,
    PRIMARY KEY (schoolid, smid),
    FOREIGN KEY (schoolid) REFERENCES SCHOOL(schoolid) ON DELETE CASCADE,
    FOREIGN KEY (smid) REFERENCES SPORTSMEETING(smid) ON DELETE CASCADE
);

CREATE TABLE EVENT (
    eventid INT AUTO_INCREMENT PRIMARY KEY,
    eventname VARCHAR(100),
    smid INT,
    startdate DATE,  -- Added startdate column with DATE type
    enddate DATE,    -- Added enddate column with DATE type
    FOREIGN KEY (smid) REFERENCES SPORTSMEETING(smid) ON DELETE CASCADE
);


-- Create JUDGE table
CREATE TABLE JUDGE (
    jid INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phonenumber VARCHAR(20)
);

-- Create MATCH table
CREATE TABLE `MATCH` (
    matchid INT AUTO_INCREMENT PRIMARY KEY,
    matchdate DATE,
    eventid INT,
    jid INT,
    smid INT,
    FOREIGN KEY (eventid) REFERENCES EVENT(eventid) ON DELETE CASCADE,
    FOREIGN KEY (jid) REFERENCES JUDGE(jid) ON DELETE CASCADE,
    FOREIGN KEY (smid) REFERENCES SPORTSMEETING(smid) ON DELETE CASCADE
);

-- Create RECORD table
CREATE TABLE `RECORD` (
    sid INT,
    matchid INT,
    record DECIMAL(10,2),
    `rank` INT,
    PRIMARY KEY (sid, matchid),
    FOREIGN KEY (sid) REFERENCES STUDENT(sid) ON DELETE CASCADE,
    FOREIGN KEY (matchid) REFERENCES `MATCH`(matchid) ON DELETE CASCADE
);

-- Create SUSPEND table
CREATE TABLE SUSPEND (
    suspendid INT AUTO_INCREMENT PRIMARY KEY,
    sid INT,
    details VARCHAR(255),
    startdate DATE,
    enddate DATE,
    FOREIGN KEY (sid) REFERENCES STUDENT(sid) ON DELETE CASCADE
);

-- Insert records into STUDENT table
INSERT INTO STUDENT (firstname, nationality, dateofbirth) VALUES
('John', 'American', '2001-05-15'),
('Emily', 'Canadian', '2002-06-10'),
('Michael', 'British', '2000-03-21'),
('Sophia', 'Australian', '1999-11-30'),
('James', 'German', '2001-09-25');

-- Insert records into SPORTSMEETING table
INSERT INTO SPORTSMEETING (meetingname, startdate, enddate) VALUES
('Summer Sports Championship', '2024-06-01', '2024-06-05'),
('Winter Sports Festival', '2024-12-10', '2024-12-15'),
('Spring Invitational', '2025-03-01', '2025-03-05'),
('Autumn Classic', '2024-09-15', '2024-09-20'),
('Global Sports Meet', '2025-07-10', '2025-07-15');

-- Insert records into SCHOOL table
INSERT INTO SCHOOL (schoolname) VALUES
('Springfield High School'),
('Greenwich International School'),
('Riverwood Academy'),
('Lakeside Preparatory School'),
('Mountain View High School');

-- Insert records into SCHOOLSPORTSMEETING table
INSERT INTO SCHOOLSPORTSMEETING (schoolid, smid) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5);

-- Insert records into EVENT table
INSERT INTO EVENT (eventname, smid, startdate, enddate) VALUES
('100m Sprint', 1, '2024-06-01', '2024-06-01'),
('Long Jump', 2, '2024-12-11', '2024-12-11'),
('Basketball Tournament', 3, '2025-03-02', '2025-03-03'),
('Football Match', 4, '2024-09-16', '2024-09-16'),
('Tennis Championship', 5, '2025-07-11', '2025-07-12');

-- Insert records into JUDGE table
INSERT INTO JUDGE (name, email, phonenumber) VALUES
('Alice Johnson', 'alice.johnson@example.com', '555-1234'),
('Bob Williams', 'bob.williams@example.com', '555-5678'),
('Charlie Brown', 'charlie.brown@example.com', '555-8765'),
('Diana Green', 'diana.green@example.com', '555-4321'),
('Eva White', 'eva.white@example.com', '555-3456');

-- Insert records into MATCH table
INSERT INTO `MATCH` (matchdate, eventid, jid, smid) VALUES
('2024-06-01', 1, 1, 1),
('2024-12-11', 2, 2, 2),
('2025-03-02', 3, 3, 3),
('2024-09-16', 4, 4, 4),
('2025-07-11', 5, 5, 5);

-- Insert records into RECORD table
INSERT INTO `RECORD` (sid, matchid, record, `rank`) VALUES
(1, 1, 10.15, 1),
(2, 2, 7.80, 2),
(3, 3, 25.40, 3),
(4, 4, 15.20, 4),
(5, 5, 12.45, 5);

-- Insert records into SUSPEND table
INSERT INTO SUSPEND (sid, details, startdate, enddate) VALUES
(1, 'Injury during match', '2024-06-01', '2024-06-10'),
(2, 'Unsportsmanlike conduct', '2024-12-10', '2024-12-15'),
(3, 'Violation of rules', '2025-03-01', '2025-03-05'),
(4, 'Disqualification for unfair play', '2024-09-15', '2024-09-20'),
(5, 'Unacceptable behavior during event', '2025-07-10', '2025-07-15');
