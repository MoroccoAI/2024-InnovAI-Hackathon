import altair as alt
import pandas as pd
import streamlit as st

THRESHOLD = 10
materials = ['Shower', 'Bathtub', 'Faucet', 'Washing Machine', 'Dishwasher',
             'Water Heater', 'Irrigation System', 'Water Filter', 'Other']


df = pd.read_csv("data/user_data.csv")
df_melted = df.drop(columns=["Price"]).melt("Month", var_name="Category", value_name="Liters")

user_name = "John Bob"
current_water_usage = df.iloc[-1]['User Water Usage (liters)']
city_threshold = f"{THRESHOLD} liters"


# App layout
st.set_page_config(layout="wide")
st.title("Water Usage")

# User details
col1, col2 = st.columns(2)
with col1:
    st.subheader("User Details")
    st.info(f"**First Name:** {user_name.split()[0]}")
    st.info(f"**Last Name:** {user_name.split()[1]}")

with col2:
    st.subheader("Last month Water Usage")
    st.warning(f"**Water Usage:** {current_water_usage} liters")
    st.warning(f"**City Threshold:** {city_threshold}")


# Users material
st.subheader("Select Water-Related Materials/Devices")

if "selected_materials" not in st.session_state:
    st.session_state.selected_materials = []

# Create checkboxes for each material
cols = st.columns(3)

for i, material in enumerate(materials):
    col_idx = i % 3
    with cols[col_idx]:
        if st.checkbox(material, value=(material in st.session_state.selected_materials)):
            # Add to session state if selected
            if material not in st.session_state.selected_materials:
                st.session_state.selected_materials.append(material)
        else:
            # Remove from session state if unchecked
            if material in st.session_state.selected_materials:
                st.session_state.selected_materials.remove(material)

# Plots
col1, col2 = st.columns(2)

st.header("Track your water usage")

chart = (
    alt.Chart(df_melted)
    .mark_line(point=True)
    .encode(
        x=alt.X("Month:T", title="Month"),
        y=alt.Y("Liters:Q", title="Liters"),
        color=alt.Color("Category:N", title="Category"),
        tooltip=["Month:T", "Category:N", "Liters:Q"],
    )
    .properties(
        width=800,
        height=400,
        title="Water Usage Evolution"
    )
    .interactive()
)

price_chart = (
    alt.Chart(df)
    .mark_line(color="red", point=True)
    .encode(
        x=alt.X("Month:T", title="Month"),
        y=alt.Y("Price:Q", title="Price (in MAD)"),
        tooltip=["Month:T", "Price:Q"],
    )
    .properties(
        width=800,
        height=200,
        title="Monthly Price Paid (MAD)",
    )
    .interactive()
)

st.altair_chart(price_chart, use_container_width=True)
st.altair_chart(chart, use_container_width=True)
