import json
import datetime

def home():
    now = datetime.datetime.now()
    h = now.hour
    m = now.minute
    s = now.second

    time = "{:02d}".format(h)+":"+"{:02d}".format(m)+":"+"{:02d}".format(s)

    resp = [time, 30, 27]

    return "t"+str(resp)

def day():
    now = datetime.datetime.now()
    y = now.year
    M = now.month
    d = now.day

    time = "{:02d}".format(d)+" - "+"{:02d}".format(M)+" - "+str(y)

    resp = [time, 7, 27]

    return "t"+str(resp)

def app():
    resp = "ok"
    return resp

def up():
    return "UP"

def down():
    return "DOWN"