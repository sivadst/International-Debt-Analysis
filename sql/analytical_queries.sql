USE international_debt_db;

-- ==========================================
-- 🔹 Basic Queries (1-10)
-- ==========================================

-- 1. Retrieve all distinct country names from the dataset.
SELECT DISTINCT Country_Name 
FROM Countries;

-- 2. Count the total number of countries available.
SELECT COUNT(Country_ID) AS Total_Countries 
FROM Countries;

-- 3. Find the total number of indicators present.
SELECT COUNT(Indicator_ID) AS Total_Indicators 
FROM Indicators;

-- 4. Display the first 10 records of the dataset.
SELECT * 
FROM Debt_Data 
LIMIT 10;

-- 5. Calculate the total global debt.
SELECT SUM(Debt_Value) AS Total_Global_Debt 
FROM Debt_Data;

-- 6. List all unique indicator names.
SELECT DISTINCT Indicator_Name 
FROM Indicators;

-- 7. Find the number of records for each country.
SELECT c.Country_Name, COUNT(d.Data_ID) AS Record_Count 
FROM Countries c 
JOIN Debt_Data d ON c.Country_ID = d.Country_ID 
GROUP BY c.Country_Name;

-- 8. Display all records where debt is greater than 1 billion USD.
SELECT * 
FROM Debt_Data 
WHERE Debt_Value > 1000000000;

-- 9. Find the minimum, maximum, and average debt values.
SELECT MIN(Debt_Value) AS Min_Debt, 
       MAX(Debt_Value) AS Max_Debt, 
       AVG(Debt_Value) AS Avg_Debt 
FROM Debt_Data;

-- 10. Count total number of records in the dataset.
SELECT COUNT(Data_ID) AS Total_Records 
FROM Debt_Data;

-- ==========================================
-- 🔹 Intermediate Level (11-20)
-- ==========================================

-- 11. Find the total debt for each country.
SELECT c.Country_Name, SUM(d.Debt_Value) AS Total_Debt 
FROM Countries c 
JOIN Debt_Data d ON c.Country_ID = d.Country_ID 
GROUP BY c.Country_Name;

-- 12. Display the top 10 countries with the highest total debt.
SELECT c.Country_Name, SUM(d.Debt_Value) AS Total_Debt 
FROM Countries c 
JOIN Debt_Data d ON c.Country_ID = d.Country_ID 
GROUP BY c.Country_Name 
ORDER BY Total_Debt DESC 
LIMIT 10;

-- 13. Find the average debt per country.
SELECT c.Country_Name, AVG(d.Debt_Value) AS Avg_Debt 
FROM Countries c 
JOIN Debt_Data d ON c.Country_ID = d.Country_ID 
GROUP BY c.Country_Name;

-- 14. Calculate total debt for each indicator.
SELECT i.Indicator_Name, SUM(d.Debt_Value) AS Total_Debt 
FROM Indicators i 
JOIN Debt_Data d ON i.Indicator_ID = d.Indicator_ID 
GROUP BY i.Indicator_Name;

-- 15. Identify the indicator contributing the highest total debt.
SELECT i.Indicator_Name, SUM(d.Debt_Value) AS Total_Debt 
FROM Indicators i 
JOIN Debt_Data d ON i.Indicator_ID = d.Indicator_ID 
GROUP BY i.Indicator_Name 
ORDER BY Total_Debt DESC 
LIMIT 1;

-- 16. Find the country with the lowest total debt.
SELECT c.Country_Name, SUM(d.Debt_Value) AS Total_Debt 
FROM Countries c 
JOIN Debt_Data d ON c.Country_ID = d.Country_ID 
GROUP BY c.Country_Name 
ORDER BY Total_Debt ASC 
LIMIT 1;

-- 17. Calculate total debt for each country and indicator combination.
SELECT c.Country_Name, i.Indicator_Name, SUM(d.Debt_Value) AS Total_Debt 
FROM Debt_Data d 
JOIN Countries c ON d.Country_ID = c.Country_ID 
JOIN Indicators i ON d.Indicator_ID = i.Indicator_ID 
GROUP BY c.Country_Name, i.Indicator_Name;

-- 18. Count how many indicators each country has.
SELECT c.Country_Name, COUNT(DISTINCT d.Indicator_ID) AS Indicator_Count 
FROM Countries c 
JOIN Debt_Data d ON c.Country_ID = d.Country_ID 
GROUP BY c.Country_Name;

-- 19. Display countries whose total debt is above the global average.
SELECT c.Country_Name, SUM(d.Debt_Value) AS Total_Debt 
FROM Countries c 
JOIN Debt_Data d ON c.Country_ID = d.Country_ID 
GROUP BY c.Country_Name 
HAVING Total_Debt > (
    SELECT AVG(Total_Debt_Per_Country) 
    FROM (
        SELECT SUM(Debt_Value) AS Total_Debt_Per_Country 
        FROM Debt_Data 
        GROUP BY Country_ID
    ) AS Country_Avg
);

-- 20. Rank countries based on total debt (highest to lowest).
SELECT c.Country_Name, SUM(d.Debt_Value) AS Total_Debt, 
       RANK() OVER (ORDER BY SUM(d.Debt_Value) DESC) AS Debt_Rank 
