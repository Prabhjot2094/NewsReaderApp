'''
    Simple socket server using threads
'''
 
import socket
import sys
from threading import Thread
import threading
import time 
from functions import *


def clientThread(conn):
    i=0

    print "waitiing for recieving"
    news_type = conn.recv(512)
    print news_type
    arr = get_filenames(news_type)
    #print "Sending"

    for item in arr:
        item_name = item.split('\\') 
        item_name = item_name[-1:]
        #print "Sending ",item
        conn.send(item_name[0]+"helloFROMtheINSIDE")
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
        conn.send("helloFROMtheINSIDE")

    conn.close()

def main():
    HOST = '0.0.0.0' 
    PORT = 50011

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print 'Socket created'

    try:
        s.bind((HOST, PORT))
        print 'Socket bind complete'
    except socket.error as msg:
        print 'Bind failed. \nError Code : ' + str(msg[0]) + ' \nMessage :' + msg[1]
        sys.exit()

    s.listen(0)
    print 'Socket now listening'
     
    i=0
    while 1:
        i+=1
        conn, addr = s.accept()
        print 'Connected with ' + addr[0] + ':' + str(addr[1])
        t=Thread(target = clientThread,args = (conn,))
        #clientThread(conn)
        # print "Thread ",i," Active\n"
        t.start()
        print threading.enumerate()
    print "##################################################################################################################################################################################################################################################################################"
    s.close()

if __name__=="__main__":
    main()

