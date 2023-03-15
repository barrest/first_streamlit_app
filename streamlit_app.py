import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Favorites')

streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')

streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')

streamlit.text('🐔 Hard-Boiled Free-Range Egg')

streamlit.text('🥑🍞 Avacado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


# Display the table on the page.
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')


# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    # take the json response and add to a pandas data frame
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized


streamlit.header("Fruityvice Fruit Advice!")

try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information")
    else:
        streamlit.write('The user entered ', fruit_choice)
        back_from_function = get_fruityvice_data(fruit_choice)
        # display the dataframe
        streamlit.dataframe(back_from_function)
except URLError as e:
    streamlit.error()

streamlit.stop()
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
my_data_row = my_cur.fetchall()

streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_row)

add_fruit = streamlit.text_input("What fruit would you like to add?")
streamlit.write("Thank you for adding " + add_fruit)


my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('From Streamlit');")
