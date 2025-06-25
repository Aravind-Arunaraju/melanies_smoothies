# Import required packages
import streamlit as st
from snowflake.snowpark.functions import col

# App title and instructions
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# User input
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Get data with all three columns (case-sensitive handling)
my_dataframe = session.table("smoothies.public.fruit_options").select(
    col('"FRUIT_ID"'),
    col('"FRUIT_NAME"'),
    col('"SEARCH_ON"')
)

# Show table columns for verification
st.write("Columns in the DataFrame:", my_dataframe.schema.names)

# Display the result
st.dataframe(data=my_dataframe.to_pandas(), use_container_width=True)
