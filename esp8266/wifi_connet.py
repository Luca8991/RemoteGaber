import network
def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('<SSID>', '<PASSWORD>')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
    
do_connect()

