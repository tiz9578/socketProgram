'''
Created on Jan 17, 2020

@author: tiz
'''

from socket import *
import os.path
from os import path
import sys

serverName = 'localhost'

serverPort = 4000

clientSocket = socket(AF_INET, SOCK_DGRAM)

#clientSocket.connect((serverName,serverPort))

fileToget = raw_input('Url to get :')

#clientSocket.send(fileToget)

clientSocket.sendto(fileToget,(serverName, serverPort))


try:
    #fileSizeFromServer = int(clientSocket.recv(4000))
    fileSizeFromServer, serverAddress = clientSocket.recvfrom(2048)
    if 'Error' in fileSizeFromServer:
        print "Error, the Server was unable to get the file"
        clientSocket.close()
        sys.exit(1)
        
   

except ValueError:
    print "Error, the Server was unable to get the file"
    sys.exit(1)
    

#fileFromServer = clientSocket.recv(4000)
fileFromServer, serverAddress = clientSocket.recvfrom(2048)


print 'From Server:', fileFromServer


#Check the size of the file downloaded
fileSize = int (os.path.getsize(fileFromServer))
print 'File size downloaded from server: ', fileSize

#Compare size of the file with info coming from the server

fileSizeFromServerInt = int(fileSizeFromServer)
if fileSizeFromServerInt == fileSize:
    print 'File arrived ..sending BYE to server'
else: 
    print 'Files have not the same size: something wrong. Exiting'
    sys.exit(1)
        
#clientSocket.send('BYE')
clientSocket.sendto('BYE',(serverName, serverPort))

#timeToDwFromServer = clientSocket.recv(4000)
timeToDwFromServer, serverAddress = clientSocket.recvfrom(2048)

print 'Time to download the file is: ', timeToDwFromServer, ' sec.'

clientSocket.close()
