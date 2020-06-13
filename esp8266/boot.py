# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import uos, machine, sh1106
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
#import webrepl
#webrepl.start()
gc.collect()

import network

i2c = machine.I2C(scl=machine.Pin(4), sda=machine.Pin(5))
oled = sh1106.SH1106_I2C(128, 64, i2c, None, 0x3c)

SSID = "<your-ssid>"
PWD = "<your-pwd>"

oled.fill(0)
oled.text("connecting to wifi network:", 0, 0)
oled.text(SSID, 0, 10)
oled.rotate(True)
oled.show()

def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(SSID, PWD)
        while not sta_if.isconnected():
            pass
    oled.fill(0)
    oled.text("connected!", 0, 0)
    oled.text("IP:"+str(sta_if.ifconfig()[0]), 0 ,10)
    oled.rotate(True)
    oled.show()
    print('network config:', sta_if.ifconfig())
    
do_connect()