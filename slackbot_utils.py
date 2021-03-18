from slack_bolt import App
from db_utils import *


def buy_modal_1(client):
    all_availble_stocks = get_all_available_stock_data()

    view_template = {
	"type": "modal",
	"callback_id": "buy_modal_1",
	"title": {
		"type": "plain_text",
		"text": "Hack Club Stock Exchange",
		"emoji": True
	},
	"submit": {
		"type": "plain_text",
		"text": "Proceed"
	},
	"close": {
		"type": "plain_text",
		"text": "Cancel",
		"emoji": True
	},
	"blocks": [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Buy Stocks:",
				"emoji": True
			}
		},
		{
			"type": "divider"
		},
		{
            "block_id" : "static_select",
            "type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Choose a stock to buy:*"
			},
			"accessory": {
				"type": "static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select a stock",
					"emoji": True
				},
				"options": [
				],
				"action_id": "stock-to-buy"
			}
		}
	]
}

    value = 0
    for stock in all_availble_stocks:
        option = {
						"text": {
							"type": "plain_text",
							"text": f'{stock["stock_name"]} ("{stock["stock_symbol"]}") |Price: {stock["stock_price"]}hn',
							"emoji": True
						},
						"value": f"value-{value}"
					}
        view_template['blocks'][2]['accessory']['options'].append(option)
        value += 1
    
    client.views_open(
        trigger_id=body["trigger_id"],
        view=view_template
    )


def buy_modal_2(ack, body, client, stock_symbol):
    amount_available = get_amount_of_available_stocks(stock_symbol)

    view_template = {
	"type": "modal",
	"callback_id": "buy_modal_2",
	"title": {
		"type": "plain_text",
		"text": "Hack Club Stock Exchange",
		"emoji": True
	},
	"submit": {
		"type": "plain_text",
		"text": "Proceed"
	},
	"close": {
		"type": "plain_text",
		"text": "Cancel",
		"emoji": True
	},
	"blocks": [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Select the amount you would like to buy:",
				"emoji": True
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"block_id": "static_select",
			"text": {
				"type": "mrkdwn",
				"text": "*Choose the amount you would like to buy:*"
			},
			"accessory": {
				"type": "static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select amount",
					"emoji": True
				},
				"options": [
				],
				"action_id": "amount-to-buy"
			}
		}
	]
}

    value = 0
    stock_amount = 0
    for stock in amount_available:
        stock_amount += 1
        option = {
						"text": {
							"type": "plain_text",
							"text": f'{stock_symbol}-{stock_amount}',
							"emoji": True
						},
						"value": f"value-{value}"
					}
        view_template['blocks'][2]['accessory']['options'].append(option)
        value += 1


    client.views_open(
        trigger_id=body["trigger_id"],
        view=view_template
    )


def buy_modal_3(ack, body, client, stock_symbol_plus_amount):
    values = stock_symbol_plus_amount.split('-')
    stock_symbol = values[0]
    amount = values[1]

    client.views_open(
        trigger_id=body["trigger_id"],
        view={
	"type": "modal",
	"callback_id": "buy_modal_3",
	"title": {
		"type": "plain_text",
		"text": f"Buy {amount} {stock_symbol}",
		"emoji": True
	},
	"submit": {
		"type": "plain_text",
		"text": "Proceed"
	},
	"close": {
		"type": "plain_text",
		"text": "Cancel",
		"emoji": True
	},
	"blocks": [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "What to do next:",
				"emoji": True
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "context",
			"elements": [
				{
					"type": "mrkdwn",
					"text": "*To pay for the stocks you would like to buy follow the following instructions:* Make sure you have an hn account, if you do not click cancel and make one. Once you have made one try again. Now, *once you press submit you will receive an invoice for the amount of HN that you have to pay* for in order to buy the stocks. *Check your HN Dashboard, and /pay* in order to pay the appropriate amount of HN. Once you have done, that the stocks will be yours! If you encounter any errors contact @Marius S. "
				}
			]
		}
	]
}
    )


#Modal for Getting the User_ID
def sell_modal_1(client):
	client.views_open(
		trigger_id=body["trigger_id"],
		view={
	"type": "modal",
	"callback_id": "sell_modal_1",
	"title": {
		"type": "plain_text",
		"text": "Hack Club Stock Exchange",
		"emoji": True
	},
	"submit": {
		"type": "plain_text",
		"text": "Proceed",
		"emoji": True
	},
	"close": {
		"type": "plain_text",
		"text": "Cancel",
		"emoji": True
	},
	"blocks": [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "If you would like to proceed with selling stocks press proceed below",
				"emoji": True
			}
		}
	]
}
	)


