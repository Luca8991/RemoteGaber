import socket 
import threading

from gaber import Gaber

HEADER = 64
PORT = 50500
#SERVER = socket.gethostbyname(socket.gethostname())
SERVER = "192.168.1.10"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    gaber = Gaber()

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            print(f"[{addr}] {msg}")

            if msg[0] == "u":
                gaber.setUser(msg)
                config = gaber.getUserConfig()
                send_msg = str(config)
                #print(send_msg)
            elif msg == DISCONNECT_MESSAGE:
                connected = False
                send_msg = "Goodbye"
            else:
                send_msg = gaber.respond(msg)

            
            conn.send(send_msg.encode(FORMAT))

    conn.close()
        

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()