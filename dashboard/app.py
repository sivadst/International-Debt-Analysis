import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys

# Add src to sys.path to import database connection
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

try:
    from database_connection import get_database_connection
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False

# Set page config
st.set_page_config(
    page_title="International Debt Analysis",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data function (with caching)
@st.cache_data
def load_data_from_csv():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(script_dir, "../data/cleaned/cleaned_debt_data.csv")
        return pd.read_csv(path)
    except FileNotFoundError:
        return None

def load_data_from_db():
    conn = get_database_connection(use_db=True)
    if not conn:
        return None
    
    query = """
    SELECT c.Country_Name, i.Indicator_Name, d.Year, d.Debt_Value
    FROM Debt_Data d
    JOIN Countries c ON d.Country_ID = c.Country_ID
    JOIN Indicators i ON d.Indicator_ID = i.Indicator_ID
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Main logic
st.title("🌍 International Debt Analysis System")
st.markdown("An interactive dashboard to explore and analyze international debt statistics.")

# Sidebar setup
st.sidebar.header("Navigation & Filters")
data_source = st.sidebar.radio("Data Source", ["CSV File", "MySQL Database"])

df = None
if data_source == "MySQL Database" and DB_AVAILABLE:
    df = load_data_from_db()
    if df is None:
        st.sidebar.error("Could not connect to MySQL. Falling back to CSV.")
        df = load_data_from_csv()
else:
    df = load_data_from_csv()

if df is None:
    st.error("No data found! Please ensure data generation and cleaning steps are completed.")
    st.stop()

# Ensure columns map correctly whether from CSV or DB
if 'Country_Name' in df.columns:
    df = df.rename(columns={'Country_Name': 'country_name', 'Indicator_Name': 'indicator_name', 'Year': 'year', 'Debt_Value': 'debt_value'})

# Filters
countries = st.sidebar.multiselect("Select Countries", options=df['country_name'].unique(), default=[])
indicators = st.sidebar.multiselect("Select Indicators", options=df['indicator_name'].unique(), default=[])

# Filter dataframe
filtered_df = df.copy()
if countries:
    filtered_df = filtered_df[filtered_df['country_name'].isin(countries)]
if indicators:
    filtered_df = filtered_df[filtered_df['indicator_name'].isin(indicators)]

# KPIs
st.header("📈 Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Global Debt", f"${filtered_df['debt_value'].sum():,.2f}")
col2.metric("Average Debt", f"${filtered_df['debt_value'].mean():,.2f}")
col3.metric("Total Countries", f"{filtered_df['country_name'].nunique()}")
col4.metric("Total Indicators", f"{filtered_df['indicator_name'].nunique()}")

# Dataset Preview
st.header("🔍 Dataset Preview")
st.dataframe(filtered_df.head(100), use_container_width=True)

# Tabs for visual analysis
tab1, tab2, tab3 = st.tabs(["Country Analysis", "Indicator Analysis", "Trend Analysis"])

with tab1:
    st.subheader("Top Countries by Debt")
    country_debt = filtered_df.groupby('country_name')['debt_value'].sum().reset_index().sort_values(by='debt_value', ascending=False).head(20)
    fig_country = px.bar(country_debt, x='country_name', y='debt_value', title='Top 20 Indebted Countries', color='debt_value', color_continuous_scale='Reds')
    st.plotly_chart(fig_country, use_container_width=True)

with tab2:
    st.subheader("Debt Contribution by Indicator")
    indicator_debt = filtered_df.groupby('indicator_name')['debt_value'].sum().reset_index().sort_values(by='debt_value', ascending=False)
    fig_ind = px.pie(indicator_debt.head(10), names='indicator_name', values='debt_value', title='Top 10 Debt Indicators')
    st.plotly_chart(fig_ind, use_container_width=True)
    
with tab3:
    st.subheader("Global Debt Trend")
    trend = filtered_df.groupby('year')['debt_value'].sum().reset_index()
    fig_trend = px.line(trend, x='year', y='debt_value', title='Debt Accumulation Over Time', markers=True)
    st.plotly_chart(fig_trend, use_container_width=True)

st.markdown("---")
st.markdown("Built for the Data Analytics Project using Python, Pandas, MySQL, and Streamlit.")
