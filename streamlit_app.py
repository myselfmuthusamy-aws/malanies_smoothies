# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests  

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("""Choose the fruits you want in your custome Smoothies!""")


name_on_order = st.text_input("Name on Smoothies")
st.write("The name on your smoothie will be:", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

# session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))


# st.write(f"Current role: {session.get_current_role()}")
# st.write(f"current database/schema: {session.get_current_database()}")

ingredients_list = st.multiselect(
    "Choose upto 5 ingredients?",
    my_dataframe,
    max_selections=5,
    accept_new_options=True,
)
if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)
    
    ingredients_string = ""
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    st.write(ingredients_string)




    my_insert_stmt = f"""
insert into smoothies.public.orders (INGREDIENTS, NAME_ON_ORDER)
values ('{ingredients_string}', '{name_on_order}')
"""


    st.write(my_insert_stmt)
    # st.stop()

    # if ingredients_string:
    #     session.sql(my_insert_stmt).collect()
    
    timer_to_insert = st.button("Submit Order")
    if timer_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success(f"Your Smoothie is ordered, {name_on_order}!", icon="✅")    

# st.write(my_insert_stmt)
# st.dataframe(data = my_dataframe, use_container_width = True)


# smoothiefroot_response = requests.get("[https://my.smoothiefroot.com/api/fruit/watermelon](https://my.smoothiefroot.com/api/fruit/watermelon)")  
# st.text(smoothiefroot_response)


smoothiefroot_response = requests.get(
    "https://my.smoothiefroot.com/api/fruit/watermelon"
)

st.text(smoothiefroot_response.text)
