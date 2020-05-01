import socket
import time

### state of leds:
# False = OFF
# True = ON
prec4 = False       # prec state of led 4
prec5 = False       # prec state of led 5
prec4_mem = False   # prec memory of led 4
prec5_mem = False   # prec memory of led 5
###

### pins declaration
btn_arr = [12, 14]  # array of possible buttons
led4 = 4
led5 = 5
led_onboard = 2
###

### state of onboard led (pin 2):
# False = ON
# True = OFF
prec2 = True
###

### "operative system" state
state = "home"
###

### variables to handle double button click
start = time.time() # now
DELTA_BTN = 1 # = 1s // time between two btn clicks
###

### UDP variables ###
LOCAL_IP = '0.0.0.0'   # IP of local server
ESP_IP = '192.168.1.14'     # IP of ESP
PORT = 65432                # Port to listen on (non-privileged ports are > 1023)
BUFFER_SIZE = 1024          # Normally 1024
### ###

#### send package cointaining all pins and ####
def send(pkg_arr):
    msg = ''
    for pkg in pkg_arr:
        msg = msg+str(pkg)+":"
    msg = msg[:-1]  # remove last semicolon
    
    pkg_to_bit = bytes(msg, 'utf-8')    # translate to bits
    print("sending in byte:",pkg_to_bit,"sending:",msg)
    s.sendto(pkg_to_bit, (ESP_IP,PORT))  # send UDP message
    
#### ####
    
    
#### MAIN "OPERATIVE SYSTEM" FUNCTION ####
def gaber(btn):
    global prec4, prec5, prec2, led, bit, state, start, prec4_mem, prec5_mem    # view these variables as global
    
    pkg_arr = [] # array to be sent, containing each led new state
    
    ##### BUTTON 12 PRESSED #####
    if btn == 12:
    
        if state == "home":         # home -> led 4 switch state
            print("home, btn 12")
            led = 4
            prec4 = not prec4
            bit = int(prec4)
            pk = led*10 + bit     # number of two digits: the first is 0 or 1 (value to be written) the second is the number of the pin to witch write value
            
            pkg_arr.append(pk)
            # other led states unchanged
            pkg_arr.append(50+int(prec5))
            pkg_arr.append(20+int(prec2))
            
        elif state == "app":        # app -> switch both leds
            print("app, btn 12")
            prec4 = not prec4       # switch 
            prec5 = not prec5
            pk1 = 40 + int(prec4)
            pk2 = 50 + int(prec5)
            
            pkg_arr.append(pk1)
            pkg_arr.append(pk2)
            # other led states unchanged
            pkg_arr.append(20+int(prec2))
    ##### END BUTTON 12 #####
    
    ##### BUTTON 14 PRESSED #####
    elif btn == 14:
        elapsed = time.time() - start # time elapsed between this click and the previous one
        print(elapsed)
        
        ### double click -> switch between home and app ###
        if elapsed < DELTA_BTN:     
        
            if state == "home":     ## enter the app, switch leds off
                print("home, btn 14, double click")
                state = "app"
                prec4_mem = prec4
                prec5_mem = prec5
                prec4 = False
                prec5 = False
                pk1 = 40 + int(prec4) # switch off led 4
                pk2 = 50 + int(prec5)# switch off led 5
                
                pkg_arr.append(pk1)
                pkg_arr.append(pk2)
                # other led states unchanged
                pkg_arr.append(20+int(prec2))
                
            elif state == "app":    ## exit the app, return to previous state
                print("app, btn 14, double click")
                state = "home"
                prec4 = prec4_mem   # load from memory previous led 4 state
                prec5 = prec5_mem   # load from memory previous led 5 state
                prec2 = True        # switch off led 2
                pk1 = 40 + int(prec4) # back to previous state on led 4
                pk2 = 50 + int(prec5) # back to previous state on led 5
                
                pkg_arr.append(pk1)
                pkg_arr.append(pk2)
                # other led states unchanged
                pkg_arr.append(20+int(prec2))
                
        ### end double click ###
        
        ### single click -> routines for home and app ###
        else:                                   
            
            if state == "home":     ## home -> led 5 switch state
                print("home, btn 14")
                led = led5
                prec5 = not prec5
                bit = int(prec5)
                pk = led*10 + bit     # number of two digits: the first is 0 or 1 (value to be written) the second is the number of the pin to witch write value
                
                pkg_arr.append(pk)
                # other led states unchanged
                pkg_arr.append(40+int(prec4))
                pkg_arr.append(20+int(prec2))
            elif state == "app":    ## app -> onboard led (pin 2) switch state
                print("app, btn 14")
                led = led_onboard
                prec2 = not prec2
                bit = int(prec2)
                pk = led*10 + bit     # number of two digits: the first is 0 or 1 (value to be written) the second is the number of the pin to witch write value
                
                pkg_arr.append(pk)
                # other led states unchanged
                pkg_arr.append(40+int(prec4))
                pkg_arr.append(50+int(prec5))
        ### end single click ###
        
        start = time.time() # set start to now, waiting for another double click
    ##### END BUTTON 14 #####
    send(pkg_arr) # send array!
    return 0
    
#### ####
    
## init socket ##
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    #UDP socket
s.bind((LOCAL_IP,PORT))
## ##

#### loop until data is empty ####
while True:
    data, addr = s.recvfrom(BUFFER_SIZE)
    if not data: break  # exit if data is empty
    print ("received data:", data)
    
    btn = int.from_bytes(data,'big')    # get number of button pressed
    
    if btn in btn_arr:  # if received button is on possible buttons
        gaber(btn) # MAIN
    
#### end loop ####

s.close()   # close socket


