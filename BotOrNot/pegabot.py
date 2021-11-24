import json
import requests

def get(screen_name):
    req = requests.get('https://api.pegabot.com.br/botometer?socialnetwork=twitter&profile='+screen_name+'&search_for=profile&limit=1')
    return req.json()

def get_bot_probability(screen_name):
    req = requests.get('https://api.pegabot.com.br/botometer?socialnetwork=twitter&profile='+screen_name+'&search_for=profile&limit=1')
    data = req.json()
    return data['profiles'][0]['bot_probability']
    
#data = req.json()
#with open('output.json', 'w') as f:
    #json.dump(data, f)