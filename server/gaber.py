import json
import sys
import importlib
import adafruit_framebuf

class Gaber:
    def __init__(self):

        self.config = []
        self.init = []
        self.framework = []
        self.actions = []

        self.screens = []

        self.scripts = None

        self.username = ""
        
        self.state = {
            "current": "home",
            "previous": "home"
        }

        self.pinState = []

        self.screenWidth = 0
        self.screenHeight = 0
        self.screenBuffer = None

        self.memory = {}

    #-------------------#
    ####### USER ########
    #-------------------#
    
    def setUser(self, username_from_client):
        user = username_from_client.replace("'","\"")
        user_data = json.loads(user)
        self.username = user_data["username"]
        
        with open("./"+self.username+"/config.json", "r") as rf:
            tmp = json.load(rf)
            self.config = tmp["pins"]
            self.initials = tmp["init"]

            for _ in self.config["out"]:   # set all output pins off
                self.pinState.append(0)
        
        with open("./"+self.username+"/framework.json", "r") as rf:
            tmp = json.load(rf)
            self.framework = tmp["framework"]
            self.actions = tmp["actions"]

        with open("./"+self.username+"/screens.json", "r") as rf:
            self.screens = json.load(rf)

        self.scripts = importlib.import_module(self.username+".scripts", self.username)

        self.setScreen()

    def setScreen(self):
        initScreen = self.initials["screen"]
        self.screenWidth = self.initials["width"]
        self.screenHeight = self.initials["height"]

        initScreen = bytearray(round(self.screenWidth * self.screenHeight / 8))
        self.screenBuffer = adafruit_framebuf.FrameBuffer(
            initScreen, self.screenWidth, self.screenHeight, buf_format=adafruit_framebuf.MVLSB
        )

    def getUserConfig(self):
        return self.config

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
    
    def updateState(self, newState, saveState):
        if self.state["current"] is not newState:
            if saveState:
                self.state["previous"] = self.state["current"]
            
            self.state["current"] = newState
    
    def doAction(self, toDo):
        #print("todo: ", toDo, "previous: ", self.state["previous"])
        if toDo == "BACK":
            toDo = self.state["previous"]
        
        action = self.actions[toDo]
        actionMode = action["mode"]
        actionType = action["type"]
        actionDo = action["do"]

        if actionMode == "script":
            script = getattr(self.scripts, actionDo)
            script(self.memory, self.screenBuffer, self.pinState)
        '''elif actionMode == "screen":
            resp = self.screens[actionDo]'''

        if actionType == "save-state":
            self.updateState(toDo, True)
        elif actionType == "change-state":
            self.updateState(toDo, False)

        byteResp = self.prepareResp()

        return byteResp

    def prepareResp(self):
        fb = self.screenBuffer.buf
        pins = bytearray(self.pinState)

        byteResp = pins + fb

        return byteResp
