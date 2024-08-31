----

SET FOREIGN_KEY_CHECKS = 0;
SET AUTOCOMMIT = 0;


-- Create the Memberships Table

CREATE OR REPLACE TABLE Memberships(
    memID INT NOT NULL AUTO_INCREMENT, 
    tier varchar(45) NOT NULL, 
    length INT NOT NULL,
    cost DEC(5,2) NOT NULL,
    PRIMARY KEY (memID)
);


-- Create the Customers Table

CREATE OR REPLACE TABLE Customers (
    customerID INT NOT NULL AUTO_INCREMENT, 
    firstName varchar(45) NOT NULL,
    lastName varchar(45) NOT NULL, 
    email varchar(45) NOT NULL,
    phone varchar(45) NOT NULL, 
    memID INT, 
    FOREIGN KEY (memID) REFERENCES Memberships(memID) ON DELETE SET NULL,
    PRIMARY KEY (customerID)
);


-- Create the Gyms Table

CREATE OR REPLACE TABLE Gyms ( 
    gymID INT NOT NULL AUTO_INCREMENT,
    address varchar(45) NOT NULL, 
    phone varchar(45) NOT NULL,
    manager varchar(45) NOT NULL, 
    PRIMARY KEY (gymID)
);


-- Create the Trainers Table

CREATE OR REPLACE TABLE Trainers(
    trainerID INT NOT NULL AUTO_INCREMENT,  
    firstName varchar(45) NOT NULL,
    lastName varchar(45) NOT NULL,
    specialistType varchar(45) NOT NULL,
    level varchar(45) NOT NULL,
    gymID INT NOT NULL,
    FOREIGN KEY (gymID) REFERENCES Gyms(gymID) ON DELETE CASCADE,
    PRIMARY KEY (trainerID)
);


-- Create the Classes Table

CREATE OR REPLACE TABLE Classes (
    classID INT NOT NULL AUTO_INCREMENT, 
    type varchar(45) NOT NULL, 
    classDate DATE NOT NULL,
    classTime TIME NOT NULL,
    cost DEC(5,2) NOT NULL,
    level varchar(45) NOT NULL, 
    trainerID INT NOT NULL,
    gymID INT NOT NULL, 
    FOREIGN KEY (trainerID) REFERENCES Trainers(trainerID) ON DELETE CASCADE,
    FOREIGN KEY (gymID) REFERENCES Gyms(gymID) ON DELETE CASCADE, 
    PRIMARY KEY (classID)
);


-- Create the CustomerClasses Table

CREATE OR REPLACE TABLE CustomerClasses ( 
    customerclassID INT NOT NULL AUTO_INCREMENT,
    customerID INT NOT NULL, 
    classID INT NOT NULL, 
    FOREIGN KEY (customerID) REFERENCES Customers(customerID) ON DELETE CASCADE,
    FOREIGN KEY (classID) REFERENCES Classes(classID) ON DELETE CASCADE,
    PRIMARY KEY (customerclassID)
);


-- Insert data into Memberships Table
INSERT INTO Memberships (tier, length, cost)
VALUES ("Bronze", 1, 15.00),
       ("Silver", 3, 40.00),
       ("Gold", 6, 85.00),
       ("Platinum", 12, 160.00);


-- Insert data into Gyms Table
INSERT INTO Gyms (address, phone, manager)
VALUES ("100 MadeUpStreet GainsVille OR 12343", "503-232-4243", "Roshan Patel"),
       ("130 WheyStreet ProteinsVille OR 12343", "503-124-1234", "Kishan Pedal"),
       ("225 VitaminStreet RunsVille OR 12343", "503-184-4312", "Sarah Yeswalk");


-- Insert data into Trainers table
INSERT INTO Trainers(firstName, lastName, specialistType, level, gymID)
VALUES ("Bruce", "Wayne", "Weightlifting", "Advanced", 1),
       ("Clark", "Kent", "Weightlifting", "Intermediate", 1),
       ("Hal", "Jordan", "Weightlifting", "Beginner", 2),
       ("Diana", "Prince", "Crossfit", "Advanced", 1),
       ("Selina", "Kyle", "Crossfit", "Intermediate", 1),
       ("Kara", "Kent", "Crossfit", "Beginner", 1),
       ("Jason", "Todd", "Boxing", "Advanced", 1),
       ("Tim", "Drake", "HITT", "Beginner", 1);


-- Insert data into Classes table
INSERT INTO Classes(type, classDate, classTime, cost, level, trainerID, gymID)
VALUES ("Weightlifting", "2024-02-10", "14:40:00", 20.00, "Intermediate", (Select trainerID from Trainers WHERE specialistType = "Weightlifting" and level = "Intermediate" and gymID = 1), 1),
       ("Weightlifting", "2024-02-10", "15:23:00", 20.00, "Beginner", (Select trainerID from Trainers WHERE specialistType = "Weightlifting" and level = "Beginner" and gymID = 2), 2),
       ("Weightlifting", "2024-02-10", "14:37:00", 30.00, "Advanced", (Select trainerID from Trainers WHERE specialistType = "Weightlifting" and level = "Advanced" and gymID = 1), 1),
       ("Boxing", "2024-02-11", "15:40:00", 30.00, "Advanced", (Select trainerID from Trainers WHERE specialistType = "Boxing" and level = "Advanced" and gymID = 1), 1),
       ("Crossfit", "2024-02-12", "13:00:00", 25.00, "Intermediate", (Select trainerID from Trainers WHERE specialistType = "Crossfit" and level = "Intermediate" and gymID = 1), 1);


-- Insert data into Customers table
INSERT INTO Customers (firstName, lastName, email, phone, memID)
VALUES ("Rohan", "Patel", "random@gmail.com", "503-865-2352", 4),
       ("Lori", "Greiner", "shark@gmail.com", "503-123-3212", 1),
       ("Mark", "Cuban", "dolphin@gmail.com", "503-322-9787", 2),
       ("Kevin", "OLeary", "squid@gmail.com","503-689-1243", 3),
       ("Barbara", "Corcoran", "penguin@gmail.com", "503-658-2341", 1);


       


-- Insert data into CustomerClasses table
INSERT INTO CustomerClasses(customerID, classID)
VALUES (2, 3),
       (2, 4),
       (1, 2),
       (3, 5),
       (3, 4);

SET FOREIGN_KEY_CHECKS = 1;
COMMIT;