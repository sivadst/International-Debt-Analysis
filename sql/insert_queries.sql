USE international_debt_db;

-- These are template insert queries. 
-- The actual bulk data insertion will be performed by the Python script (src/data_insertion.py) using Pandas and mysql-connector-python.

-- 1. Insert into Countries
-- INSERT INTO Countries (Country_Code, Country_Name) VALUES ('AFG', 'Afghanistan');

-- 2. Insert into Indicators
-- INSERT INTO Indicators (Indicator_Code, Indicator_Name) VALUES ('DT.AMT.DLXF.CD', 'Principal repayments on external debt...');

-- 3. Insert into Debt_Data
-- INSERT INTO Debt_Data (Country_ID, Indicator_ID, Year, Debt_Value) VALUES (1, 1, 2010, 1500000.00);
