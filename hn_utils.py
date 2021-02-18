import requests
import os
import json

def check_for_hn_transaction(slack_id, amount, transaction_id):
    #Query:
    query = """query check_for_hn_transaction{
  user(id:"U01N29M0C9L"){
    incomingTransactions{
      amount_transacted : balance
      from{
        id
      }
      for
    }
  }
}
"""
    #Sending the Post Request and getting the data back:
    r = requests.post('https://hn.rishi.cx', json={"query":query})
    
    #Formatting the Data into JSON
    json_data = json.loads(r.content)

    #Limiting the amount of data the function will check through so it won't take forever...:
    incomingTransactions_list = json_data['data']['user']['incomingTransactions'][0:3]

    #The for loop will check if there are coresponding values in the data, if so it will return True, else False
    #In order to return False if all the data does not contain corresponding values we have the loop count
    #Once the loop count reaches the length of the Data, it will return False
    loop_count = 0
    #Length of the list stored in a variable:
    length = 3
    #Actual For loop
    for transaction_data in incomingTransactions_list:
        loop_count += 1
        if transaction_data['amount_transacted'] == amount:
            correct_amount_transacted = True
        else:
            correct_amount_transacted = False
        
        if transaction_data['from']['id'] == slack_id:
            correct_slack_id = True
        else:
            correct_slack_id = False
        
        if transaction_data['for'] == transaction_id:
            correct_transaction_id = True
        else:
            correct_transaction_id = False
        
        if correct_amount_transacted and correct_slack_id and correct_transaction_id:
            return True
        elif loop_count == length:
            return False
        else:
            pass
            

def payout(slack_id, amount):
    #Mutation:
    data = """mutation send_hn_test($amount:Float!, $from: String!, $to: String!, $for : String!) {
  send(data:{balance:$amount, from: $from, to:$to, for:$for}){
    validated
  }
}"""
    #Variables for the mutation:
    variables = {
  "amount": amount,
  "from": "U01N29M0C9L",
  "to": slack_id,
  "for": "TEST"
}
    #Authentication
    headers = {
    "secret" : 'PUT_HN_TOKEN_HERE'
}
    #Sending the post request to the HN Api
    r = requests.post('https://hn.rishi.cx', json={"query":data, 'variables': variables}, headers=headers)


