import json
import datetime
import math

from PIL import Image #python3 -m pip install Pillow

def drawLine(cx, cy, r, angle):
    
    sx = cx
    sy = cy - r + 2

    if angle == 30:
        sx = cx
        sy = cy + r - 2

    if angle > 0:
        rad = (angle/30) * math.pi - math.pi/2
        m = math.tan( rad )
        if angle < 30:
            sx = int( r / math.sqrt(1+math.pow(m,2)) ) + cx
            sy = int(  m*(sx-cx) ) + cy
        elif angle > 30:
            sx = -int( r / math.sqrt(1+math.pow(m,2)) ) + cx
            sy = int(  m*(sx-cx) ) + cy

    return sx, sy

def time(memory, screenBf, pinState):
    now = datetime.datetime.now()
    h = now.hour
    m = now.minute
    s = now.second

    screenBf.fill(0)

    cx = int(screenBf.width/2)
    cy = int(screenBf.height/2)
    r = int(screenBf.height/2)

    screenBf.circle(cx, cy, r, True)
    screenBf.circle(cx, cy, r-1, True)

    sx, sy = drawLine(cx, cy, r-1, s)
    screenBf.line(cx, cy, sx, sy, True)

    mx, my = drawLine(cx, cy, r-6, m)
    screenBf.line(cx, cy, mx, my, True)

    hx, hy = drawLine(cx, cy, r-12, (h/24)*60)
    screenBf.line(cx, cy, hx, hy, True)

def day(memory, screenBf, pinState):
    now = datetime.datetime.now()

    time = now.strftime("%X")

    screenBf.fill(0)

    screenBf.text(time, 16, 18, True, size=2)

    date = now.strftime("%a, %b %d %Y")

    screenBf.text(date, 16, 45, True, size=1)

'''def scrollUp(memory, screenBf, pinState):
    screenBf.scroll(0, -3)

def scrollDown(memory, screenBf, pinState):
    screenBf.scroll(0, 3)'''

def up(memory, screenBf, pinState):
    screenBf.fill(0)
    screenBf.text("TORCH", 32, 24, True, size=2)

def down(memory, screenBf, pinState):
    screenBf.fill(0)
    screenBf.text("COUNTER", 24, 24, True, size=2)
    '''image = Image.open('./scatman.1.pbm').convert('1')
    screenBf.image(image)'''

def showCount(count, screenBf):
    screenBf.fill(0)
    screenBf.text("Count:", 46, 16, True, size=1)

    x = 0
    y = 32
    if count >= 0 and count < 10:
        x = 59
    elif count < 0 and count > -10:
        x = 54
    elif count >= 10 :
        x = 54
    elif count < -10:
        x = 49
    
    screenBf.text(str(count), x, y, True, size=2)

def openCounter(memory, screenBf, pinState):
    if "counter" not in memory:
        memory["counter"] = {
            "count": 0
        }
    
    counterMem = memory["counter"]

    count = counterMem["count"]

    showCount(count, screenBf)

def counterUp(memory, screenBf, pinState):
    
    counterMem = memory["counter"]

    counterMem["count"] = counterMem["count"] + 1

    memory["counter"] = counterMem

    showCount(counterMem["count"], screenBf)

def counterDown(memory, screenBf, pinState):

    counterMem = memory["counter"]

    counterMem["count"] = counterMem["count"] - 1

    memory["counter"] = counterMem

    showCount(counterMem["count"], screenBf)

def showTorch(torchState, screenBf):
    text = "OFF"
    x = 48
    if torchState == 1:
        text = "ON"
        x = 52

    screenBf.fill(0)
    screenBf.text("Torch is:", 36, 16, True, size=1)
    screenBf.text(text, x, 32, True, size=2)

def torchOn(memory, screenBf, pinState):

    memory["torch"]["state"] = 1

    pinState[0] = 1

    showTorch(1, screenBf)

def torchOff(memory, screenBf, pinState):

    memory["torch"]["state"] = 0

    pinState[0] = 0

    showTorch(0, screenBf)

def openTorch(memory, screenBf, pinState):
    if "torch" not in memory:
        memory["torch"] = {
            "state": 0
        }
    
    torchState = memory["torch"]["state"]

    showTorch(torchState, screenBf)