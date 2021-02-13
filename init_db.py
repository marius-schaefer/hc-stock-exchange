import sqlite3

def check_for_table(table_name):
    #creates or connects to an existing db
    conn = sqlite3.connect('hse.db')
    #creates cursor
    c = conn.cursor()

    #gets the count of tables with table_name:
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name= ? ''', (table_name,))
    if c.fetchone()[0]==1 :
        conn.commit()
        conn.close()
        return True
    else:
        conn.commit()
        conn.close()
        return False


def create_all_stocks_table():
    #creates or connects to an existing db
    conn = sqlite3.connect('hse.db')
    #creates cursor
    c = conn.cursor()

    #creates all-stocks table
    c.execute("""CREATE TABLE all-stocks (
            stock_id text,
            stock_name text,
            stock_symbol text,
            stock_owner text,
            stock_creator text,
    )""")
    
    conn.commit()
    conn.close()


def create_stock_table():
    #creates or connects to an existing db
    conn = sqlite3.connect('hse.db')
    #creates cursor
    c = conn.cursor()

    #creates stock table
    c.execute("""CREATE TABLE stock (
            stock_name text,
            stock_symbol text,
            stock_price interger,
            stock_creator text,
    )""")
    
    conn.commit()
    conn.close()


def create_trades_table():
    #creates or connects to an existing db
    conn = sqlite3.connect('hse.db')
    #creates cursor
    c = conn.cursor()

    #creates trades table
    c.execute("""CREATE TABLE trades (
            stock_symbol text,
            trade_time text,
    )""")
    
    conn.commit()
    conn.close()