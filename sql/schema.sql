CREATE DATABASE IF NOT EXISTS international_debt_db;
USE international_debt_db;

-- 1. Countries Table
CREATE TABLE IF NOT EXISTS Countries (
    Country_ID INT AUTO_INCREMENT PRIMARY KEY,
    Country_Code VARCHAR(10) UNIQUE NOT NULL,
    Country_Name VARCHAR(100) NOT NULL
);

-- 2. Indicators Table
CREATE TABLE IF NOT EXISTS Indicators (
    Indicator_ID INT AUTO_INCREMENT PRIMARY KEY,
    Indicator_Code VARCHAR(50) UNIQUE NOT NULL,
    Indicator_Name VARCHAR(255) NOT NULL
);

-- 3. Debt Data Table
CREATE TABLE IF NOT EXISTS Debt_Data (
    Data_ID INT AUTO_INCREMENT PRIMARY KEY,
    Country_ID INT NOT NULL,
    Indicator_ID INT NOT NULL,
    Year INT NOT NULL,
    Debt_Value DOUBLE NOT NULL,
    FOREIGN KEY (Country_ID) REFERENCES Countries(Country_ID) ON DELETE CASCADE,
    FOREIGN KEY (Indicator_ID) REFERENCES Indicators(Indicator_ID) ON DELETE CASCADE
);
