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