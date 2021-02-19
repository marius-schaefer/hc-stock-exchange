from init_db import *
import os
from slack_bolt import App


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
    token='PUT BOT TOKEN HERE',
    signing_secret='PUT SIGNING SECRET HERE'
)

# Listens to incoming messages that contain "hello"
@app.message("!hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(f"Hey there <@{message['user']}>!")

# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))