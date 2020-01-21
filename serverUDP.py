'''
Created on Jan 17, 2020

@author: tiz
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

#serverSocket.listen(1)
print 'The server is ready to receive'
while 1:

    connect_from_client, clientAddress = serverSocket.recvfrom(2048)
    print 'From client: '+ connect_from_client

    accept_connection = 'accept'
    serverSocket.sendto(accept_connection, clientAddress)





    fileurl, clientAddress = serverSocket.recvfrom(2048)
    #connectionSocket, addr = serverSocket.accept()
    #fileurl = connectionSocket.recv(4000)
    #Try to get the total time for the process
    start = timer()

    try:
        r = requests.get(fileurl, allow_redirects=True)
        r.raise_for_status() 
    except requests.exceptions.HTTPError as err:
        print err
        serverSocket.sendto('Http Error', clientAddress)
        #connectionSocket.send('Http error')
        sys.exit(1)
    except requests.exceptions.ConnectionError as errcon:
        print ("Error Connecting:",errcon)
        serverSocket.sendto('Connection Error', clientAddress)
        sys.exit(1)
    except requests.exceptions.Timeout as errTime:
        print ("Timeout Error:",errTime)
        serverSocket.sendto('Timeout Error', clientAddress)
        sys.exit(1)
    #except:
     #   print ("Generic Error")
      #  serverSocket.sendto('Generic Error', clientAddress)
       # sys.exit(1)
    
    
    # Check the file size
    fileSize = r.headers['Content-length']
    
    print 'Client request new file. Size of the file: ', fileSize

      
    # Find the name of the file based on URL
    if fileurl.find('/'):
        print 'Getting ' + fileurl.rsplit('/', 1)[1]
       # fileToClient = fileurl.rsplit('/', 1)[1]
        fileToClient = fileurl.rsplit('/', 1)[1]
    
    # Create an empty file to store the content of the file
    #######OKOK open(fileToClient, 'wb').write(r.content)
    open(fileToClient, 'wb').write(r.content)
    
    
    
    #First: send the size of the file from the header to the client to compare

    #connectionSocket.send(fileSize)
    message = "clientFile"+fileToClient
    serverSocket.sendto(message, clientAddress)
    #serverSocket.sendto(fileToClient, clientAddress)
    
    #Second send the file to client
    
    #connectionSocket.send(fileToClient)
    serverSocket.sendto(fileToClient, clientAddress)
    
    f=open(fileToClient,"rb")
    dataTosend = f.read(1024)
    while (dataTosend):
        if(serverSocket.sendto(dataTosend,clientAddress)):
            #print "sending ..."
            dataTosend = f.read(1024)
            time.sleep(0.02)# Give receiver a bit time to save
    f.close()
    
    #Send the size:
    
    
    
    # Then wait for the BYE message from the client in order to close
    
    #byeMessage = connectionSocket.recv(4000)
    byeMessage,clientAddress  = serverSocket.recvfrom(2048)
    print 'From client: ' , byeMessage
    if byeMessage == 'BYE':
        print 'BYE message arrived, closing connection'
        
        # Now stop the timer, compute the elapsed time and send it to the client
        end = timer()
        totTime = (end - start)
        print 'Total time: ', totTime, 'sec.'
        print
        #connectionSocket.send(str(timeTodw))
        serverSocket.sendto(str(totTime), clientAddress)
        #serverSocket.close()

