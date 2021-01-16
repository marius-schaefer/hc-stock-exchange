from overseer_utils import *

#stock price calculation function:
def stock_price_calculate(user_id, amount_of_transactions):
    message_amount = int(get_user_message_count(user_id))
    stock_price = (((message_amount//100) * 50) + (amount_of_transactions * 50))// 100
    return stock_price

