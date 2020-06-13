import json
import datetime

allData = []

def handle_init_msg(msg):
    scope = msg[0]  #first char of msg
    msg = msg[1:].replace("'","\"")   #remove first char and correct quotes

    if scope == "u":    #received user data
        user_data = json.loads(msg)

        username = user_data["username"]

        with open(username+".json", "r") as rf:
            allData = json.load(rf)
            config = allData["config"]
            return config

def handle_msg(msg):
    '''msg = msg.replace("'","\"")   #correct quotes
    data = json.loads(msg)'''

    
    now = datetime.datetime.now()
    y = now.year
    M = now.month
    d = now.day
    h = now.hour
    m = now.minute
    s = now.second

    data = str(h)+":"+str(m)+":"+str(s)

    return data