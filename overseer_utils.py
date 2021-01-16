import requests
import json

#Gets data from the Overseer Github
url = 'https://github.com/KhushrajRathod/TheOverseerBackend/releases/download/Latest/results.json'
x = requests.get(url)

#Formates the data into a list containing lists
json_data = json.loads(x.content)


#Function for getting the message count of a user
def find_user_message_count(user_id, json_data):
    ind = 0
    for item in json_data:
        ind += 1
        if item[0] == user_id: 
            break
    ind -= 1
    return json_data[ind][1]


# This function may be unneccesary and may be replaced by a db table
#def update_message_count(dictionary):
#    for item in dictionary:
#       new_message_count = find_user_message_count(item, json_data)
#       dictionary[item] = new_message_count
#    return dictionary