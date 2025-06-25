# Import necessary packages
import streamlit as st

# Set Streamlit page title
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Input field
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# ✅ Run direct SQL query to ensure all columns (including SEARCH_ON) show up
query = "SELECT * FROM smoothies.public.fruit_options"
fruit_sql_df = session.sql(query).to_pandas()

# Display the data
st.write("📊 Fruit Options (with full column list including SEARCH_ON):")
st.dataframe(fruit_sql_df, use_container_width=True)
