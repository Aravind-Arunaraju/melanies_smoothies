# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

if ingredients_list:

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    ingredients_string = ingredients_string.strip()  # remove trailing space

    my_insert_stmt = f"""INSERT INTO smoothies.public.orders(ingredients, name_on_order)
                         VALUES ('{ingredients_string}','{name_on_order}')"""

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")



#New section to display smoothiefroot nutrition information
# import requests
# smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
# # st.text(smoothiefroot_response.json())
# sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)

# import streamlit as st
import requests
# import pandas as pd

# Get the response from the API
response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
data = response.json()

# Extract common metadata and nutrition details
common_info = {
    "family": data["family"],
    "genus": data["genus"],
    "id": data["id"],
    "name": data["name"],
    "order": data["order"]
}

# Convert nutrition dict to rows with shared metadata
nutrition_data = []
for nutrient, value in data["nutritions"].items():
    row = {
        "nutrition_type": nutrient,
        **common_info,
        "nutrition": value
    }
    nutrition_data.append(row)

# Convert to DataFrame and set index to 'nutrition_type' for better view
df = pd.DataFrame(nutrition_data).set_index("nutrition_type")

# Display in Streamlit
st.dataframe(df, use_container_width=True)
