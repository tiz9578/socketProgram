'''
Created on Jan 17, 2020

@author: tiz
'''
from socket import *
from requests import *
import requests
import sys
import time
from timeit import default_timer as timer
from test.test_sax import start

serverPort = 4000
serverSocket = socket(AF_INET,SOCK_STREAM)

serverSocket.bind(('',serverPort))

serverSocket.listen(1)

print 'The server is ready to receive'
while 1:
    connectionSocket, addr = serverSocket.accept()
    fileurl = connectionSocket.recv(4000)
    #Try to get the total time for the process
    start = timer()

    try:
        r = requests.get(fileurl, allow_redirects=True)
        r.raise_for_status() 
    except requests.exceptions.HTTPError as err:
        print err
        connectionSocket.send('Http error')
        sys.exit(1)
    except requests.exceptions.ConnectionError as errcon:
        print ("Error Connecting:",errcon)
        connectionSocket.send('Connection error')
        sys.exit(1)
    except requests.exceptions.Timeout as errTime:
        print ("Timeout Error:",errTime)
        connectionSocket.send('Timeout error')
        sys.exit(1)
    
    
    # Check the file size
    fileSize = r.headers['Content-length']
    
    print 'Client request new file. Size of the file: ', fileSize
        
   
    # Find the name of the file based on URL
    if fileurl.find('/'):
        print 'Getting ' + fileurl.rsplit('/', 1)[1]
        fileToClient = fileurl.rsplit('/', 1)[1]
    
    
    # Create an empty file to store the content of the file
    open(fileToClient, 'wb').write(r.content)
    
    
    #First: send the size of the file from the header to the client to compare

    connectionSocket.send(fileSize)
    
    
    #Second send the file to client
    
    connectionSocket.send(fileToClient)
    
    
    
    # Then wait for the BYE message from the client in order to close
    
    byeMessage = connectionSocket.recv(4000)
    print 'From client: ' , byeMessage
    if byeMessage == 'BYE':
        print 'BYE message arrived, closing connection'
        
        # Now stop the timer, compute the elapsed time and send it to the client
        end = timer()
        totTime = (end - start)
        print 'Total time: ', totTime, 'sec.'
        print
        connectionSocket.send(str(totTime))
        
        #Then close the connection
        connectionSocket.close()
