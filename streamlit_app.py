
import streamlit

import requests
import pandas

import snowflake.connector
from urllib.error import URLError

streamlit.title('This is draft copy')
streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show=my_fruit_list.loc[fruits_selected]

# Display the table on the page.

streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(this_fruit_choice):
  fruityvice_response= requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

try:
  fruit_choice= streamlit.text_input('What fruit you want ?')
  if not fruit_choice:
    streamlit.error('Please select a fruit')
  else:
    data_from_function= get_fruityvice_data(fruit_choice)
    streamlit.dataframe(data_from_function)

      
except URLError as e:
  streamlit.error()







streamlit.stop()

fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
#streamlit.text(fruityvice_response.json())
# write your own comment -what does the next line do? 
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# write your own comment - what does this do?
streamlit.dataframe(fruityvice_normalized)

streamlit.stop()
#import snowflake.connector
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("Select * from fruit_load_list")
my_data_row = my_cur.fetchall()
#streamlit.text("Hello from Snowflake:")

streamlit.header("The Fruit Load List Contains:")
streamlit.dataframe(my_data_row)


add_my_fruit = streamlit.text_input('What fruit would you like to add?')
streamlit.write('The user entered ', add_my_fruit)
#my_data_row.append(add_my_fruit)
#df1=streamlit.dataframe(my_data_row)
#t1=add_my_fruit
#my_data_row.append(t1)
#df2=df1.append(add_my_fruit)
#df2

my_cur.execute("insert into fruit_load_list values('from Stearmlit')")

streamlit.dataframe(my_data_row)
