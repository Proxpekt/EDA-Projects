import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="Car Data Overview", layout="wide")

# Load data
@st.cache_data
def load_data():
    raw = pd.read_csv("Cars.csv")
    clean = pd.read_csv("Cars_cleaned.csv")
    return raw, clean

raw_df, clean_df = load_data()

# Title
st.title("🚗 Car Dataset Comparison App")

st.markdown("""
<style>
    .big-font {
        font-size:18px !important;
    }
    .stDataFrame {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Overview Info
st.markdown("### 📊 Dataset Shapes")
col1, col2 = st.columns(2)
with col1:
    st.metric("Raw Data", f"{raw_df.shape[0]} rows × {raw_df.shape[1]} columns")
with col2:
    st.metric("Cleaned Data", f"{clean_df.shape[0]} rows × {clean_df.shape[1]} columns")

st.markdown("---")

# Side-by-side View
st.markdown("## 🔍 Compare Raw vs Cleaned Data")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Raw Dataset")
    st.dataframe(raw_df.head(), use_container_width=True)

with col2:
    st.subheader("Cleaned Dataset")
    st.dataframe(clean_df.head(), use_container_width=True)

st.markdown("---")

# Differences Explained
st.markdown("## ✅ Key Cleaning Steps")
st.markdown("""
- 🧹 **Missing Values** handled
- 🔢 **Data types** cleaned (e.g., 'bhp', 'kmpl' converted to float)
- ✂️ **Units removed** (like "bhp", "kmpl", "cc")
- 📐 **Consistent formatting** across all fields
- 🚘 **Brand and model** separated into individual columns
""")

st.markdown("---")

# Dataset Explorer
st.markdown("## 🧪 Explore the Cleaned Dataset")

with st.expander("🔍 Column Explorer"):
    selected_cols = st.multiselect("Choose columns to view", clean_df.columns.tolist(), default=clean_df.columns.tolist())
    st.dataframe(clean_df[selected_cols], use_container_width=True)

# Summary Statistics
st.markdown("## 📈 Summary Statistics")

tab1, tab2 = st.tabs(["📊 Raw Dataset", "📊 Cleaned Dataset"])

with tab1:
    st.write(raw_df.describe())

with tab2:
    st.write(clean_df.describe())

# Download button
st.markdown("## ⬇️ Download Cleaned Dataset")
st.download_button(
    label="Download Cleaned CSV",
    data=clean_df.to_csv(index=False),
    file_name="cleaned_car_data.csv",
    mime="text/csv"
)