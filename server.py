'''
    Simple socket server using threads
'''
import socket
import sys
from threading import Thread
import threading
import os


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
        sys.exit(0)

    s.listen(0)
    print 'Socket now listening'
     
    i=0
    while 1:
        i+=1
        conn, addr = s.accept()
        print 'Connected with ' + addr[0] + ':' + str(addr[1])
        t=Thread(target = clientThread,args = (conn,))
        t.start()
        print threading.activeCount();


def clientThread(conn):

    try:
        news_type = conn.recv(512)
        arr = get_filenames(news_type)

        for item in arr:
            item_name = item.split('/') 
            item_name = item_name[-1:]
            conn.send(item_name[0]+"aAaAaAaAaAaAaAaAaAaA")
            f=open(item,"rb")
            
            i=0
            while True:
                i+=1 
                data = f.read(512)
                if not data:
                    break    
                conn.send(data)
            conn.send("aAaAaAaAaAaAaAaAaAaA")
            f.close()

        conn.close()    

    except socket.error as msg:
        print 'Connect failed. \nError Code : ' + str(msg[0]) + ' \nMessage :' + msg[1]
        return

def get_filenames(location):
    #print location
    files = os.listdir("F:/News/"+location+"/")
    arr = []
    for i in files:
        directory = "F:/News/"+location+"/"+i
        arr.append(directory)
    return arr

if __name__=="__main__":
    main()

