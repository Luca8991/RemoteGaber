import socket
import json
import struct

import utime, machine, sh1106
from time import sleep
import framebuf

i2c = machine.I2C(scl=machine.Pin(4), sda=machine.Pin(5))
oled = sh1106.SH1106_I2C(128, 64, i2c, None, 0x3c)

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

def receiveJSON(config):
    j = json.loads(config.replace("'","\""))   #correct quotes and load into object
    return j

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
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

with open("user.json", "r") as read_file:
    user_info = json.load(read_file)

user_name = user_info["username"]
oled.fill(0)
oled.text(user_name, 0, 0)
oled.rotate(True)
oled.show()

send("u"+str(user_info))    # send user info to server

config = receiveJSON(recv_msg(client).decode(FORMAT))

inPins = config["in"]
outPins = config["out"]

while True:
    reads = []
    for pin in inPins:
        val = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP).value()
        reads.append(val)
    send(str(reads))

    r = recv_msg(client)
    #print(resp, resp[1:])

    firstChar = chr(r[0])
    
    if firstChar == "t":
        resp = r.decode(FORMAT)
        resp = receiveJSON(resp[1:])
        oled.fill(0)
        oled.text(resp[0], resp[1], resp[2])
    elif firstChar == "p":
        resp = r.decode(FORMAT)
        resp = receiveJSON(resp[1:])
        for i in (0, len(resp)-1):
            pinNumber = outPins[i]
            pinValue = resp[i]
            machine.Pin(pinNumber, machine.Pin.OUT).value(not pinValue)
    else:
        #print(r)
        data = bytearray(r)
        #print(len(data))
        fbuf = framebuf.FrameBuffer(data, 128, 64, framebuf.MONO_HLSB)
        #oled.invert(1)
        oled.fill(0)
        oled.blit(fbuf,0,0)
    
    oled.rotate(True)
    oled.show()
    sleep(0.01)

send(DISCONNECT_MESSAGE)