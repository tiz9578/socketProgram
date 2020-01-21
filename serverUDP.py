'''
Created on Jan 17, 2020

@author: tiz - UDP Server
'''
from socket import *
from requests import *
import requests
import os
import sys
from timeit import default_timer as timer
import time

serverPort = 4000
serverSocket = socket(AF_INET,SOCK_DGRAM)

serverSocket.bind(('',serverPort))

#server in listening mode
print 'The server is ready to receive'
while 1:

    # Connect - accept messages

    connect_from_client, clientAddress = serverSocket.recvfrom(2048)
    print 'From client: '+ connect_from_client

    accept_connection = 'accept'
    serverSocket.sendto(accept_connection, clientAddress)

    # Get the URL from the client

    fileurl, clientAddress = serverSocket.recvfrom(2048)
   
    #Try to get the total time for the process. Start:
    start = timer()
    
    # Get the file from the URL sent by the client. 
    # In order to deal with exceptions we implement a try-except block
    # we use exceptions from the "requests" module. 
    # On the server we have the specific error - HTTP, Connection, Timeout
    # or a generic error. A message is sent to the client.
    
    try:
        r = requests.get(fileurl, allow_redirects=True)
        r.raise_for_status() 
    except requests.exceptions.HTTPError as err:
        print err
        serverSocket.sendto('Http Error', clientAddress)
        sys.exit(1)
    except requests.exceptions.ConnectionError as errcon:
        print ("Error Connecting:",errcon)
        serverSocket.sendto('Connection Error', clientAddress)
        sys.exit(1)
    except requests.exceptions.Timeout as errTime:
        print ("Timeout Error:",errTime)
        serverSocket.sendto('Timeout Error', clientAddress)
        sys.exit(1)
    except:
        print ("Generic Error")
        serverSocket.sendto('Generic Error', clientAddress)
        sys.exit(1)
    
    
    # Optional: check the file size from the headers
    
    fileSize = r.headers['Content-length']
    
    print 'Client request new file. Size of the file: ', fileSize

      
    # Find the name of the file based on URL
    
    if fileurl.find('/'):
        print 'Getting ' + fileurl.rsplit('/', 1)[1]
    
        fileToClient = fileurl.rsplit('/', 1)[1]
    
    # Create an empty file to store the content of the file and open in write mode

    open(fileToClient, 'wb').write(r.content)
    
    #First: send the name of the file. We add "clientFile" to the name of the file

    message = "clientFile"+fileToClient
    serverSocket.sendto(message, clientAddress)
    
    #Second send the file to client. This is the main part
    
    serverSocket.sendto(fileToClient, clientAddress)
    
    f=open(fileToClient,"rb") # Open the file in read mode
    dataTosend = f.read(1024) # Read with 1024 bit buffer
    while (dataTosend):
        if(serverSocket.sendto(dataTosend,clientAddress)):
            dataTosend = f.read(1024)
            time.sleep(0.02)# Give receiver a bit time to save
    f.close()
    
    
    # Then wait for the BYE message from the client in order to close
    
    byeMessage,clientAddress  = serverSocket.recvfrom(2048)
    print 'From client: ' , byeMessage
    if byeMessage == 'BYE':
        print 'BYE message arrived, closing connection'
        
        # Now stop the timer, compute the elapsed time and send it to the client
        end = timer()
        totTime = (end - start)
        print 'Total time: ', totTime, 'sec.'
        print
        serverSocket.sendto(str(totTime), clientAddress)

