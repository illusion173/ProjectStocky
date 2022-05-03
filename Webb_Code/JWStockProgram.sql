-- Begin Program
DROP DATABASE IF EXISTS stockDataBase;
CREATE DATABASE IF NOT EXISTS stockDataBase;
use stockDataBase;
-- Create Tables
CREATE TABLE IF NOT EXISTS stockData(
  stockDate DATE,
  stockName VARCHAR(30),
  stockTicker VARCHAR(10),
  RSI DOUBLE,
  MACD DOUBLE,
  stochasticOperator DOUBLE,
  Volume DOUBLE,
  Price DOUBLE,
  PriceChange DOUBLE,
  PRIMARY KEY(stockName, stockTicker, stockDate)
);

CREATE TABLE IF NOT EXISTS userTable(
  phoneNumber VARCHAR(30),
  EmailAddress VARCHAR(60),
  FirstName VARCHAR(30),
  LastName VARCHAR(30),
  USERID INTEGER,
  PRIMARY KEY(USERID)
);

CREATE TABLE IF NOT EXISTS LoginTable(
  LoginUsername VARCHAR(30),
  LoginPassword VARCHAR(255),
  USERID INTEGER,
  PRIMARY KEY(USERID, LoginUsername, LoginPassword)
);

CREATE TABLE IF NOT EXISTS StockDashboard(
  DashboardName VARCHAR(50),
  DashboardItemTicker VARCHAR(50),
  DashboardID INTEGER
  -- PRIMARY KEY(DashboardID)
);

CREATE TABLE IF NOT EXISTS StockPreview(
  stockTicker VARCHAR(5),
  BullishBoolean BOOLEAN,
  PRIMARY KEY(stockTicker)
);

-- Please note this will have to change in order for the program to work.
LOAD DATA LOCAL INFILE '/home/illusion/Desktop/CS317_Project/webbCode/stockData.csv' INTO TABLE stockDataBase.stockData FIELDS TERMINATED by ',' LINES TERMINATED by '\n'IGNORE 1 LINES (stockDate, stockName, stockTicker, RSI, MACD, stochasticOperator, Volume, Price, PriceChange);



-- DEBUGGING DO NOT TOUCH
-- Clear any data inside the table initially if there is old data.
-- TRUNCATE TABLE stockData;
-- Insert Data from csv to database gotta figure out how to make this a dynamic thing for any user.
-- Please note I am using Arch Linux, and I am using MariaDB, may be separate syntax in mysql.
-- SELECT * FROM stockDataBase.stockData LIMIT 1000,4000;
-- INSERT INTO LoginTable VALUES("illusion173","Pokemon123",123);
-- SELECT * FROM stockDataBase.LoginTable;
-- SELECT * FROM stockDataBase.StockDashboard;
-- SELECT * FROM stockData;
-- Get latest data from stockticker
-- SELECT stockDate, RSI, MACD, stochasticOperator FROM stockData WHERE stockTicker = "MMM" ORDER by stockDate DESC LIMIT 1; 

-- SELECT * FROM LoginTable;




