#!/bin/python

'''
    SERVER.PY : SERVER PROGRAM FOR THE Convopy

    What it does?:
    It instantiate a server for client to chat on. It also displays the chat message after
    sending it.
'''

import socket, _thread, sys

# Take in HOST and PORT as command line arguments
try:
    HOST = str(sys.argv[1])
    PORT = int(sys.argv[2])
except:
    print("Usage: ./client.py <hostname> <port>")
    sys.exit(0)

# HEADERSIZE which will decribe our message content before sending so we can process it properly
HEADERSIZE = 10

# List which will contain all the connected clients
CLIENTS = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(1)

# Removes connected clients
def remove(conn):
    if conn in CLIENTS:
        CLIENTS.remove(conn)

# When a client sends a message, we will broadcast it to all the users so that they can see the message
def broadcast(msg, conn):
    for client in CLIENTS:
        if client != conn:
            try:
                client.send(msg)
            except:
                client.close()
                remove(client)

# When clients connects we create a new thread and pass this function which will constantly
# receive data from the client and broadcast to other clients
def clientThread(conn, addr):
    serverMsg = "{:^80s}".format("Welcome to my CHATROOM V0.1!")
    serverMsg = (f'{len(serverMsg):<{HEADERSIZE}}' + serverMsg).encode('utf-8')
    conn.send(serverMsg)

    while True:
        try:
            newMsg = True
            fullMsg = ""
            while True:
                msg = conn.recv(20)
                if newMsg:
                    msgLength = int(msg.decode('utf-8')[:HEADERSIZE])
                    newMsg = False
                fullMsg += msg.decode('utf-8')

                if len(fullMsg)-HEADERSIZE == msgLength:
                    fullMsg = '<' + addr[0] + '>: ' + fullMsg[HEADERSIZE:]
                    broadcastMsg = (f'{len(fullMsg):<{HEADERSIZE}}' + fullMsg).encode('utf-8')
                    broadcast(broadcastMsg, conn)
                    print(fullMsg)
                    newMsg = True
                    fullMsg = ""
        except:
            continue

# main loop which will accept connections and create a new thread for each connections
while True:
    conn, addr = s.accept()
    CLIENTS.append(conn)
    print("Connected by %s" % str(addr))
    _thread.start_new_thread(clientThread, (conn, addr,))

conn.close()
s.close()