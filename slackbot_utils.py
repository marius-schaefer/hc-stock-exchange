from slack_bolt import App
from db_utils import *


def buy_modal_1(ack, body, client):
    all_availble_stocks = get_all_available_stock_data()

    view_template = {
	"type": "modal",
	"callback_id": "buy_modal",
	"title": {
		"type": "plain_text",
		"text": "Hack Club Stock Exchange",
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
				"text": "Buy Stocks:",
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
					"text": "Select a stock",
					"emoji": True
				},
				"options": [
					{
						"text": {
							"type": "plain_text",
							"text": "Ch",
							"emoji": True
						},
						"value": "value-0"
					}
				],
				"action_id": "stock-to-buy"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Once you have selected a stock click Proceed *"
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "Proceed",
					"emoji": True
				},
				"value": "click_me_123",
				"action_id": "buy-proceed-1"
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