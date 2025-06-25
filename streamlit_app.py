# Import necessary packages
import streamlit as st
from snowflake.snowpark.functions import col

# Set Streamlit page title
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Input field
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Access the table
fruit_table = session.table("smoothies.public.fruit_options")

# Get the list of column names from the Snowflake table
columns = fruit_table.columns
st.write("🔍 Columns (from Snowpark):", columns)

# Check if 'SEARCH_ON' column exists
if "SEARCH_ON" in columns:
    st.success("✅ 'SEARCH_ON' column is available in the table.")
else:
    st.warning("⚠️ 'SEARCH_ON' column not found. Check for case sensitivity or recent schema changes.")

# Display sample data from the table
st.write("📊 Sample data:")
st.dataframe(fruit_table.limit(10).to_pandas(), use_container_width=True)
