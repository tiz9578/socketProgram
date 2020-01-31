'''
Created on Jan 17, 2020

@author: tiz
'''
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
from thread import start_new_thread
  

serverPort = 4000
serverSocket = socket(AF_INET,SOCK_STREAM)

serverSocket.bind(('',serverPort))

serverSocket.listen(10)

#server in listening mode
print 'The server is ready to receive'

# We define a function that holds all the TCP version of the code
# skipping the connect part that will be postponed to the end in while loop

def client_thread(connectionSocket):

    
    connect_from_client = connectionSocket.recv(4000)
    print 'From client: '+ connect_from_client
    
    accept_connection = 'accept'
    connectionSocket.send(accept_connection)
    
    # Get the URL from the client
    
    fileurl = connectionSocket.recv(4000)
    
    #Try to get the total time for the process
    
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
        connectionSocket.send('Http Error')
        sys.exit(1)
    except requests.exceptions.ConnectionError as errcon:
        print ("Error Connecting:",errcon)
        connectionSocket.send('Connection Error')
        sys.exit(1)
    except requests.exceptions.Timeout as errTime:
        print ("Timeout Error:",errTime)
        connectionSocket.send('Timeout Error')
        sys.exit(1)
    except:
        print ("Generic Error")
        connectionSocket.send('Generic Error')
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
    connectionSocket.send(message)

    
    #Second send the file to client. This is the main part
    
    
    f=open(fileToClient,"rb") #Open the file in read mode 
    dataTosend = f.read(1024)
    while (dataTosend):
        if(connectionSocket.send(dataTosend)):
            dataTosend = f.read(1024)
            time.sleep(0.02)# Give receiver a bit time to save
    f.close()
      
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
        
# We set up a while loop in order to create a new thread for each new connection
#calling the function created at the beginning. 
        
while True:
    # blocking call, waits to accept a connection
    #conn, addr = s.accept()
    connectionSocket, addr = serverSocket.accept()
    print("[-] Connected to " + addr[0] + ":" + str(addr[1]))

    start_new_thread(client_thread, (connectionSocket,))

serverSocket.close()
