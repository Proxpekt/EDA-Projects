import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
from streamlit_option_menu import option_menu
import time

# ---------------------
# Page Setup
# ---------------------
st.set_page_config(
    page_title="Household Power Consumption EDA",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------
# Sidebar Navigation
# ---------------------
with st.sidebar:
    selected = option_menu(
        "Main Menu",
        ["Home", "Data Overview", "Energy Trends", "Visualizations", "Insights", "About"],
        icons=["house", "table", "activity", "bar-chart", "lightbulb", "info-circle"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "10px", "background-color": "#2c2c2c"},
            "icon": {"color": "white", "font-size": "18px"},
            "nav-link": {"font-size": "16px", "color": "#ffffff"},
            "nav-link-selected": {"background-color": "#3FC1C9", "color": "black"}
        }
    )

# Load data
@st.cache_data
def load_data():
    df_raw = pd.read_csv('household_power_consumption.csv')
    df_cleaned = pd.read_csv("cleaned_dataset.csv", parse_dates=['DateTime'])
    return df_raw, df_cleaned


df_raw, df_cleaned = load_data()

# ---------------------
# Home Page
# ---------------------
if selected == "Home":
    st.title("💡 Household Power Consumption EDA")
    st.subheader("A deep dive into energy usage patterns")
    
    st.image("wp2252989.jpg", use_container_width=True)

    with st.expander("📌 Problem Statement"):
        st.markdown("""
        Energy consumption is a vital metric for sustainable development and efficient utility management. 
        This project explores the **Household Power Consumption** dataset to:

        - Identify peak consumption hours 🕒
        - Compare active vs. reactive power ⚡
        - Understand sub-metering trends 🧮
        - Enable data-driven decisions for energy conservation 🌍
        """)
    
# ---------------------
# Data Overview
# ---------------------
elif selected == "Data Overview":
    # Custom CSS for styling
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

    st.header("📊 Dataset Overview")

    # Shape Comparison
    st.markdown("### 📏 Dataset Shapes")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Raw Data", f"{df_raw.shape[0]} rows × {df_raw.shape[1]} columns")
    with col2:
        st.metric("Cleaned Data", f"{df_cleaned.shape[0]} rows × {df_cleaned.shape[1]} columns")

    st.markdown("---")

    # Side-by-side preview
    st.markdown("## 🔍 Compare Raw vs Cleaned Data")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📄 Raw Dataset")
        st.dataframe(df_raw.head(), use_container_width=True)

    with col2:
        st.subheader("🧹 Cleaned Dataset")
        st.dataframe(df_cleaned.head(), use_container_width=True)

    st.markdown("---")

    # Key Cleaning Steps
    st.markdown("## ✅ Key Cleaning Steps")
    st.markdown("""
    - 🧼 Removed rows with missing or corrupted entries  
    - 🕒 Combined Date and Time into a single DateTime column  
    - 📐 Converted measurement columns to numeric types  
    - 🔢 Added useful columns: **hour**, **date**, and **Total_sub_metering**  
    """)

    st.markdown("---")

    # Explore Cleaned Dataset
    st.markdown("## 🧪 Explore the Cleaned Dataset")

    with st.expander("🔍 Column Explorer"):
        selected_cols = st.multiselect("Choose columns to view", df_cleaned.columns.tolist(), default=df_cleaned.columns.tolist())
        st.dataframe(df_cleaned[selected_cols], use_container_width=True)

    # Summary Statistics
    st.markdown("## 📈 Summary Statistics")

    tab1, tab2 = st.tabs(["📊 Raw Dataset", "📊 Cleaned Dataset"])

    with tab1:
        st.write(df_raw.describe())

    with tab2:
        st.write(df_cleaned.describe())

    # Download button
    st.markdown("## ⬇️ Download Cleaned Dataset")
    st.download_button(
        label="Download Cleaned CSV",
        data=df_cleaned.to_csv(index=False),
        file_name="cleaned_household_power_consumption.csv",
        mime="text/csv"
    )

