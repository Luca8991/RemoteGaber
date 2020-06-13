import json
import datetime

def handle_init_msg(msg):
    scope = msg[0]  #first char of msg
    msg = msg[1:].replace("'","\"")   #remove first char and correct quotes

    if scope == "u":    #received user data
        user_data = json.loads(msg)

        username = user_data["username"]

        with open(username+".json", "r") as rf:
            allData = json.load(rf)
            return allData

def work(btnType, currentState, previousState):
    toDo = ""
    if btnType == "toggle":
        newCurrentState = previousState
        newPreviousState = currentState
        toDo = newCurrentState
    return toDo, newCurrentState, newPreviousState


def handle_msg(msg, state, allData):
    #msg = msg.replace("'","\"")   #correct quotes
    data = json.loads(msg)
    workData = allData["work"]
    configData = allData["config"]

    currentState = state["current"]
    previousState = state["previous"]
    
    now = datetime.datetime.now()
    y = now.year
    M = now.month
    d = now.day
    h = now.hour
    m = now.minute
    s = now.second

    toDo = currentState
    if data[2] == 0:
        btnType = workData[str(configData["in"][2])]["type"]
        toDo, state["current"], state["previous"] = work(btnType, currentState, previousState)
    
    resp = "empty"
    if toDo == "home":
        resp = str(h)+":"+str(m)+":"+str(s)
    elif toDo == "day":
        resp = str(d)+"-"+str(M)+"-"+str(y)

    return resp, state