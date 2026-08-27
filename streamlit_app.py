import os
import streamlit as st
from snowflake.snowpark.functions import col
import requests  

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")

st.write("""Choose the fruits you want in your Smoothie!""")


name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your smoothie will be ", name_on_order)

cnx= st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# 1. Name this 'ingredients_list' so it holds the selected items
ingredients_list = st.multiselect("Choose up to 5 ingredients:", my_dataframe, max_selections=5)

# 2. Check if the list is not empty
if ingredients_list:
    ingredients_string = ''

    # 3. Loop through the list to build your text string
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")  
        sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
    #st.write(ingredients_string)

    # 4. Construct the SQL statement
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
                    values ('""" + ingredients_string + """', '""" + name_on_order + """' )"""

   
    
    time_to_insert = st.button('Submit Order')

    #st.write(my_insert_stmt)
    #st.stop()

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered,' + name_on_order + '!', icon="✅")