FROM Countries c 
JOIN Debt_Data d ON c.Country_ID = d.Country_ID 
GROUP BY c.Country_Name;


-- ==========================================
-- 🔹 Advanced Level (21-30)
-- ==========================================

-- 21. Find the top 5 indicators contributing most to global debt.
SELECT i.Indicator_Name, SUM(d.Debt_Value) AS Total_Debt 
FROM Indicators i 
JOIN Debt_Data d ON i.Indicator_ID = d.Indicator_ID 
GROUP BY i.Indicator_Name 
ORDER BY Total_Debt DESC 
LIMIT 5;

-- 22. Calculate percentage contribution of each country to total global debt.
SELECT c.Country_Name, SUM(d.Debt_Value) AS Total_Debt, 
       (SUM(d.Debt_Value) / (SELECT SUM(Debt_Value) FROM Debt_Data)) * 100 AS Percentage_Contribution 
FROM Countries c 
JOIN Debt_Data d ON c.Country_ID = d.Country_ID 
GROUP BY c.Country_Name 
ORDER BY Percentage_Contribution DESC;

-- 23. Identify the top 3 countries for each indicator based on debt.
WITH RankedCountries AS (
    SELECT i.Indicator_Name, c.Country_Name, SUM(d.Debt_Value) AS Total_Debt, 
           RANK() OVER (PARTITION BY i.Indicator_Name ORDER BY SUM(d.Debt_Value) DESC) as Rnk 
    FROM Debt_Data d 
    JOIN Countries c ON d.Country_ID = c.Country_ID 
    JOIN Indicators i ON d.Indicator_ID = i.Indicator_ID 
    GROUP BY i.Indicator_Name, c.Country_Name
) 
SELECT Indicator_Name, Country_Name, Total_Debt 
FROM RankedCountries 
WHERE Rnk <= 3;

-- 24. Find the difference between maximum and minimum debt for each country.
SELECT c.Country_Name, MAX(d.Debt_Value) - MIN(d.Debt_Value) AS Debt_Difference 
FROM Countries c 
JOIN Debt_Data d ON c.Country_ID = d.Country_ID 
GROUP BY c.Country_Name;

-- 25. Create a view for the top 10 countries with highest debt.
CREATE OR REPLACE VIEW Top_10_Countries_Debt AS 
SELECT c.Country_Name, SUM(d.Debt_Value) AS Total_Debt 
FROM Countries c 
JOIN Debt_Data d ON c.Country_ID = d.Country_ID 
GROUP BY c.Country_Name 
ORDER BY Total_Debt DESC 
LIMIT 10;

-- 26. Categorize countries into: High Debt, Medium Debt, Low Debt (based on thresholds)
SELECT c.Country_Name, SUM(d.Debt_Value) AS Total_Debt, 
       CASE 
           WHEN SUM(d.Debt_Value) > 50000000000 THEN 'High Debt' 
           WHEN SUM(d.Debt_Value) BETWEEN 10000000000 AND 50000000000 THEN 'Medium Debt' 
           ELSE 'Low Debt' 
       END AS Debt_Category 
FROM Countries c 
JOIN Debt_Data d ON c.Country_ID = d.Country_ID 
GROUP BY c.Country_Name;

-- 27. Use window functions to calculate cumulative debt per country.
SELECT c.Country_Name, d.Year, d.Debt_Value,
       SUM(d.Debt_Value) OVER (PARTITION BY c.Country_Name ORDER BY d.Year) AS Cumulative_Debt 
FROM Countries c 
JOIN Debt_Data d ON c.Country_ID = d.Country_ID;

-- 28. Find indicators where average debt is higher than overall average debt.
SELECT i.Indicator_Name, AVG(d.Debt_Value) AS Avg_Debt 
FROM Indicators i 
JOIN Debt_Data d ON i.Indicator_ID = d.Indicator_ID 
GROUP BY i.Indicator_Name 
HAVING Avg_Debt > (SELECT AVG(Debt_Value) FROM Debt_Data);

-- 29. Identify countries contributing more than 5% of global debt.
SELECT c.Country_Name, SUM(d.Debt_Value) AS Total_Debt, 
       (SUM(d.Debt_Value) / (SELECT SUM(Debt_Value) FROM Debt_Data)) * 100 AS Percentage_Contribution 
FROM Countries c 
JOIN Debt_Data d ON c.Country_ID = d.Country_ID 
GROUP BY c.Country_Name 
HAVING Percentage_Contribution > 5;

-- 30. Find the most dominant indicator (highest contribution) for each country.
WITH RankedIndicators AS (
    SELECT c.Country_Name, i.Indicator_Name, SUM(d.Debt_Value) AS Total_Debt, 
           RANK() OVER (PARTITION BY c.Country_Name ORDER BY SUM(d.Debt_Value) DESC) as Rnk 
    FROM Debt_Data d 
    JOIN Countries c ON d.Country_ID = c.Country_ID 
    JOIN Indicators i ON d.Indicator_ID = i.Indicator_ID 
    GROUP BY c.Country_Name, i.Indicator_Name
) 
SELECT Country_Name, Indicator_Name, Total_Debt 
FROM RankedIndicators 
WHERE Rnk = 1;
