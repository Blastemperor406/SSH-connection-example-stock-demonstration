import socket
import threading
import ssl
import yfinance as yf

ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain(certfile='server.crt', keyfile='server.key')

HEADER = 2048 # the first message is going to be a header of 64 bytes that gives info about the actual message.
PORT = 5050
FORMAT = "utf-8"
DISSCONNECT_MESSAGE = "!DISCONNECT"

"""SERVER="192.168.0.104"""  # hardcoding

SERVER = socket.gethostbyname(socket.gethostname())


"""print(socket.gethostname()) 
print(SERVER)"""  # testing

ADDR = (SERVER, PORT)

# picking the socket ,socket streaming data over ipv4
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# Defining a list to store the connected clients
clients = []

#The client handler 
def handle_client(conn, addr):
    print(f"New connection made: {addr}")
    conn_ssl = ssl_context.wrap_socket(conn, server_side=True)
    connection = True
    while connection == True: 
        msg_length = conn_ssl.recv(HEADER).decode(FORMAT)  # blocking lines of code; doesnt execute until done
        if msg_length:
            msg_length = int(msg_length)
            msg = conn_ssl.recv(msg_length).decode(FORMAT)
            if msg == DISSCONNECT_MESSAGE:
                connection = False
                print(f"{addr} {msg}")
                conn_ssl.send(("Msg recieved "+msg).encode(FORMAT))
            else:
                data=msg.split()
                ticker = yf.Ticker(data[0])
                data1 = ticker.history(period=data[1])
                data1= data1.to_dict(orient="records")
                data1=str(data1)
                data1=data1[1:len(data1)-1]
                print(f"{addr} {msg}")
                conn_ssl.send(("Msg recieved "+msg).encode(FORMAT))
                conn_ssl.send((data1).encode(FORMAT))


#initialization
def start():
    server.listen()
    print(f"Listening Server on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"Active connections {threading.active_count()-1}")


print("Server is starting")

start()
