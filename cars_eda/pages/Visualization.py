import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(page_title="📊 Visual Analysis", layout="wide")

# Load data
df = pd.read_csv("Cars_cleaned.csv")

# Inject Custom CSS
st.markdown("""
    <style>
        .main {
            background-color: #f8f9fa;
        }
        h1, h2, h3 {
            color: #2c3e50;
        }
        .stRadio > div {
            flex-direction: row;
        }
        .stSelectbox label, .stRadio label {
            font-weight: bold;
        }
        .css-1d391kg {  /* plot title spacing */
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("📊 Car Dataset Visualization & Analysis")
st.markdown("Explore the dataset using **Univariate**, **Bivariate**, and **Multivariate** plots.")

# Selection
analysis_type = st.radio("📌 Choose Analysis Type", ("Univariate", "Bivariate", "Multivariate"))

# === UNIVARIATE ===
if analysis_type == "Univariate":
    st.header("🔍 Univariate Analysis")
    column = st.selectbox("Select a column for univariate analysis", df.columns)

    if pd.api.types.is_numeric_dtype(df[column]):
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📊 Distribution")
            fig, ax = plt.subplots()
            sns.histplot(df[column], kde=True, ax=ax, color="skyblue")
            ax.set_title(f'Distribution of {column}')
            st.pyplot(fig)

        with col2:
            st.subheader("📦 Boxplot")
            fig2, ax2 = plt.subplots()
            sns.boxplot(x=df[column], ax=ax2, color="lightgreen")
            ax2.set_title(f'Boxplot of {column}')
            st.pyplot(fig2)
    else:
        st.subheader("📊 Count Plot")
        fig, ax = plt.subplots(figsize=(8, 4))
        df[column].value_counts().head(15).plot(kind='bar', color="salmon", ax=ax)
        ax.set_title(f'Count Plot of {column}')
        ax.set_ylabel("Count")
        st.pyplot(fig)

# === BIVARIATE ===
elif analysis_type == "Bivariate":
    st.header("🔗 Bivariate Analysis")
    col1 = st.selectbox("📌 Select first column (numeric)", df.select_dtypes(include='number').columns)
    col2 = st.selectbox("🆚 Select second column", df.columns)

    if pd.api.types.is_numeric_dtype(df[col1]) and pd.api.types.is_numeric_dtype(df[col2]):
        st.subheader("📈 Scatter Plot")
        fig, ax = plt.subplots()
        sns.scatterplot(x=df[col1], y=df[col2], ax=ax, color="orange")
        ax.set_title(f'Scatter Plot: {col1} vs {col2}')
        st.pyplot(fig)

    elif pd.api.types.is_numeric_dtype(df[col1]) and not pd.api.types.is_numeric_dtype(df[col2]):
        st.subheader("📦 Boxplot Grouped by Category")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.boxplot(x=df[col2], y=df[col1], ax=ax, palette="Set2")
        ax.set_title(f'Boxplot of {col1} grouped by {col2}')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right")
        st.pyplot(fig)
    else:
        st.warning("⚠️ Bivariate plot not available for selected combination.")

# === MULTIVARIATE ===
elif analysis_type == "Multivariate":
    st.header("📊 Multivariate Analysis")

    # --- Correlation Heatmap ---
    st.subheader("🔥 Correlation Heatmap")
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    selected_cols = st.multiselect("Select numeric columns for heatmap", numeric_cols, default=numeric_cols[:5])

    if len(selected_cols) >= 2:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(df[selected_cols].corr(), annot=True, cmap='coolwarm', ax=ax)
        ax.set_title("Correlation Heatmap")
        st.pyplot(fig)
    else:
        st.info("ℹ️ Select at least two numeric columns to generate the heatmap.")

    # --- Plot with Hue ---
    st.subheader("🎯 Scatter / Bar Plot with Hue")
    all_cols = df.columns.tolist()
    x_col = st.selectbox("Select X-axis column", all_cols, key='xcol')
    y_col = st.selectbox("Select Y-axis column", all_cols, key='ycol')
    hue_col = st.selectbox("Select Hue (grouping) column", [None] + all_cols, key='huecol')

    plot_type = st.radio("Select plot type", ("Scatter Plot", "Bar Plot"))

    if x_col and y_col:
        try:
            fig, ax = plt.subplots(figsize=(10, 5))
            if plot_type == "Scatter Plot":
                sns.scatterplot(data=df, x=x_col, y=y_col, hue=hue_col if hue_col else None, ax=ax)
            else:
                sns.barplot(data=df, x=x_col, y=y_col, hue=hue_col if hue_col else None, ax=ax)
            ax.set_title(f'{plot_type} of {y_col} vs {x_col} grouped by {hue_col}')
            ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right")
            st.pyplot(fig)
        except Exception as e:
            st.error(f"❌ Plotting failed: {e}")