#Sell_modal_2 Allows the user to select what stock to sell and how much:
def sell_modal_2(ack, body, client, user):
	portfolio = get_portfolio(user)
	
	view_template = {
	"type": "modal",
	"callback_id": "sell_modal_2",
	"title": {
		"type": "plain_text",
		"text": "Hack Club Stock Exchange",
		"emoji": True
	},
	"submit": {
		"type": "plain_text",
		"text": "Proceed",
		"emoji": True
	},
	"close": {
		"type": "plain_text",
		"text": "Cancel",
		"emoji": True
	},
	"blocks": [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Select what stock you would like to sell:",
				"emoji": True
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Choose a stock to sell:"
			},
			"accessory": {
				"type": "static_select",
				"block_id" : "static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select an item",
					"emoji": True
				},
				"options": [

				],
				"action_id": "stock-to-sell"
			}
		}
	]
}
	portfolio_stocks = []
	for stock in portfolio:
		portfolio_stocks.append(stock)

	#For loop that adds a block for every stock that a user owns:
	value = 0
	for stock in portfolio_stocks:
        option = {
						"text": {
							"type": "plain_text",
							"text": f'{stock}',
							"emoji": True
						},
						"value": f"value-{value}"
					}
        view_template['blocks'][1]['accessory']['options'].append(option)
        value += 1

	client.views_open(
		trigger_id=body["trigger_id"],
		view=view_template
	)
 

def sell_modal_3(ack, body, client, user, stock_name):
	portfolio = get_portfolio(user)
	amount_available =  portfolio[stock_name]
	stock_symbol = get_stock_symbol(stock_name)

	view_template = {
	"type": "modal",
	"callback_id": "sell_modal_3",
	"title": {
		"type": "plain_text",
		"text": "Hack Club Stock Exchange",
		"emoji": true
	},
	"submit": {
		"type": "plain_text",
		"text": "Sell",
		"emoji": true
	},
	"close": {
		"type": "plain_text",
		"text": "Cancel",
		"emoji": true
	},
	"blocks": [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Select the amount you would like to sell:",
				"emoji": true
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Choose the amount to sell:"
			},
			"accessory": {
				"type": "static_select",
				"block_id" : "static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select an item",
					"emoji": true
				},
				"options": [

				],
				"action_id": "amount-to-sell"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*As soon as you press sell, the stocks will be made available for purchase on the market!*"
			}
		}
	]
}

	#For Loop that adds the options to view_template:
	value = 0
    stock_amount = 0
    for stock in amount_available:
        stock_amount += 1
        option = {
						"text": {
							"type": "plain_text",
							"text": f'{stock_symbol}-{stock_amount}',
							"emoji": True
						},
						"value": f"value-{value}"
					}
        view_template['blocks'][1]['accessory']['options'].append(option)
        value += 1

	client.views_open(
		trigger_id=body["trigger_id"],
		view=view_template
	)


def error_modal(ack, body, client):
	client.views_open(
		trigger_id=body["trigger_id"],
		view={
	"type": "modal",
	"title": {
		"type": "plain_text",
		"text": "Hack Club Stock Exchange",
		"emoji": true
	},
	"close": {
		"type": "plain_text",
		"text": "Cancel",
		"emoji": true
	},
	"blocks": [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "There has been an Error, Contact @Marius S., and inform him of the error! ",
				"emoji": true
			}
		}
	]
}
	)


