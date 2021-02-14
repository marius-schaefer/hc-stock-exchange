import sqlite3


def get_stock_price(stock):
    #This function will allow the stock price to be found through either inputing a stock symbol
    # or the full stock name, therefore the try and except
    try:
        # attempts to get the price with full stock name
        #creates or connects to an existing db
        conn = sqlite3.connect('hse.db')
        #creates cursor
        c = conn.cursor()

        #Selecting the data we want:
        c.execute("SELECT * FROM stock WHERE stock_name = ? ", (stock,))

        #Actually getting the price and storing it in the variale price
        price = c.fetchone()

        if price == None:
            pass
        else:
            return price[2]
    except:
        pass
    try:
        #attempts to get the price with stock symbol
        #creates or connects to an existing db
        conn = sqlite3.connect('hse.db')
        #creates cursor
        c = conn.cursor()

        #Selecting the data we want:
        c.execute("SELECT * FROM stock WHERE stock_symbol = ? ", (stock,))
        
        #Actually getting the price and storing it in the variale price
        price = c.fetchone()
        if price == None:
            pass
        else:
            return price[2]
    except:
        #tell main.py to send an error messgae
        return None


def set_stock_owner(stock_symbol, owner, new_owner, amount):
    #Amount refers to the amount of stocks that should be transfered to the new owner 
    #creates or connects to an existing db
    conn = sqlite3.connect('hse.db')
    #creates cursor
    c = conn.cursor()

    #Inputing what we want to do:
    c.execute("""UPDATE all-stocks SET stock_owner = ? 
                WHERE stock_owner = ? AND stock_symbol = ? LIMIT ?""", (new_owner, owner, stock_symbol, amount,))
    #Executing our instructions from above:
    conn.commit()
    #closing the db:
    conn.close()


def set_stock_as_available(stock_symbol, owner, amount):
    #creates or connects to an existing db
    conn = sqlite3.connect('hse.db')
    #creates cursor
    c = conn.cursor()

    #Inputing what we want to do
    c.execute("""UPDATE all-stocks SET available = True
                WHERE stock_owner = ? AND stock_symbol = ? LIMIT ?""", (owner, stock_symbol, amount))
    
    #Executing our instructions from above:
    conn.commit()
    #closing the db:
    conn.close()


def set_stock_as_unavailable(stock_symbol, owner, amount):
    #creates or connects to an existing db
    conn = sqlite3.connect('hse.db')
    #creates cursor
    c = conn.cursor()

    #Inputing what we want to do
    c.execute("""UPDATE all-stocks SET available = False
                WHERE stock_owner = ? AND stock_symbol = ? LIMIT ?""", (owner, stock_symbol, amount))
    
    #Executing our instructions from above:
    conn.commit()
    #closing the db:
    conn.close()


def get_portfolio(user):
    #creates or connects to an existing db
    conn = sqlite3.connect('hse.db')
    #creates cursor
    c = conn.cursor()

    #Selecting the data we want:
    c.execute("""SELECT * FROM all-stocks WHERE stock_owner = ?""", (user,))

    #Actually getting the data and storing it in the variable stocks
    stocks = c.fetchall()

    conn.commit()
    conn.close()

    #Creating the dictionary that will be used to count the stocks in the portfolio
    portfolio = {}

    #Counting the total stocks:
    for stock in stocks:
        if stock[1] not in portfolio:
            portfolio.update({stock[1]:1})
        else:
            portfolio[stock[1]] += 1
    
    #Once the stocks in the portfolio have been counted, the function returns the dictionary:
    return portfolio


def get_top_stocks():
    #creates or connects to an existing db
    conn = sqlite3.connect('hse.db')
    #creates cursor
    c = conn.cursor()

    #Selecting the data we want to get from the db
    c.execute("SELECT * FROM stock ORDER BY stock_price DESC LIMIT 10")

    #Getting the data we selected:
    top_stocks = c.fetchall()

    conn.commit()
    conn.close()

    return top_stocks


def check_if_can_be_sold(owner, stock_symbol, amount):
    #creates or connects to an existing db
    conn = sqlite3.connect('hse.db')
    #creates cursor
    c = conn.cursor()

    #Selecting the data we want to get from the db
    c.execute("SELECT * FROM all-stocks WHERE stock_symbol = ? AND stock_owner = ?", (stock_symbol, owner))

    #Getting the data we selected:
    stocks = c.fetchall()

    conn.commit()
    conn.close()

    #Comparing the amount of stocks owned by the user to the amount the user wishes to sell:
    amount_in_possesion = len(stocks)
    if amount <= amount_in_possesion:
        return True
    else:
        return False


def check_stock_creation_conditions(user_id):
    #This Function will return True if a user can create a stock
    #user_id = Slack user id

    #creates or connects to an existing db
    conn = sqlite3.connect('hse.db')
    #creates cursor
    c = conn.cursor()
    
    #Selecting the data we want to get from the db
    c.execute("SELECT * FROM stock-creator WHERE stock_creator = ?", (user_id,))

    #Getting the data we selected:
    created_stock = c.fetchall()

    if created_stock == None:
        return True
    else:
        return False