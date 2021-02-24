from slack_bolt import App
from db_utils import *


def buy_modal_1(ack, body, client):
    all_availble_stocks = get_all_available_stock_data()

    view_template = {
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
	"type": "modal",
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
				"text": "Buy Stocks",
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
				"text": "*Choose a stock to buy:*"
			},
			"accessory": {
				"type": "static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select an item",
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
							"text": f"{stock['stock_name']} ({stock['stock_symbol']}) |Price: {stock['stock_price']}hn",
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