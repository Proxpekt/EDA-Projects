import streamlit as st
import pandas as pd

# Load Data
df = pd.read_csv("Cars_cleaned.csv")

# Page Config
st.set_page_config(page_title="🚗 Cars EDA Dashboard", page_icon="🚗", layout="wide")

# --- Custom CSS Styling ---
st.markdown("""
    <style>
        /* App-wide style */
        body {
            background-color: #f9f9f9;
        }
        /* Header */
        .main h1 {
            font-size: 3rem;
            color: #2c3e50;
        }
        /* Section Headers */
        h2 {
            color: #e67e22;
            margin-top: 2em;
        }
        h3 {
            color: #34495e;
            margin-top: 1.5em;
        }
        /* Markdown Paragraphs */
        .markdown-text-container {
            font-size: 1.1rem;
            line-height: 1.6;
        }
        /* DataFrames */
        .dataframe {
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 10px;
        }
        /* Footer */
        footer {
            visibility: hidden;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🚗 Cars EDA Dashboard")
st.markdown("#### Gain insights into the used car market with data-powered exploration and statistics.")

# Section: Basic Info
st.markdown("## 🔍 1. Dataset Overview")
mem_usage = df.memory_usage(deep=True).sum() / (1024 ** 2)

info_df = pd.DataFrame({
    "📌 Column": df.columns,
    "✅ Non-Null Count": df.notnull().sum().values,
    "🔠 Data Type": df.dtypes.astype(str).values,
    "🔢 Unique Values": [df[col].nunique() for col in df.columns],
    "📍 Example Value": [df[col].dropna().iloc[0] if not df[col].dropna().empty else "N/A" for col in df.columns]
})

st.dataframe(info_df, use_container_width=True)

st.markdown(f"""
<div style="padding: 10px; background-color: #ecf0f1; border-left: 5px solid #2ecc71; border-radius: 5px">
<b>🧾 Total Entries:</b> {len(df)}  
<br><b>📊 Total Columns:</b> {df.shape[1]}  
<br><b>🧠 Memory Usage:</b> {mem_usage:.2f} MB
</div>
""", unsafe_allow_html=True)

# Section: Summary Statistics
st.markdown("## 📈 2. Summary Statistics")
st.dataframe(df.describe(), use_container_width=True)

# Section: Null Values
st.markdown("## ❓ 3. Missing Values")
nulls = df.isnull().sum()
nulls = nulls[nulls > 0].sort_values(ascending=False)

if nulls.empty:
    st.success("✅ No missing values found in the dataset!")
else:
    st.dataframe(nulls.to_frame(name="Missing Count"))

# Section: Unique Value Counts
st.markdown("## 🧬 4. Unique Value Counts")

cols_to_check = ['Fuel_Type', 'Transmission', 'Owner_Type', 'Colour', 'Company_Name']
for col in cols_to_check:
    st.markdown(f"### 🔹 {col}")
    st.markdown(f"- Unique Values: `{df[col].nunique()}`")
    st.dataframe(df[col].value_counts().to_frame(name="Count"))

# Section: Top Driven Cars
st.markdown("## 🚘 5. Top 5 Most Driven Cars")
top_driven = df.sort_values(by='Kilometers_Driven', ascending=False)[['Name', 'Kilometers_Driven']].head()
st.dataframe(top_driven, use_container_width=True)

# Section: Average Price by Brand
st.markdown("## 💸 6. Average Car Price by Brand")
avg_price = df.groupby("Company_Name")["Price"].mean().sort_values(ascending=False).round(2)
st.dataframe(avg_price.to_frame(name="Average Price (₹)"), use_container_width=True)
