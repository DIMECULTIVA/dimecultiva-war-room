import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- 1. ENTERPRISE CONFIG & CSS ---
st.set_page_config(page_title="DIMECULTIVA | Enterprise OS", page_icon="⚙️", layout="wide")

st.markdown("""
    <style>
    /* Dark Theme Core */
    [data-testid="stAppViewContainer"] { background-color: #050505; color: #ffffff; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-right: 1px solid #1f1f1f; }
    
    /* Premium Metric Cards */
    [data-testid="stMetricValue"] { font-size: 2rem; font-weight: 800; color: #ffffff; }
    [data-testid="stMetricDelta"] { font-size: 1rem; }
    .stMetric { background: rgba(20, 20, 20, 0.8); backdrop-filter: blur(10px); border: 1px solid #222; padding: 20px; border-radius: 8px; border-top: 3px solid #33cc66; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    
    /* Custom Headers */
    h1, h2, h3 { font-weight: 800; tracking: tight; }
    hr { border-color: #1f1f1f; }
    </style>
""", unsafe_allow_html=True)

# --- 2. ADVANCED DATA ENGINE (Synthetic but realistic) ---
@st.cache_data
def generate_enterprise_data():
    np.random.seed(42)
    today = datetime.today()
    dates = [today - timedelta(days=x) for x in range(365)]
    
    # Financial Data
    revenue = np.cumsum(np.random.normal(50000, 15000, 365)) + 5000000
    overhead = revenue * np.random.uniform(0.4, 0.7, 365)
    
    df_finance = pd.DataFrame({
        'Date': dates, 'Revenue': revenue, 'Overhead': overhead
    })
    df_finance['Net Profit'] = df_finance['Revenue'] - df_finance['Overhead']
    df_finance['Margin %'] = (df_finance['Net Profit'] / df_finance['Revenue']) * 100
    
    # Logistics/Operations Data
    regions = ['Gauteng', 'Western Cape', 'KZN', 'Eastern Cape']
    df_ops = pd.DataFrame({
        'Region': np.random.choice(regions, 1000, p=[0.5, 0.25, 0.15, 0.10]),
        'Delivery_Time_Hrs': np.random.normal(48, 12, 1000),
        'Status': np.random.choice(['On Time', 'Delayed', 'Failed'], 1000, p=[0.85, 0.12, 0.03])
    })
    
    return df_finance.sort_values('Date'), df_ops

df_finance, df_ops = generate_enterprise_data()

# --- 3. SIDEBAR NAVIGATION ---
st.sidebar.markdown("<h2 style='text-align: center; color: white; letter-spacing: 2px;'>DIMECULTIVA<span style='color: #33cc66;'>.</span></h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; color: #888; font-size: 12px; margin-bottom: 30px;'>ENTERPRISE OS // V.2.4</p>", unsafe_allow_html=True)

menu = st.sidebar.radio("COMMAND MODULES", ["💰 Financial Intelligence", "⚙️ Operational Logistics", "🤖 AI Diagnostic Advisor"])

st.sidebar.markdown("---")
st.sidebar.markdown("### Client Settings")
date_range = st.sidebar.selectbox("Reporting Period", ["Last 30 Days", "Last 90 Days", "Year to Date", "All Time"], index=1)

# --- 4. MODULE: FINANCIAL INTELLIGENCE ---
if menu == "💰 Financial Intelligence":
    st.title("Financial Command Center")
    st.markdown("Live cross-departmental revenue tracking and margin analysis.")
    
    # Top KPI Row
    col1, col2, col3, col4 = st.columns(4)
    current_rev = df_finance['Revenue'].iloc[-1]
    prev_rev = df_finance['Revenue'].iloc[-30]
    rev_growth = ((current_rev - prev_rev) / prev_rev) * 100
    
    col1.metric("YTD Gross Revenue", f"R {current_rev/1000000:.2f}M", f"+{rev_growth:.1f}% vs last month")
    col2.metric("Average Gross Margin", f"{df_finance['Margin %'].mean():.1f}%", "Optimal")
    col3.metric("Operating Overhead", f"R {df_finance['Overhead'].iloc[-1]/1000000:.2f}M", "-2.4% vs last month", delta_color="inverse")
    col4.metric("EBITDA", f"R {df_finance['Net Profit'].iloc[-1]/1000000:.2f}M", "+5.2%")

    st.markdown("---")
    
    # Deep Dive Charts
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("Revenue vs Overhead Trajectory")
        fig1 = px.area(df_finance.tail(90), x='Date', y=['Revenue', 'Overhead'], 
                       color_discrete_sequence=['rgba(51, 204, 102, 0.7)', 'rgba(248, 81, 73, 0.7)'])
        fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white', margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig1, use_container_width=True)
        
    with c2:
        st.subheader("Cash Flow Distribution")
        fig2 = go.Figure(go.Waterfall(
            name="20", orientation="v",
            measure=["relative", "relative", "total", "relative", "total"],
            x=["Gross Sales", "Services", "Total Revenue", "Overhead", "Net Profit"],
            textposition="outside",
            y=[4000000, 1500000, 5500000, -2200000, 3300000],
            connector={"line":{"color":"#333"}},
            increasing={"marker":{"color":"#33cc66"}},
            decreasing={"marker":{"color":"#f85149"}},
            totals={"marker":{"color":"#1f6feb"}}
        ))
        fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
        st.plotly_chart(fig2, use_container_width=True)

# --- 5. MODULE: OPERATIONAL LOGISTICS ---
elif menu == "⚙️ Operational Logistics":
    st.title("Logistics & Bottleneck Detection")
    st.markdown("Real-time fulfillment tracking and regional efficiency metrics.")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Active Fleet Units", "1,204", "All systems nominal")
    c2.metric("Global Fulfillment Rate", "96.4%", "-0.2% vs SLA")
    c3.metric("Avg Delivery Time", "42.5 Hrs", "-4.1 Hrs (Improving)", delta_color="inverse")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Regional Workload Distribution")
        reg_counts = df_ops['Region'].value_counts().reset_index()
        reg_counts.columns = ['Region', 'Volume']
        fig3 = px.bar(reg_counts, x='Region', y='Volume', color='Region', color_discrete_sequence=px.colors.sequential.Tealgrn)
        fig3.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
        st.plotly_chart(fig3, use_container_width=True)
        
    with col2:
        st.subheader("SLA Exception Tracking")
        status_counts = df_ops['Status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        fig4 = px.pie(status_counts, values='Count', names='Status', hole=0.6, color_discrete_sequence=['#33cc66', '#d29922', '#f85149'])
        fig4.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
        st.plotly_chart(fig4, use_container_width=True)

# --- 6. MODULE: AI DIAGNOSTIC ---
elif menu == "🤖 AI Diagnostic Advisor":
    st.title("Automated Executive Intelligence")
    st.markdown("Proprietary AI engine scanning live data streams for operational risks.")
    
    st.info("Scanning 4.2 million data points across Finance, HR, and Operations...", icon="🔄")
    
    st.markdown("### 🚨 Critical Exceptions Detected (2)")
    st.error("**CASH FLOW ALERT:** Overhead in the Western Cape region has spiked 14% above the 90-day moving average. Recommend an immediate audit of logistics contractors in Cape Town.")
    st.warning("**SLA RISK:** 12% of deliveries in Gauteng are currently flagged as 'Delayed'. This correlates with a 30% drop in active fleet units reported this morning.")
    
    st.markdown("### ✅ Optimizations Executed")
    st.success("**AUTOMATION:** Monthly VAT compilation for SARS has been automatically generated and securely routed to the CFO's inbox.")
