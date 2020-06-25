import json
import datetime

def time(memory):
    now = datetime.datetime.now()
    h = now.hour
    m = now.minute
    s = now.second

    time = "{:02d}".format(h)+":"+"{:02d}".format(m)+":"+"{:02d}".format(s)

    resp = [time, 32, 28]

    return "t"+str(resp)

def day(memory):
    now = datetime.datetime.now()
    y = now.year
    M = now.month
    d = now.day

    time = "{:02d}".format(d)+"/"+"{:02d}".format(M)+"/"+str(y)

    resp = [time, 24, 28]

    return "t"+str(resp)

def openCounter(memory):
    if "counter" not in memory:
        memory["counter"] = {
            "count": 0
        }
    
    counterMem = memory["counter"]

    resp = [str(counterMem["count"]), 60, 28]

    return "t"+str(resp)

def counterUp(memory):
    
    counterMem = memory["counter"]

    counterMem["count"] = counterMem["count"] + 1

    memory["counter"] = counterMem

    resp = [str(counterMem["count"]), 60, 28]

    return "t"+str(resp)

def counterDown(memory):

    counterMem = memory["counter"]

    counterMem["count"] = counterMem["count"] - 1

    memory["counter"] = counterMem

    resp = [str(counterMem["count"]), 60, 28]

    return "t"+str(resp)

def torchOn(memory):

    memory["torch"]["state"] = 1

    resp = [1]
    return "p"+str(resp)

def torchOff(memory):

    memory["torch"]["state"] = 0

    resp = [0]
    return "p"+str(resp)

def openTorch(memory):
    if "torch" not in memory:
        memory["torch"] = {
            "state": 0
        }
    
    torchState = memory["torch"]["state"]

    text = "OFF"
    if torchState == 1:
        text = "ON"
    
    resp = ["Torch is "+text, 10, 27]

    return "t"+str(resp)