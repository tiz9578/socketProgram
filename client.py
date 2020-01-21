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
message = 'connect'
clientSocket.send(message)

accept_from_server = clientSocket.recv(4000)
print 'From server: ' + accept_from_server


fileToget = raw_input('Url to get :')

clientSocket.send(fileToget)

#try:
 #   fileSizeFromServer = int(clientSocket.recv(4000))
#except ValueError:
 #   print "Error, the Server was unable to get the file"
  #  sys.exit(1)
    

fileFromServer = clientSocket.recv(4000)
if 'Error' in fileFromServer:
        print "Error, the Server was unable to get the file"
        clientSocket.close()
        sys.exit(1)


#print 'From Server:', fileFromServer
print "Received File:",fileFromServer.strip()

#######
## Main code ###
#######
f = open(fileFromServer,'wb')

fileFromServer = clientSocket.recv(1024)
try:
    while(fileFromServer):
        f.write(fileFromServer)
        #print fileFromServer
        clientSocket.settimeout(2)
        fileFromServer  = clientSocket.recv(1024)
except timeout:
####xxx###dataFromServer = clientSocket.recv(1024)
####xxx###while(dataFromServer):
####xxx###    dataFromServer = clientSocket.recv(1024)
#while dataFromServer:
    #dataFromServer = clientSocket.recv(1024)
####xxx###   print dataFromServer
    #if not dataFromServer:
    #    break
#while (dataFromServer):
    #f.write(dataFromServer)

    f.close()
  
print "File Downloaded"



#Check the size of the file downloaded
#fileSize = int (os.path.getsize(fileFromServer))
#print 'File size downloaded from server: ', fileSize

#Compare size of the file with info coming from the server
#if fileSizeFromServer == fileSize:
#    print 'File arrived ..sending BYE to server'
#else: 
 #   print 'Files have not the same size: something wrong. Exiting'
  #  sys.exit(1)
        
clientSocket.send('BYE')

timeToDwFromServer = clientSocket.recv(4000)

print 'Time to download the file is: ', timeToDwFromServer, ' sec.'


clientSocket.close()
