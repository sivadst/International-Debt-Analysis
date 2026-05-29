# International Debt Analysis System

An end-to-end data analytics pipeline that cleans, preprocesses, stores, and visualizes international debt data using Python, MySQL, and Streamlit.

## Project Structure
```text
international-debt-analysis/
├── data/
│   ├── raw/
│   └── cleaned/
├── notebooks/
│   └── eda_notebook.ipynb
├── sql/
│   ├── schema.sql
│   ├── insert_queries.sql
│   └── analytical_queries.sql
├── src/
│   ├── data_cleaning.py
│   ├── database_connection.py
│   ├── data_insertion.py
│   ├── analysis.py
│   └── mock_data_generator.py
├── dashboard/
│   └── app.py
├── visuals/
├── README.md
├── requirements.txt
└── insights_report.md
```

## Setup Instructions

### 1. Install Dependencies
Ensure you have Python 3.8+ installed, then run:
```bash
pip install -r requirements.txt
```

### 2. Generate Dataset
Since the original World Bank dataset link was missing, a script is provided to generate a highly realistic mock dataset that meets all project requirements.
```bash
python src/mock_data_generator.py
```
This will create `data/raw/international_debt.csv`.

### 3. Data Cleaning
Run the data cleaning script to handle missing values, duplicates, and convert data types.
```bash
python src/data_cleaning.py
```

### 4. Database Setup
Ensure you have a local MySQL server running.
1. Create a `.env` file in the root directory:
   ```env
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=yourpassword
   ```
2. The `sql/schema.sql` creates the database and tables. The `src/data_insertion.py` script will execute the schema creation and populate the data.
```bash
python src/data_insertion.py
```

### 5. Run Streamlit Dashboard
```bash
streamlit run dashboard/app.py
```

## SQL Analytics
The 30 required analytical queries can be found in `sql/analytical_queries.sql`.
