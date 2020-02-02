'''
Created on Jan 17, 2020

@author: tiz
'''

from socket import *
import sys
import os

serverName = 'localhost'

serverPort = 4000

clientSocket = socket(AF_INET, SOCK_DGRAM)

# Connect - accept messages

message = 'connect'
clientSocket.sendto(message,(serverName, serverPort))

accept_from_server, serverAddress = clientSocket.recvfrom(1024)
print 'From server: ' + accept_from_server

#Send the URL to the server

fileToget = raw_input('Url to get :')

clientSocket.sendto(fileToget,(serverName, serverPort))


#Here the client should receive the name of the file or, if there's any error in getting it
#from the server it should receive an error message. It then print a generic error message to
#the output. Of course if the resource also contain "error" in the name should be a problem but 
#a unique ID could be used, i.e. the mac address of the server

fileFromServer, serverAddress = clientSocket.recvfrom(1024)
if 'Error' in fileFromServer:
        print "Error, the Server was unable to get the file"
        clientSocket.close()
        sys.exit(1)
        
print "Received File:",fileFromServer.strip()
nameFile = fileFromServer.strip()
print nameFile

################
## Main code ###
################

f = open(fileFromServer.strip(),'wb') # open file in write mode

fileFromServer, serverAddress = clientSocket.recvfrom(1024)
try:
    while(fileFromServer):
        f.write(fileFromServer)
        clientSocket.settimeout(2)
        fileFromServer,addr = clientSocket.recvfrom(1024)
except timeout:
    f.close()
  
    print "File Downloaded"

# Test get the file size on dik:

bSize=os.statvfs(nameFile).f_bsize
print 'Actual size of the file: ', bSize

clientSocket.sendto('OK file downloaded',(serverName, serverPort))

filesizeOnDiskFromServer, serverAddress = clientSocket.recvfrom(1024)
print 'The server claims that the size of the file on the disk is ', filesizeOnDiskFromServer

if int(filesizeOnDiskFromServer) == bSize:
    print 'File arrived ..sending BYE to server'
else: 
    print 'Not equals...'

#Send BYE message to server

clientSocket.sendto('BYE',(serverName, serverPort))

#Get the total time from server and display it 

timeToDwFromServer, serverAddress = clientSocket.recvfrom(2048)

print 'Time to download the file is: ', timeToDwFromServer, ' sec.'

#Close connection

clientSocket.close()
