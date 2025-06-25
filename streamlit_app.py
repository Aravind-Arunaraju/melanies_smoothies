# Import required packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# App title
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# User input
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Debug: Check current DB and Schema
st.write("Current Database:", session.get_current_database())
st.write("Current Schema:", session.get_current_schema())

# Get fresh fruit options (force evaluation)
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_ID')).to_pandas()

# Debug: Display current fruit options (will be empty if table was truncated)
st.write("Available fruit options:")
st.dataframe(my_dataframe)

# Extract list of fruit names
fruit_names = my_dataframe['FRUIT_NAME'].tolist()

# Ingredient selection
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_names,
    max_selections=5
)

# If ingredients are selected
if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)

    for fruit_chosen in ingredients_list:
        st.subheader(f"{fruit_chosen} Nutrition Information")
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{fruit_chosen}")
        try:
            st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
        except Exception as e:
            st.error(f"Failed to fetch data for {fruit_chosen}: {e}")

    # Insert order into Snowflake
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders(ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
