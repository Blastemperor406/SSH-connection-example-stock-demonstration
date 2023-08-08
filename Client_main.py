import socket
import ssl
import tkinter as tk
import json
import matplotlib.pyplot as plt
HEADER= 2048 # the first message is going to be a header of 64 bytes that gives info about the actual message.
PORT= 5050
FORMAT="utf-8" 
DISSCONNECT_MESSAGE= "!DISCONNECT"


SERVER="10.20.203.147"  #hardcoding
ADDR=(SERVER,PORT)



client =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)




ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
ssl_context.load_verify_locations('server.crt')
conn_ssl = ssl_context.wrap_socket(client, server_hostname='Darsh')
v=0
v1=0

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn_ssl.send(send_length)
    conn_ssl.send(message)
    print(conn_ssl.recv(2048).decode(FORMAT))
    print(conn_ssl.recv(2048).decode(FORMAT))
    return



def disconnect():
    send(DISSCONNECT_MESSAGE)
k='1'
while k!='0':
    a=input("Choose a stock:")
    b=input("choose a duration 1d, 5d, 1mo:")
    c=a+ " "+b
    print(c,type(c))
    send(c)
    k=(input("\n do you want to CONTINUE press enter, else press 0"))
    if k=="0":
        disconnect()
    
