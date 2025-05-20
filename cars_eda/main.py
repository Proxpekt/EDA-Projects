import streamlit as st
# from PIL import Image  # Uncomment if using an image

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Cars EDA Project",
    page_icon="🚗",
    layout="centered"
)

# -------------------------------
# Title and Header Section
# -------------------------------
st.title("🚗 Used Cars EDA Dashboard")
st.subheader("Gain Data-Driven Insights into the Second-Hand Car Market")

# -------------------------------
# Optional Image Display
# -------------------------------
# If you want to include an image in your dashboard, make sure 'cars.jpg' is in the same folder.
# car_image = Image.open("cars.jpg")
# st.image(car_image, caption="Used Cars Market Analysis", use_column_width=True)

# -------------------------------
# Problem Statement Section
# -------------------------------
st.markdown("""
### 📌 Problem Statement

The used car market is booming, yet many buyers and sellers lack clear, data-backed insights when evaluating vehicle value and market behavior.

This project presents an **Exploratory Data Analysis (EDA)** on a dataset of used car listings to uncover trends and relationships among key features such as:

- 🚙 **Location**
- 🏷️ **Brand & Model**
- 🛠️ **Manufacturing Year & Mileage**
- ⛽ **Fuel Type**
- 💰 **Price**

By visualizing and interpreting these variables, this dashboard helps users:
- Understand pricing trends across cities and brands.
- Detect depreciation patterns over mileage and age.
- Compare fuel types and their pricing implications.

Whether you're a buyer, seller, or analyst — this EDA equips you with actionable insights to **make informed decisions** in the used car space.
""")

# -------------------------------
# Navigation Instructions
# -------------------------------
st.markdown("---")
st.markdown("📊 **Navigate using the sidebar** to explore the dataset, visualizations, and detailed breakdowns of car features and pricing.")