# ---------------------
# Energy Trends
# ---------------------
elif selected == "Energy Trends":
    st.header("⚡ Energy Usage Trends")

    # Aggregate values
    hourly_avg = df_cleaned.groupby('hour')['Total_sub_metering'].mean()
    daily_avg = df_cleaned.groupby('Date')['Total_sub_metering'].sum()
    weekday_avg = df_cleaned.groupby(df_cleaned['DateTime'].dt.day_name())['Total_sub_metering'].mean()
    monthly_avg = df_cleaned.groupby(df_cleaned['DateTime'].dt.month)['Total_sub_metering'].mean()

    tab1, tab2, tab3, tab4 = st.tabs(["🕒 Hourly", "📅 Daily", "📆 Weekly", "🗓️ Monthly"])

    with tab1:
        st.subheader("Average Energy Consumption by Hour")
        fig, ax = plt.subplots(figsize=(5, 3))
        sns.lineplot(x=hourly_avg.index, y=hourly_avg.values, marker='o', ax=ax)
        ax.set_title("Hourly Sub-Metering Trend")
        ax.set_xlabel("Hour of Day")
        ax.set_ylabel("Avg Total Sub-Metering")
        with st.container():
            col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.pyplot(fig)

    with tab2:
        st.subheader("Total Energy Consumption by Date")
        fig, ax = plt.subplots(figsize=(6, 3.5))
        daily_avg.plot(ax=ax)
        ax.set_title("Daily Total Sub-Metering")
        ax.set_xlabel("Date")
        # ax.tick_params(axis='x', rotation=45)
        ax.xaxis.set_major_locator(plt.MaxNLocator(100))  # Show only ~10 x-ticks
        ax.set_ylabel("Total Sub-Metering")
        fig.tight_layout()
        with st.container():
            col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.pyplot(fig)

    with tab3:
        st.subheader("Average Consumption by Day of the Week")
        ordered_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekday_avg = weekday_avg.reindex(ordered_days)
        fig, ax = plt.subplots(figsize=(6, 3.5))
        sns.barplot(x=weekday_avg.index, y=weekday_avg.values, palette="viridis", ax=ax)
        ax.set_title("Average by Day of Week")
        ax.set_ylabel("Avg Total Sub-Metering")
        ax.tick_params(axis='x', rotation=20)
        with st.container():
            col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.pyplot(fig)        

    with tab4:
        st.subheader("Average Consumption by Month")
        month_names = {
            1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
            7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
        }
        monthly_avg.index = monthly_avg.index.map(month_names)
        fig, ax = plt.subplots(figsize=(6, 3.5))
        sns.barplot(x=monthly_avg.index, y=monthly_avg.values, palette="coolwarm", ax=ax)
        ax.set_title("Average by Month")
        ax.set_ylabel("Avg Total Sub-Metering")
        with st.container():
            col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.pyplot(fig)

# ---------------------
# Visualizations
# ---------------------
# elif selected == "Visualizations":
#     st.header("📉 Custom Visualizations")
#     st.subheader("🔧 Select Parameters")

#     num_cols = df_cleaned.select_dtypes(include='number').columns.tolist()
#     col = st.selectbox("Select numeric column", num_cols)

#     st.write(f"### Histogram for {col}")
#     fig1, ax1 = plt.subplots()
#     sns.histplot(df_cleaned[col], kde=True, ax=ax1)
#     st.pyplot(fig1)

#     st.write(f"### Boxplot for {col}")
#     fig2, ax2 = plt.subplots()
#     sns.boxplot(x=df_cleaned[col], ax=ax2)
#     st.pyplot(fig2)
elif selected == "Visualizations":
    st.header("📉 Custom Visualizations")
    st.subheader("🔧 Select Parameters")

    num_cols = df_cleaned.select_dtypes(include='number').columns.tolist()
    col = st.selectbox("Select numeric column", num_cols)

    # Histogram
    st.markdown(f"### 📊 Histogram - `{col}`")
    fig1, ax1 = plt.subplots(figsize=(4.5, 3))
    sns.histplot(df_cleaned[col], kde=True, ax=ax1, color="skyblue", edgecolor="black")
    ax1.set_title(f"Distribution of {col}", fontsize=11)
    ax1.set_xlabel(col, fontsize=10)
    ax1.set_ylabel("Frequency", fontsize=10)
    ax1.tick_params(axis='both', labelsize=8)
    fig1.tight_layout()
    st.pyplot(fig1)

    st.markdown("---")

    # Boxplot
    st.markdown(f"### 📦 Boxplot - `{col}`")
    fig2, ax2 = plt.subplots(figsize=(5.5, 2.5))
    sns.boxplot(x=df_cleaned[col], ax=ax2, color="lightcoral")
    ax2.set_title(f"Boxplot of {col}", fontsize=11)
    ax2.set_xlabel(col, fontsize=10)
    ax2.tick_params(axis='x', labelsize=8)
    fig2.tight_layout()
    st.pyplot(fig2)


# ---------------------
# Insights
# ---------------------
elif selected == "Insights":
    st.header("💡 Key Observations")
    
    peak_hour = df_cleaned.groupby('hour')['Total_sub_metering'].mean().idxmax()
    high_day = df_cleaned.groupby('Date')['Total_sub_metering'].sum().idxmax()

    st.success(f"🔌 Peak energy usage hour: {peak_hour}:00")
    st.success(f"📅 Highest consumption date: {high_day}")

    st.markdown("### Correlation Heatmap")
    fig, ax = plt.subplots()
    sns.heatmap(df_cleaned.select_dtypes(include='number').corr(), annot=True, cmap='YlGnBu', ax=ax)
    st.pyplot(fig)

# ---------------------
# About Page
# ---------------------
elif selected == "About":
    st.header("ℹ️ About This App")
    st.markdown("""
    - **Project**: Household Power Consumption EDA
    - **Author**: Aayush
    - **Tools Used**: Python, Streamlit, Pandas, Matplotlib, Seaborn
    - **Purpose**: Understand and visualize household energy trends for smart decision-making.
    """)
    st.balloons()