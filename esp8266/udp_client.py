import socket
from machine import Pin
from time import sleep

HOST = '192.168.1.10'  # The server's hostname or IP address
LOCAL_IP = '0.0.0.0' # IP of the ESP
PORT = 65432           # The port used by the server
BUFFER_SIZE = 1024
INIT_MESSAGE = b'\x0c'

## led and buttons initialization ##
led5 = Pin(5, Pin.OUT, value=0)
led4 = Pin(4, Pin.OUT, value=0)
led_board = Pin(2, Pin.OUT, value=1)

btn14 = Pin(14, Pin.IN, Pin.PULL_UP)
btn12 = Pin(12, Pin.IN, Pin.PULL_UP)
## end of initialization ##

### send number of button pressed ###
def send(m):
        msg = m.to_bytes(1,'big')
        print("sending:", msg, "pin read:", m)
        s.sendto(msg, (HOST,PORT))
### ###

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # init UDP socket
s.bind((LOCAL_IP, PORT))

btn14_state = 0
btn12_state = 0

while True:
        
        data = ''
        if btn14.value() != btn14_state: # if button 14 is pressed
            print("btn14:",btn14.value())
            send(14)
            data, addr = s.recvfrom(BUFFER_SIZE)
        if btn12.value() != btn12_state: # if button 12 is pressed
            print("btn12:",btn12.value())
            send(12)
            data, addr = s.recvfrom(BUFFER_SIZE)
            
        if data != '':
            print("received:",data)
            
            resp = str(data.decode('utf-8'))  # data is formatted XXx:XXx:XXx: ...
            resp = resp.split(':')
            
            for number in resp:
                #print(b)
                b = int(number)
                pin_number = int(b/10)
                pin_value = b%10
                
                print(pin_number, pin_value)
                
                if pin_number == 4:
                    led4.value(pin_value)
                elif pin_number == 5:
                    led5.value(pin_value)
                elif pin_number == 2:
                    led_board.value(pin_value)
                    
        sleep(0.2) # = 100ms // sleep to avoid undesired multiple button pressing

print('Received', repr(data))

