import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Dinner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#CSV Fruit List load
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

#Setting the Fruit name as an index
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])

#Let's show only the ones selected
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

#New section to display fruityvice API response
streamlit.header("Fruityvice Fruit Advice!")
#streamlit.write('The user entered ', fruit_choice)
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi') #Allow the user select a fruit
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else:
    #request the data to the API
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    # get the response json data and normalizes it
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    # show the normalized json as a table
    streamlit.dataframe(fruityvice_normalized)
except URLError as e:
  streamlit.error()
    
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select fruit_name from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

#Text input block to add fruits
fruit_choice2 = streamlit.text_input('What fruit would you like to add?','Kiwi')
streamlit.write('Thanks for adding ', fruit_choice2, '!')
