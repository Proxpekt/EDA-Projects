import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title='Simple Sales Dashboard', layout='wide')

@st.cache_data
def load_data():
    np.random.seed(42)
    data = {
        "Date": pd.date_range("2024-01-01", periods=60),
        "Region": ["North", "South", "East", "West"] * 15,
        "Product": ["Chai", "Coffee", "Green Tea"] * 20,
        "Revenue": np.random.randint(500, 3000, 60),
        "Units_Sold": np.random.randint(20, 100, 60)
    }

    return pd.DataFrame(data)

df = load_data()

st.sidebar.header('Filters')
region_filter = st.sidebar.multiselect("Select Region", df['Region'].unique(), default=df['Region'].unique())
product_filter = st.sidebar.multiselect("Select Product", df['Product'].unique(), default=df['Product'].unique())

filtered_df = df[df['Region'].isin(region_filter) & df['Product'].isin(product_filter)]

st.title('Simple Sales Dasboard')

total_revenue = filtered_df['Revenue'].sum()
units_sold = filtered_df['Units_Sold'].sum()
avg_units = filtered_df['Units_Sold'].mean()

col1, col2, col3 = st.columns(3)
col1.metric('Total Revenue', f'Rs. {total_revenue:,}')
col2.metric("Total Units Sold", units_sold)
col3.metric("Avg Units per Day", f"{avg_units:.2f}")

st.markdown('---')

st.subheader('Revenue by Product')
revenue_chart = filtered_df.groupby('Product')['Revenue'].sum()
st.bar_chart(revenue_chart)

st.subheader('Units Sold over Time')
units_time = filtered_df.groupby('Date')['Units_Sold'].sum()
st.line_chart(units_time)

st.markdown('---')
st.subheader("Raw Data")
st.dataframe(filtered_df.sort_values(by="Date", ascending=False), use_container_width=True)