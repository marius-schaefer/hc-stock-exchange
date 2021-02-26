from init_db import *
import os
from slack_bolt import App
from slackbot_utils import *
from hn_utils import *
import time




#checks if all-stocks table exists in the db
all_stocks_table = check_for_table('all-stocks')
#creates all-stocks table if the table does not exist
if not all_stocks_table:
    create_all_stocks_table()

#checks if stock table exists in the db
stock_table = check_for_table('stock')
#creates stock table if the table does not exist
if not stock_table:
    create_stock_table()

#checks if trades table exists in the db
trades_table = check_for_table('trades')
#creates trades table if the table does not exist
if not trades_table:
    create_trades_table()

#checks if stock-creator table exists in the db
stock_creator_table = check_for_table('stock-creator')
#creates stock-creator table if the table does not exist
if not stock_creator_table:
   create_stock_creator_table


# Initializes your app with your bot token and signing secret
app = App(
    token='TOKEN',
    signing_secret='SIGNING SECRET'
)



# Listens to incoming messages that contain "hello"
@app.message("!hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(f"Hey there <@{message['user']}>!")


@app.command('/buy-stocks')
def open_buy_modal_1(ack, body, client):
    ack()
    buy_modal_1(ack, body, client)


@app.view('buy_modal_1')
def update_to_buy_modal_2(ack, body, client, view):
    stock_to_buy = view['state']['values']['static_select']['stock-to-buy']
    stock_symbol_to_buy = stock_to_buy.split('"')
    stock_symbol = stock_symbol_to_buy[1]

    ack()

    buy_modal_2(ack, body, client, stock_symbol)


@app.view('buy_modal_2')
def update_to_buy_modal_3(ack, body, client, view):
    stock_symbol_plus_amount = view['state']['values']['static_select']['amount-to-buy']
    
    ack()

    buy_modal_3(ack, body, client, stock_symbol_plus_amount)


@app.view('buy_modal_3')
def handle_submitted_buy_modal_data(ack, body, client, view):
    #Getting Data from the submitted modals
    user=body["user"]["id"]
    values=view['title']['text']

    #Spliting values inorder to get the stock symbol and amount
    split_values = values.split(' ')

    #Setting amount and stock_symbol variables = to the data
    amount = split_values[1]
    stock_symbol = split_values[2]

    #getting the price of the stock:
    stock_price = get_stock_price(stock_symbol)
    
    #Calculating the amount the total price:
    amount = int(amount)
    total_price = stock_price * amount

    #Create an invoice:
    create_invoice(total_price, user)

    #Sleep for 3 minutes and then check for a hn transaction
    time.sleep(180)
    if check_for_hn_transaction(user, total_price):
        set_stock_owner_plus_payout(stock_symbol, user, amount)
    else:
        pass



# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))