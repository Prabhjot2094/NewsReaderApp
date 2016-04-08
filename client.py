# client.py  
import os
import sys
import socket
from threading import Thread
import time
import shutil

# create a socket object
def seperate_files(x,directory):
	i=0

	if os.path.exists(directory)==True:
		shutil.rmtree(directory)
#	if os.path.exists(directory)==False:
	#time.sleep(3)
	os.mkdir(directory)

	while True:
		string = x[i]
		if string[-4:]==".jpg":
			f=open(directory+"/"+string,"wb")
			i+=1
			f.write(x[i])
			i+=1
		elif string[-4:]==".txt":
			f=open(directory+"/"+string,"wb")
			i+=1
			f.write(x[i])
			i+=1
		else:
			break

def client_in_the_house(imt,news_type):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                        
	host = "127.0.0.1"
	port = 50011

	port = socket.htons(50011)
	port = socket.htons(port)
	print port
	s.connect((host, port)) 
	s.settimeout(5.0)
	f=open("success.txt","wb")
	#news_type = ["business","top"]


	s.send(news_type)
	print "NewsType sent"
	data = ''
	while True:
		#print "Waiting to receive"
		tm = s.recv(512)

		if not tm:
			break
		data = data+tm
		f.write(tm)
		#print tm  
	f.close()
	x = data.split("helloFROMtheINSIDE")
	#count = 0
	# for txt in x:	
	# 	count+=1
	# 	print count,"\n",txt,"\n" 
	fx=open(news_type+".txt",'w')
	fx.write(data)
	fx.close()
	seperate_files(x,news_type)
	#s.shutdown(0)
	#s.close()
	print "Thread Closed but not socket"

def main():
	begin_time = time.time()
	cnt=0
	news_list = ["business","across_toi","latest","top_stories"]
	while cnt!=1 :	
		i=0
		cnt+=1
		for news in news_list:
			print news
			t=Thread(target = client_in_the_house,args = {str(i),news})
			t.start()
			#t.join()
			i+=1
			#break
	print time.time()-begin_time

if __name__=="__main__":
	main()

#print("The time got from the server is %s" % tm.decode('ascii'))