from slack_bolt import App
from db_utils import *


def buy_modal_1(ack, body, client):
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