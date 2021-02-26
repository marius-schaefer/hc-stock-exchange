from init_db import *
import os
from slack_bolt import App
from slackbot_utils import *




#checks if all-stocks table exists in the db
all_stocks_table = check_for_table('all-stocks')
creates all-stocks table if the table does not exist
if not all_stocks_table:
    create_all_stocks_table()

#checks if stock table exists in the db
stock_table = check_for_table('stock')
creates stock table if the table does not exist
if not stock_table:
    create_stock_table()

#checks if trades table exists in the db
trades_table = check_for_table('trades')
creates trades table if the table does not exist
if not trades_table:
    create_trades_table()

#checks if stock-creator table exists in the db
stock_creator_table = check_for_table('stock-creator')
creates stock-creator table if the table does not exist
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


# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))