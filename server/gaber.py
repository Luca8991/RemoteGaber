import json
import sys
import importlib

class Gaber:
    def __init__(self):
        
        self.allData = []
        self.config = []
        self.framework = []
        self.actions = []

        self.screens = []

        self.scripts = None

        self.username = ""
        
        self.state = {
            "current": "home",
            "previous": "app"
        }

        self.memory = {}

    #-------------------#
    ####### USER ########
    #-------------------#
    
    def setUser(self, username_from_client):
        self.username = self.decodeUsername(username_from_client)
        
        with open("./"+self.username+"/config.json", "r") as rf:
            self.config = json.load(rf)
        
        with open("./"+self.username+"/framework.json", "r") as rf:
            tmp = json.load(rf)
            self.framework = tmp["framework"]
            self.actions = tmp["actions"]

        with open("./"+self.username+"/screens.json", "r") as rf:
            self.screens = json.load(rf)

        self.scripts = importlib.import_module(self.username+".scripts", self.username)

    def getUserConfig(self):
        return self.config

    def decodeUsername(self, msg):
        scope = msg[0]  #first char of msg
        msg = msg[1:].replace("'","\"")   #remove first char and correct quotes

        if scope == "u":    #received user data
            user_data = json.loads(msg)

            username = user_data["username"]

            return username

    #-------------------#
    ###### ACTIONS ######
    #-------------------#

    def respond(self, incoming_msg):
        incomingData = json.loads(incoming_msg)

        resp = ""

        index = 0
        for btnValue in incomingData:
            if btnValue == 0:
                btnNumber = self.config["in"][index]
                btn = self.framework[str(btnNumber)]

                toDo = self.handleButton(btn)

                resp = self.doAction(toDo)

                return resp
            index = index+1
        
        resp = self.doAction(self.state["current"])
        return resp

    def handleButton(self, btn):
        actions = btn["actions"]

        currentState = self.state["current"]

        for a in actions:
            #print(a)
            if "current" in a:
                if a["current"] == currentState:
                    return a["action"]
            else:
                return a["default"]
    
    def updateState(self, newState):
        self.state["previous"] = self.state["current"]
        self.state["current"] = newState
    
    def doAction(self, toDo):
        action = self.actions[toDo]
        actionMode = action["mode"]
        actionType = action["type"]
        actionDo = action["do"]

        if actionMode == "script":
            script = getattr(self.scripts, actionDo)
            resp = script(self.memory)
        elif actionMode == "screen":
            '''with open("./" + self.username + "/" + self.screens[toDo]["data"], "r") as r:
                resp = str(r)'''
            resp = self.screens[actionDo]["data"]

        if actionType == "change-state":
            self.updateState(toDo)

        return resp