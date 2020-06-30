import socket
import json
import struct

from time import sleep
from framebuf import FrameBuffer, MONO_VLSB
from machine import I2C, Pin
from sh1106 import SH1106_I2C

i2c = I2C(scl=Pin(4), sda=Pin(5))
oled = SH1106_I2C(128, 64, i2c, None, 0x3c)

HEADER = 64
PORT = 50500
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "0.0.0.0"

with open("params.json", "r") as r:
    params = json.load(r)

    HEADER = params["config"]["headerSize"]

    if "ipAddress" in params["config"]:
        SERVER = params["config"]["ipAddress"]
    elif "address":
        # getaddrinfo returns:
        # [(x, y, z, '', ('<IPADDRESS>', PORT))]
        # we can get the ip address with this index: [0][-1][0]
        SERVER = socket.getaddrinfo(params["config"]["address"],PORT)[0][-1][0]
    
    PORT = params["config"]["port"]
    FORMAT = params["config"]["encodingFormat"]
    DISCONNECT_MESSAGE = params["config"]["byeMessage"]

ADDR = (SERVER, PORT)

oled.fill(0)
oled.text("connecting to:", 0, 0)
oled.text(SERVER, 0, 10)
oled.rotate(True)
oled.show()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def receiveJSON(data):
    return json.loads(data.replace("'","\""))   #correct quotes and load into object

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    #print(send_length)
    client.send(send_length)
    client.send(message)

def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        try:
            sock.settimeout(0.01)
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        except:
            pass
    return data

with open("user.json", "r") as read_file:
    user_info = json.load(read_file)

user_name = user_info["username"]
oled.fill(0)
oled.text(user_name, 0, 0)
oled.rotate(True)
oled.show()

send(str(user_info))    # send user info to server

config = receiveJSON(recv_msg(client).decode(FORMAT))

inPins = config["in"]
outPins = config["out"]

while True:
    reads = []
    for pin in inPins:
        val = Pin(pin, Pin.IN, Pin.PULL_UP).value()
        reads.append(val)
    send(str(reads))
    
    resp = recv_msg(client)
    
    for i in (0, len(outPins)-1):
        pinNumber = outPins[i]
        pinValue = resp[i]
        Pin(pinNumber, Pin.OUT).value(not pinValue)

    screen = resp[i+1:]
    
    fbuf = FrameBuffer(screen, 128, 64, MONO_VLSB)
    oled.blit(fbuf, 0, 0)
    
    oled.rotate(True)
    oled.show()
    sleep(0.05)

send(DISCONNECT_MESSAGE)