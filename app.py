import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="Executive War Room | DIMECULTIVA", layout="wide")
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #050505; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #1f1f1f; }
    .stMetric { background-color: #0a0a0a; border: 1px solid #1f1f1f; padding: 15px; border-radius: 4px; border-top: 2px solid #33cc66; }
    </style>
""", unsafe_allow_html=True)

# --- SIMULATED ENTERPRISE DATA ---
@st.cache_data
def load_data():
    np.random.seed(42)
    dates = pd.date_range(start="2025-01-01", periods=180)
    data = pd.DataFrame({
        'Date': dates,
        'Revenue': np.random.randint(50000, 150000, size=180),
        'Overhead': np.random.randint(30000, 80000, size=180),
        'Region': np.random.choice(['Gauteng', 'Western Cape', 'KZN'], size=180)
    })
    data['Margin'] = ((data['Revenue'] - data['Overhead']) / data['Revenue']) * 100
    return data

df = load_data()

# --- SIDEBAR ---
st.sidebar.title("DIMECULTIVA")
st.sidebar.markdown("### Executive War Room")
st.sidebar.markdown("Interactive proof-of-work showcasing live operational visibility.")
selected_region = st.sidebar.selectbox("Filter by Region", ['All Regions', 'Gauteng', 'Western Cape', 'KZN'])

if selected_region != 'All Regions':
    df = df[df['Region'] == selected_region]

# --- DASHBOARD LAYOUT ---
st.title("Live Operations Dashboard")

c1, c2, c3 = st.columns(3)
c1.metric("YTD Revenue", f"R {df['Revenue'].sum():,.0f}")
c2.metric("Avg Gross Margin", f"{df['Margin'].mean():.1f} %")
c3.metric("Active Regions", len(df['Region'].unique()))

st.markdown("---")
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Revenue vs Overhead Trend")
    fig_line = px.line(df, x='Date', y=['Revenue', 'Overhead'], color_discrete_sequence=['#33cc66', '#f85149'])
    fig_line.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
    st.plotly_chart(fig_line, use_container_width=True)

with col2:
    st.subheader("Revenue Distribution")
    fig_pie = px.pie(df, values='Revenue', names='Region', hole=0.5, color_discrete_sequence=['#33cc66', '#1f6feb', '#8e15ac'])
    fig_pie.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
    st.plotly_chart(fig_pie, use_container_width=True)