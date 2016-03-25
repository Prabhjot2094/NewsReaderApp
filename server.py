'''
    Simple socket server using threads
'''
 
import socket
import sys
from threading import Thread
import time 
from functions import *


def clientThread(conn):
    i=0

    print "waitiing for recieving"
    news_type = conn.recv(512)
    arr = get_filenames(news_type)
    #print "Sending"

    for item in arr:
        item_name = item.split('\\') 
        item_name = item_name[-1:]
        print "Sending ",item
        conn.send(item_name[0]+"hello")
        f=open(item,"rb")
        #infinite loop so that function do not terminate and thread do not end.
        while True:
            i+=1 
            #print i
            data = f.read(4096)
            if not data:
                break
            conn.send(data)
        f.close()
        conn.send("hello")

    conn.close()

HOST = '127.0.0.1' 
PORT = 50011 # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
print 'Socket bind complete'

s.listen(10)
print 'Socket now listening'
 
i=0
#now keep talking with the client
while 1:
    i+=1
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    #Thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    t=Thread(target = clientThread,args = (conn,))
    print "Thread ",i," Active"
    t.start()
print "##################################################################################################################################################################################################################################################################################"
s.close()

