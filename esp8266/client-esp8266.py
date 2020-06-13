import socket
import json
import utime, machine, sh1106
from time import sleep

i2c = machine.I2C(scl=machine.Pin(4), sda=machine.Pin(5))
oled = sh1106.SH1106_I2C(128, 64, i2c, None, 0x3c)

HEADER = 64
PORT = 50500
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

# getaddrinfo is returning something like:
# [(x, y, z, '', ('<IPADDRESS>', PORT))]
# we can access the ip address with index [0][-1][0]
#SERVER = socket.getaddrinfo("lucab.ddns.net",PORT)[0][-1][0]
SERVER = "192.168.1.10"
ADDR = (SERVER, PORT)

oled.fill(0)
oled.text("connecting to:", 0, 0)
oled.text(SERVER, 0, 10)
oled.rotate(True)
oled.show()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def receiveConfig(config):
    config = json.loads(config.replace("'","\""))   #correct quotes and load into object
    return config

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    #print(send_length)
    client.send(send_length)
    client.send(message)


with open("user.json", "r") as read_file:
    user_info = json.load(read_file)

user_name = user_info["username"]
oled.fill(0)
oled.text(user_name, 0, 0)
oled.rotate(True)
oled.show()

send("u"+str(user_info))    # send user info to server

config = receiveConfig(client.recv(2048).decode(FORMAT))

inPins = config["in"]
outPins = config["out"]

while True:
    reads = []
    for pin in inPins:
        val = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP).value()
        reads.append(val)
    send(str(reads))

    time = client.recv(2048).decode(FORMAT)
    oled.fill(0)
    oled.text(time, 0, 10)
    oled.rotate(True)
    oled.show()
    
    sleep(0.05)

send(DISCONNECT_MESSAGE)