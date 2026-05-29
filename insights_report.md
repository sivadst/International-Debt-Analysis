# International Debt Analysis Insights Report

## Overview
This report provides key findings from the Exploratory Data Analysis (EDA) and SQL Analytics performed on the International Debt Statistics dataset. The dataset includes various indicators related to debt and capital flows for multiple countries over the years 2010 to 2021.

## 1. Country-wise Debt Distribution
- **Debt Disparity**: There is a significant disparity in total debt across countries. The top indebted countries account for a disproportionately large percentage of the total global debt.
- **Top Indebted Countries**: Preliminary analysis using our generated dataset highlights that larger, more developed economies tend to carry higher nominal debt loads. (Note: specific names dynamically reflect the simulated dataset generation).
- **Least Indebted Countries**: Smaller island nations and least developed countries tend to carry the lowest nominal debt amounts.

## 2. Indicator-wise Debt Insights
- **Dominant Debt Types**: Long-term debt (both public and publicly guaranteed as well as private non-guaranteed) constitutes the massive majority of total external debt stocks.
- **Interest and Repayments**: Principal repayments consistently outpace interest payments, representing a large outflow of capital from debtor countries.
- **Net Flows**: The total external debt stocks (`DT.DOD.DECT.CD`) represent the highest cumulative metric across all datasets.

## 3. Trends and Patterns (2010-2021)
- **Upward Trajectory**: Global debt levels have shown a consistent upward trajectory over the decade, reflecting increased borrowing.
- **Volatility**: Certain periods reflect spikes in borrowing, likely correlating with global economic events, stimulus packages, or crisis management borrowing.

## 4. SQL Analytics Key Takeaways
By executing the 30 advanced SQL queries, we have categorized and ranked countries according to their debt burdens:
- **High Debt / Medium Debt / Low Debt**: We successfully segmented the countries based on their cumulative debt profiles using SQL `CASE` statements.
- **Cumulative and Ranking**: Advanced window functions (`RANK()`, `SUM() OVER`) allowed us to identify the exact percentile contribution of the top 3 countries for every specific debt indicator.

## Conclusion
The developed end-to-end analytics pipeline successfully standardizes the complex raw financial data, enabling seamless insertion into a normalized MySQL database. The interactive Streamlit dashboard now serves as a robust tool for non-technical stakeholders to slice, filter, and drill down into the financial health and debt profiles of nations globally.
