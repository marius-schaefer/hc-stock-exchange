from init_db import *
import slack


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
trades_table = check_for_table('stock-creator')
#creates stock-creator table if the table does not exist
if not trades_table:
    create_stock_creator_table