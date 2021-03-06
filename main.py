from init_db import *
import os
from slack_bolt import App
from slackbot_utils import *
from hn_utils import *
from db_utils import *
import time




#checks if all-stocks table exists in the db
all_stocks_table = check_for_table('allstocks')
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
stock_creator_table = check_for_table('stockcreator')
#creates stock-creator table if the table does not exist
if not stock_creator_table:
   create_stock_creator_table()


# Initializes your app with your bot token and signing secret
app = App(
    token='PUT TOKEN HERE',
    signing_secret='PUT SIGNING SECRET HERE'
)


# Listens to incoming messages that contain "hello"
@app.message("!hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(f"Hey there <@{message['user']}>!")


#
#BUY COMMAND + MODAL 
#
@app.command('/buy-stocks')
def open_buy_modal_1(ack, body, client):
    ack()
    buy_modal_1(client, body)


@app.view('buy_modal_1')
def update_to_buy_modal_2(ack, body, client, view):
    stock_to_buy = view['state']['values']['static_select']['stock-to-buy']['selected_option']['text']['text']
    stock_symbol_to_buy = stock_to_buy.split('"')
    stock_symbol = stock_symbol_to_buy[1]

    ack()

    buy_modal_2(ack, body, client, stock_symbol)


@app.view('buy_modal_2')
def update_to_buy_modal_3(ack, body, client, view):
    stock_symbol_plus_amount = view['state']['values']['static_select']['amount-to-buy']['selected_option']['text']['text']
    
    ack()

    buy_modal_3(ack, body, client, stock_symbol_plus_amount)


@app.view('buy_modal_3')
def handle_submitted_buy_modal_data(ack, body, client, view):
    #Getting Data from the submitted modals
    user=body["user"]["id"]
    values=view['title']['text']
    ack()
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
    time.sleep(120)
    if check_for_hn_transaction(user, total_price):
        set_stock_owner_plus_payout(stock_symbol, user, amount)
    else:
        pass


#
#SELL COMMAND + MODAL:
#
@app.command('/sell-stocks')
def open_sell_modal(ack, body, client):
    ack()
    sell_modal_1(client, body)


#Once Sell_modal_1 is submitted, gets the user ID and triggers the second sell modal:
@app.view('sell_modal_1')
def update_to_sell_modal_2(ack, body, client, view):
    user=body["user"]["id"]
    ack()

    #Opens the second sell_modal:
    sell_modal_2(ack, body, client, user)


#Once Sell_modal_2 is submitted gets the selected stock and opens the third sell_modal:
@app.view('sell_modal_2')
def update_to_sell_modal_3(ack, body, client, view):
    user=body["user"]["id"]
    stock_name = view['state']['values']['static_select']['stock-to-sell']['selected_option']['text']['text']
    ack()
    sell_modal_3(ack, body, client, user, stock_name)
    

@app.view('sell_modal_3')
def update_to_sell_modal_4(ack, body, client, view):
    user=body["user"]["id"]
    amount_to_sell = view['state']['values']['static_select']['amount-to-sell']['selected_option']['text']['text']
    split_amount_to_sell = amount_to_sell.split('-')
    ack()
    stock_symbol = split_amount_to_sell[0]
    amount = split_amount_to_sell[1]
    amount = int(amount)
    if check_if_can_be_sold(user, stock_symbol, amount) == True:
        set_stock_as_available(stock_symbol, user, amount)
    else:
        error_modal(ack, body, client)


#
#TAKE OFF MARKET COMMAND:
#
@app.command('/take-off-market')
def take_off_market(ack, command, respond):
    ack()
    user = command['user']
    stock_symbol_plus_amount = command['text']
    stock_symbol_plus_amount = stock_symbol_plus_amount.split(' ')
    stock_symbol = stock_symbol_plus_amount[0]
    amount = int(stock_symbol_plus_amount[1])
    try:
        set_stock_as_unavailable(stock_symbol, user, amount)
        respond("The requested stocks have been set as unavailable for purchase", response_type=ephemeral)
    except:
        respond("An error has occured, either you do not own the stocks that you wish to take off of the market, or a bug has occured. If it is a bug please contact Marius S., informing him of the error!")


#
#CREATE STOCK COMMAND + MODAL
#
@app.command('/create-stock')
def create_stock(ack, command, body, client):
    ack()
    stock_creation_modal(ack, body, client)


@app.view("stock_creation_modal")
def stock_creation_step_2(ack, body, client, view):
    user = body["user"]["id"]
    if check_stock_creation_conditions(user) == True:
        stock_name = str(view['state']['values']['stock_name_input_block']['stock_name']['value'])
        stock_symbol = str(view['state']['values']['stock_symbol_input']['stock_symbol']['value'])
        create_invoice(75, user)
        ack()
        stock_creation_modal_2(ack, body, client)
        time.sleep(180)
        if check_for_hn_transaction(user, 75) == True:    
            add_stock_creator_to_db(user)
            add_stock_to_stock_table(stock_name, stock_symbol, user)
            add_stock_to_all_stocks_table(stock_name, stock_symbol, user)
            payout('U014DQS7AE7', 25)
            payout('UHFEGV147', 25)
            payout('U01C21G88QM', 10)
            payout('U017EPB6LE9', 5)
            payout('U015MMJ6XKP', 5)
        else:
            pass
    else:
        ack()
        error_modal(ack, body, client)


#
#Dashboard/ App Home:
#
@app.event("app_home_opened")
def update_home_tab(client, event, logger):
    open_dashboard(client, event, logger)


#
# Button Actions:
#
@app.action('buy_button')
def buy_button(ack, client, body):
    ack()
    buy_modal_1(client, body)


@app.action('sell_button')
def sell_button(ack, client, body):
    ack()
    sell_modal_1(client, body)


#
#GIVE STOCK COMMAND:
#
@app.command('/give-stocks')
def give_stock_modal(ack, client, command, body, respond):
    ack()
    command_text = command['text']
    command_text = command_text.split(' ')
    stock_symbol = command_text[0]
    amount = command_text[1]
    to_user = command_text[2]
    from_user = command['user']

    if check_if_can_be_sold(from_user, stock_symbol, amount) == True:
        set_stock_owner(stock_symbol, from_user, to_user, amount)
        respond("Stock has been given!", response_type=ephemeral)
    else:
        error_modal(ack, body, client)


# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))