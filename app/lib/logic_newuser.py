import requests
import json

def userSend(userJSON):
    server_ip = 'http://127.0.0.1:5002/newUser'
    headers = {'Content-Type': 'application/json'}
    server_return = requests.post(server_ip,headers=headers,data=json.dumps(userJSON))
    return
