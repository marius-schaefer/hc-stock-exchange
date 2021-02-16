import requests
import json
from db_utils import *


#Fucntion that finds the message count for a certain user using the Overseer API
def find_user_message_count(slack_id):
    #Url for getting overseer data
    url = 'https://github.com/KhushrajRathod/TheOverseerBackend/releases/download/Latest/results.json'
    #actually getting the data
    r = requests.get(url)

    #loading the data that was requested as json
    json_data = json.loads(r.content)

    #Finding the data for the specific user in all the json data
    index = 0
    for item in json_data:
        index += 1
        if item[0] == slack_id: 
            break
    index -= 1
    return json_data[index][1]


def update_stock_price(stock_creator):
    #Getting the data that is needed
    message_count = find_user_message_count(stock_creator)
    trade_count = get_trade_count(stock_creator)

    #Calculating the stock price and storing it in a variable:
    stock_price = (((message_count/300)*50)+(trade_count*50))//100

    #creates or connects to an existing db
    conn = sqlite3.connect('hse.db')
    #creates cursor
    c = conn.cursor()

    #Adds the data of the stock we want to add:
    c.execute("UPDATE stock SET stock_price = ? WHERE stock_creator = ?", (stock_price, stock_creator)) 

    conn.commit()
    conn.close()

