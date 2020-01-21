'''
Created on Jan 21, 2020

@author: tiz
'''
import threading
from socket import *
from requests import *
import requests
import os
import sys
import time
from timeit import default_timer as timer
from test.test_sax import start
from curses import start_color
from matplotlib.backends._macosx import Timer

serverPort = 4000
serverSocket = socket(AF_INET,SOCK_STREAM)

# Thread that will handle client's requests
class ClientThread(threading.Thread):
    # Implementation...
    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.socket = socket
    def run(self):
        while keep_alive:
            # Thread can receive from client
            data = self.socket.recv(1024)
            # Processing...
            # And send back a reply
            self.socket.send(reply)

while True:
    # The server accepts an incoming connection
    connectionSocket, addr = serverSocket.accept()
    # And creates a new thread to handle the client's requests
    newthread = ClientThread(connectionSocket)
    # Starting the thread
    newthread.start()
