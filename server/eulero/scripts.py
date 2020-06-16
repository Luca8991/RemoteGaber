import json
import datetime

def home(memory):
    now = datetime.datetime.now()
    h = now.hour
    m = now.minute
    s = now.second

    time = "{:02d}".format(h)+":"+"{:02d}".format(m)+":"+"{:02d}".format(s)

    resp = [time, 30, 27]

    return "t"+str(resp)

def day(memory):
    now = datetime.datetime.now()
    y = now.year
    M = now.month
    d = now.day

    time = "{:02d}".format(d)+" - "+"{:02d}".format(M)+" - "+str(y)

    resp = [time, 7, 27]

    return "t"+str(resp)

def counter(memory):
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