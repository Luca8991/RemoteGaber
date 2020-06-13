import socket 
import threading
import funcs

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
    global state
    print(f"[NEW CONNECTION] {addr} connected.")

    allData = []
    state = {
        "current":"home",
        "previous":"day"
    }

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            
            if msg[0] == "u":
                allData = funcs.handle_init_msg(msg)
                config = allData["config"]
                send_msg = str(config)
                print(send_msg)
            elif msg == DISCONNECT_MESSAGE:
                connected = False
                send_msg = "Goodbye"
            else:
                send_msg, state = funcs.handle_msg(msg, state, allData)

            print(f"[{addr}] {msg}")
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