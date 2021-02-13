import requests
import json


#Url for getting overseer data
url = 'https://github.com/KhushrajRathod/TheOverseerBackend/releases/download/Latest/results.json'
#actually getting the data
r = requests.get(url)

#loading the data that was requested as json
json_data = json.loads(r.content)

#Fucntion that finds the message count for a user in the json data
def find_user_message_count(slack_id, json_data):
    index = 0
    for item in json_data:
        index += 1
        if item[0] == slack_id: 
            break
    index -= 1
    return json_data[index][1]



