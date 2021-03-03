#!/bin/python

'''
    CLIENT.PY : CLIENT PROGRAM FOR THE Convopy

    What it does?:
    It connects to the server instantiated using server.py. And we can chat with the people
    connected to the same server using this client program.
'''

import socket, sys, select, _thread

# Take in HOST and PORT as command line arguments
try:
    HOST = str(sys.argv[1])
    PORT = int(sys.argv[2])
except:
    print("Usage: ./client.py <hostname> <port>")
    sys.exit(0)

# HEADERSIZE which will decribe our message content before sending so we can process it properly
HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

# When client connects successfully to the server we create a thread and pass this function
# which will constantly receive message from the server and client (basically it will also be sent
# from the server)
def receiveMsg(s):
    while True:
        try:
            newMsg = True
            fullMsg = ""
            while True:
                msg = s.recv(20)
                if newMsg:
                    msgLength = int(msg.decode('utf-8')[:HEADERSIZE])
                    newMsg = False
                fullMsg += msg.decode('utf-8')

                if len(fullMsg)-HEADERSIZE == msgLength:
                    fullMsg = fullMsg[HEADERSIZE:]
                    print(fullMsg)
                    newMsg = True
                    fullMsg = ""
        except:
            continue

_thread.start_new_thread(receiveMsg, (s,))

# main loop which will take the input from user and send it to server and other clients
while True:
    msg = str(sys.stdin.readline().rstrip()) + "\n"
    s.send((f'{len(msg):<{HEADERSIZE}}' + msg).encode('utf-8'))
    sys.stdout.write("<You>: " + msg + "\n")
    sys.stdout.flush()

s.close()