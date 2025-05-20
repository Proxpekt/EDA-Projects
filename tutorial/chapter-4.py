import streamlit as st
import pandas as pd

st.title('Chai Sales Dashboard')

file = st.file_uploader('Upload your CSV file', type=['csv'])

if file:
    st.success('File Upload Successful!')

    df = pd.read_csv(file)

    st.dataframe(df)

if file:
    st.subheader('Data Summary')
    st.write(df.describe())

if file:
    cities = df['City'].unique()
    selected_city = st.selectbox('Filter by cities', cities)
    filterd_data = df[df['City'] == selected_city]
    st.dataframe(filterd_data)