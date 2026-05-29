import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os

def load_cleaned_data(filepath="../data/cleaned/cleaned_debt_data.csv"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    abs_path = os.path.join(script_dir, filepath)
    try:
        df = pd.read_csv(abs_path)
        return df
    except FileNotFoundError:
        print(f"File not found: {abs_path}")
        return None

def analyze_country_debt_distribution(df):
    """Analyze and plot country-wise total debt distribution."""
    country_debt = df.groupby('country_name')['debt_value'].sum().reset_index()
    country_debt = country_debt.sort_values(by='debt_value', ascending=False)
    
    # Plotly Bar Chart
    fig = px.bar(
        country_debt.head(20), 
        x='country_name', 
        y='debt_value',
        title="Top 20 Countries with Highest Total Debt",
        labels={'country_name': 'Country', 'debt_value': 'Total Debt (USD)'}
    )
    return country_debt, fig

def analyze_indicator_debt(df):
    """Analyze and plot total debt per indicator."""
    indicator_debt = df.groupby('indicator_name')['debt_value'].sum().reset_index()
    indicator_debt = indicator_debt.sort_values(by='debt_value', ascending=False)
    
    # Plotly Pie Chart for top 5 indicators
    top_5_indicators = indicator_debt.head(5)
    fig = px.pie(
        top_5_indicators,
        names='indicator_name',
        values='debt_value',
        title="Top 5 Indicators Contributing to Global Debt"
    )
    return indicator_debt, fig

def yearly_debt_trend(df):
    """Analyze and plot yearly global debt trend."""
    yearly_debt = df.groupby('year')['debt_value'].sum().reset_index()
    
    # Seaborn Line Chart
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=yearly_debt, x='year', y='debt_value', marker="o")
    plt.title("Global Debt Trend Over Time")
    plt.xlabel("Year")
    plt.ylabel("Total Debt (USD)")
    plt.grid(True)
    
    return yearly_debt, plt.gcf()

if __name__ == "__main__":
    df = load_cleaned_data()
    if df is not None:
        print("Data loaded successfully.")
        
        # Display some statistical summaries
        print("\n--- Statistical Summary ---")
        print(df['debt_value'].describe())
        
        country_debt, fig1 = analyze_country_debt_distribution(df)
        print("\nTop 5 indebted countries:")
        print(country_debt.head(5))
        
        indicator_debt, fig2 = analyze_indicator_debt(df)
        print("\nTop 5 debt indicators:")
        print(indicator_debt.head(5))
        
        print("\nAnalysis complete. Run the Streamlit dashboard for interactive visualizations.")