def stock_creation_modal(ack, body, client)
	client.views_open(
		trigger_id=body["trigger_id"],
		view={
	"title": {
		"type": "plain_text",
		"text": "Hack Club Stock Exchange",
		"emoji": True
	},
	"submit": {
		"type": "plain_text",
		"text": "Proceed"
	},
	"type": "modal",
	"callback_id": "stock_creation_modal",
	"close": {
		"type": "plain_text",
		"text": "Cancel",
		"emoji": True
	},
	"blocks": [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Create a Stock:",
				"emoji": True
			}
		},
		{
			"type": "context",
			"elements": [
				{
					"type": "mrkdwn",
					"text": "Fill in the fields with the appropriate information. Press proceed when done, if you have not created a stock already and the stock you wish to create does not exist yet, you will receive further instructions. Otherwise you will receive an Error Message."
				}
			]
		},
		{
			"type": "input",
			"block_id" : "stock_name_input_block",
			"element": {
				"type": "plain_text_input",
				"action_id": "stock_name"
			},
			"label": {
				"type": "plain_text",
				"text": "Stock Name (Example: Corgi Coin)",
				"emoji": True
			}
		},
		{
			"type": "input",
			"block_id" : "stock_symbol_input"
			"element": {
				"type": "plain_text_input",
				"action_id": "stock_symbol"
			},
			"label": {
				"type": "plain_text",
				"text": "Stock Symbol/Ticker  (Example: DOGE, Tip: try keep it short and simple/memorable!)",
				"emoji": True
			}
		}
	]
}
	)


def stock_created_notif(client):
	client.views_open(
		trigger_id=body["trigger_id"],
		view={
	"title": {
		"type": "plain_text",
		"text": "Hack Club Stock Exchange",
		"emoji": True
	},
	"type": "modal",
	"callback_id": "buy_modal_3",
	"close": {
		"type": "plain_text",
		"text": "Close",
		"emoji": True
	},
	"blocks": [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Congratulations on creating your own stock! In order to sell your stock use the command /sell-stocks!",
				"emoji": True
			}
		}
	]
}
	)


def stock_creation_modal_2(ack, body, client)
	client.views_open(
		trigger_id=body["trigger_id"],
		view={
	"title": {
		"type": "plain_text",
		"text": "Hack Club Stock Exchange",
		"emoji": true
	},
	"type": "modal",
	"callback_id": "buy_modal_3",
	"close": {
		"type": "plain_text",
		"text": "Close",
		"emoji": true
	},
	"blocks": [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Just one last step...",
				"emoji": true
			}
		},
		{
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": "In order to create a stock you will have to pay a one time fee of 75 HN. In order to pay the one time fee, go to your HN dashboard and pay the appropriate invoice using /pay ! Once you have payed the appropriate invoice your stock will be created immeadietly. If not of course contact @Marius S.!",
				"emoji": true
			}
		}
	]
}
	)


def open_dashboard(client, event, logger)
	total_amount_of_stocks = 0
	total_value = 0
	
	view_template = {
	"type": "home",
	"blocks": [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Your HSE Dashboard ",
				"emoji": True
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"*Total Amount of Stocks:* {total_amount_of_stocks}"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"*Total Value of all Stocks:* {total_value}"
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Your Stocks:",
				"emoji": True
			}
		},
	]
}
	action_extension = [{
			"type": "divider"
		},
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Actions:",
				"emoji": True
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Buy Stocks*"
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "Buy Stocks",
					"emoji": True
				},
				"value": "click_me_123",
				"action_id": "buy_button"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Sell Stocks*"
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "Sell Stocks",
					"emoji": True
				},
				"value": "click_me_123",
				"action_id": "sell_button"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Give Stocks*"
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "Give Stocks",
					"emoji": True
				},
				"value": "click_me_123",
				"action_id": "button-action"
			}
		}]	
	user = event["user"]
	portfolio = get_portfolio(user)
	
	if len(portfolio) == 0:
		no_stocks_extension = {
			"type": "context",
			"elements": [
				{
					"type": "plain_text",
					"text": "At the moment you do not own any stocks, to purchase stocks press the buy stocks button below!",
					"emoji": True
				}
			]
		}
		view_template['blocks'].append(no_stocks_extension)
		view_template['blocks'].extend(action_extension)
	else:
		for stock in portfolio:
			stock_name = stock
			stock_symbol = get_stock_symbol(stock)
			stock_price = get_stock_price(stock)
			amount = portfolio[stock]
			stock_value = stock_price * amount
			mrkdwn_format_template = {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"*{stock_name}* ({stock_symbol}) | *{amount} Stocks* | Price per Stock: {stock_price} HN | Total Value: {stock_value} HN"
			}
		}
			view_template['blocks'].append(mrkdwn_format_template)
			total_amount_of_stocks += amount
			total_value += stock_value
		view_template['blocks'].extend(action_extension)

	try:
		client.views_publish(
			user_id=event["user"],
			view=view_template
		)
	except Exception as e:
		logger.error(f"Error publishing home tab: {e}")


