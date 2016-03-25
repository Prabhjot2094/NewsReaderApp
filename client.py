# client.py  
import os
import sys
import socket
from threading import Thread

# create a socket object
def seperate_files(x,directory):
	i=0

	if os.path.exists(directory)==False:
		os.mkdir(directory)

	while True:
		string = x[i]
		if string[-4:]==".jpg":
			f=open(directory+"\\"+string,"wb")
			i+=1
			f.write(x[i])
			i+=1
		elif string[-4:]==".txt":
			f=open(directory+"\\"+string,"wb")
			i+=1
			f.write(x[i])
			i+=1
		else:
			break

def client_in_the_house(imt,news_type):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                        
	port = 50011
	s.connect(('127.0.0.1', port)) 
	s.settimeout(5.0)
	f=open("success.txt","wb")
	#news_type = ["business","top"]


	s.send(news_type)
	print "NewsType sent"
	data = ''
	while True:
		print "Waiting to receive"
		tm = s.recv(512)

		if not tm:
			break
		data = data+tm
		f.write(tm)
		#print tm  
	x = data.split("hello")
	count = 0
	for txt in x:	
		count+=1
		print count,"\n",txt,"\n" 
	seperate_files(x,news_type)
	

	f.close()
	s.close()
	print "Socket Closed"

def main():
	i=0
	news_list = ["business","across_toi","latest","top_stories"]
	for news in news_list:
		t=Thread(target = client_in_the_house,args = {str(i),news})
		t.start()
		i+=1
		#break

if __name__=="__main__":
	main()

#print("The time got from the server is %s" % tm.decode('ascii'))