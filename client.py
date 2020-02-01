'''
Created on Jan 17, 2020

@author: tiz
'''
from socket import *
import sys

serverName = 'localhost'


serverPort = 4000

clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect((serverName,serverPort))

fileToget = raw_input('Url to get :')

clientSocket.send(fileToget)

try:
    fileSizeFromServer = int(clientSocket.recv(4000))
except ValueError:
    print "Error, the Server was unable to get the file"
    sys.exit(1)
    

fileFromServer = clientSocket.recv(4000)


print 'From Server:', fileFromServer


#Check the size of the file downloaded
fileSize = int (os.path.getsize(fileFromServer))
print 'File size downloaded from server: ', fileSize

#Compare size of the file with info coming from the server
if fileSizeFromServer == fileSize:
    print 'File arrived ..sending BYE to server'
else: 
    print 'Files have not the same size: something wrong. Exiting'
    sys.exit(1)
        
clientSocket.send('BYE')

timeToDwFromServer = clientSocket.recv(4000)

print 'Time to download the file is: ', timeToDwFromServer, ' sec.'


clientSocket.close()
