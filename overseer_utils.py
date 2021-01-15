import requests
import json


url = 'https://github.com/KhushrajRathod/TheOverseerBackend/releases/download/Latest/results.json'
x = requests.get(url)

json_data = json.loads(x.content)

def find_user_message_count(y, json_data):
    z = 0
    for item in json_data:
        z += 1
        if item[0] == y: 
            break
    z -= 1
    return json_data[z][1]