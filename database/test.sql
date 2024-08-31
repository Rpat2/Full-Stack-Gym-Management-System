-- Create Customers table
CREATE OR REPLACE TABLE Customers (
    customerID varchar(255) NOT NULL,
    firstName varchar(50) NOT NULL,
    lastName varchar(50) NOT NULL,
    email varchar(255) NOT NULL,
    streetAndCity varchar(255) NOT NULL,
	state varchar(2) NOT NULL,
	zipCode varchar(5) NOT NULL,
    credit int DEFAULT 1 NOT NULL,
    PRIMARY KEY (customerID)
);

-- Create Books table
CREATE OR REPLACE TABLE Books (
    bookID int NOT NULL AUTO_INCREMENT,
    bookName varchar(255) NOT NULL,
    author varchar(255),
    bookIsbn bigint NOT NULL,
    customerID varchar(255) NOT NULL,
    creditCost int NOT NULL,
    numberCopies int NOT NULL,
    PRIMARY KEY(bookID),
    FOREIGN KEY (customerID) REFERENCES Customers(customerID) ON DELETE CASCADE
);

-- For Books table, set bookID to auto-increment starting at 1000
ALTER TABLE Books AUTO_INCREMENT=1000;

-- Create ShipRates table
CREATE OR REPLACE TABLE ShipRates (
    shipRateID varchar(50) NOT NULL,
    zoneDescription varchar(255) NOT NULL,
	cost decimal(4,2) NOT NULL,
    PRIMARY KEY (shipRateID)
);

-- Create Swaps table
CREATE OR REPLACE TABLE Swaps (
    swapID int NOT NULL AUTO_INCREMENT,
	swapDate date NOT NULL,
	bookID int NOT NULL,
	shipRateID varchar(50),
	PRIMARY KEY (swapID),
	FOREIGN KEY (bookID) REFERENCES Books(bookID),
	FOREIGN KEY (shipRateID) REFERENCES ShipRates(shipRateID)
);

-- Create CustomerSwaps table (intersection table for Customers and Swaps)
CREATE OR REPLACE TABLE CustomerSwaps (
    customerSwapID int NOT NULL AUTO_INCREMENT,
	senderCustomerID varchar(255) NOT NULL,
    requesterCustomerID varchar(255) NOT NULL,
	swapID int NOT NULL,
	PRIMARY KEY (customerSwapID),
	FOREIGN KEY (senderCustomerID) REFERENCES Customers(customerID),
    FOREIGN KEY (requesterCustomerID) REFERENCES Customers(customerID),
	FOREIGN KEY (swapID) REFERENCES Swaps(swapID) ON DELETE CASCADE
);

-- For CustomerSwaps table, set customerSwapsID to auto-increment starting at 40
ALTER TABLE CustomerSwaps AUTO_INCREMENT=40;

-- Insert data into Customers table
INSERT INTO Customers (customerID, firstName, lastName, email, streetAndCity, state, zipCode, credit)
VALUES
('scollins','Susan', 'Collins', 'scollins@gmail.com', '3953 Randall Dr, Honolulu', 'HI', '96819', 1),
('janeee', 'Jane', 'Park', 'jane@hotmail.com', '8680 Pawnee Ave, Campbell', 'CA', '95008', 12),
('ggeorge98', 'George', 'Otis', 'georgeo@yahoo.com', '55 Roehampton St, Lakeville', 'MN', '55044', 2),
('mitchellbooks', 'Mitchell', 'Maxson', 'mmitchell@gmail.com', '602 E. Border St, Ladson', 'SC', '29456', 4),
('charlotte1000', 'Charlotte', 'Bronte', 'charlottebronte@icloud.com', '8949 Birch Hill Rd, Torrance', 'CA', '90505', 7);

-- Insert data into Books table
INSERT INTO Books (bookName, author, bookIsbn, customerID, creditCost, numberCopies)
VALUES
('To Kill a Mockingbird', 'Harper Lee', 9780060935467, 'ggeorge98', 1, 1),
('The Great Gatsby', 'F. Scott Fitzgerald', 9780684801520, 'janeee', 2, 1),
('The Alchemist', 'Paulo Coelho', 9780062315007, 'mitchellbooks', 1, 1),
('Pride and Prejudice', 'Jane Austen', 9781908533050, 'charlotte1000', 1, 1),
('The Little Prince', 'Antoine de Saint-Exupéry', 9781461190462, 'scollins', 3, 1);

-- Insert data into ShipRates table
INSERT INTO ShipRates (shipRateID, zoneDescription, cost)
VALUES
('sameState', 'Same State', 2.99),
('mainlandUsa', 'Mainland USA', 4.99),
('alaskaOrHawaii', 'Alaska or Hawaii', 6.99);

-- Insert data into CustomerSwaps table
INSERT INTO CustomerSwaps (senderCustomerID, requesterCustomerID, swapID)
VALUES
('ggeorge98', 'scollins', 1),
('scollins', 'mitchellbooks', 2),
('charlotte1000', 'janeee', 3),
('mitchellbooks', 'ggeorge98', 4),
('janeee', 'charlotte1000', 5);

-- Insert data into Swaps table
INSERT INTO Swaps (swapDate, bookID, shipRateID)
VALUES
('2024-04-30', 1000, 'alaskaOrHawaii'),
('2024-02-15', 1004, 'alaskaOrHawaii'),
('2023-12-30', 1003, 'sameState'),
('2023-03-09', 1002, 'mainlandUsa'),
('2024-04-12', 1001, 'sameState');
