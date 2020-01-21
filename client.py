'''
Created on Jan 17, 2020

@author: tiz Client TCP
'''
from socket import *
import os.path
from os import path
import sys

serverName = 'localhost'

serverPort = 4000

clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect((serverName,serverPort))

# Connect - accept messages

message = 'connect'
clientSocket.send(message)

accept_from_server = clientSocket.recv(4000)
print 'From server: ' + accept_from_server

#Send the URL to the server

fileToget = raw_input('Url to get :')

clientSocket.send(fileToget)
    
#Here the client should receive the name of the file or, if there's any error in getting it
#from the server it should receive an error message. It then print a generic error message to
#the output. Of course if the resource also contain "error" in the name should be a problem but 
#a unique ID could be used, i.e. the mac address of the server

fileFromServer = clientSocket.recv(4000)
if 'Error' in fileFromServer:
        print "Error, the Server was unable to get the file"
        clientSocket.close()
        sys.exit(1)

print "Received File:",fileFromServer.strip()

################
## Main code ###
################

f = open(fileFromServer,'wb') # open file in write mode

fileFromServer = clientSocket.recv(1024)
try:
    while(fileFromServer):
        f.write(fileFromServer)
        clientSocket.settimeout(2)
        fileFromServer  = clientSocket.recv(1024)
except timeout:

    f.close()
  
print "File Downloaded"

#Send BYE message to server
        
clientSocket.send('BYE')

#Get the total time from server and display it 

timeToDwFromServer = clientSocket.recv(4000)

print 'Time to download the file is: ', timeToDwFromServer, ' sec.'

#Close connection

clientSocket.close()
