# Import required packages
import streamlit as st
from snowflake.snowpark.functions import col

# App UI
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Name input
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Snowflake connection
cnx = st.connection("snowflake")
session = cnx.session()

# Use quoted, case-sensitive column names
fruit_table = session.table("smoothies.public.fruit_options")

my_dataframe = fruit_table.select(
    col('"FRUIT_ID"'),
    col('"FRUIT_NAME"'),
    col('"SEARCH_ON"')
)

# Debug: Show actual selected column names
st.write("Columns in the DataFrame:", my_dataframe.schema.names)

# Show data
st.dataframe(my_dataframe.to_pandas(), use_container_width=True)
