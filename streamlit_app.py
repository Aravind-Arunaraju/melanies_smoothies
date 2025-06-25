# Import necessary packages
import streamlit as st
from snowflake.snowpark.functions import col

# Title
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Input field
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Get the table object
fruit_table = session.table("smoothies.public.fruit_options")

# Get and display the actual column names (case-sensitive)
columns = fruit_table.columns
st.write("Columns in the table:", columns)

# Optional: Display a preview of the data
st.write("Sample data:")
st.dataframe(fruit_table.limit(10).to_pandas(), use_container_width=True)
