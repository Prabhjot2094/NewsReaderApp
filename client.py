import os
import sys
import socket
from threading import Thread
import time
import shutil	

def main():
	begin_time = time.time()

	news_list  = ["business","across_toi","latest","top_stories"]	
	
	i=0
	for news in news_list:
		print "NewsType sent = " , news
		#client(news)
		t=Thread(target = client,args = {news})
		t.start()
		#t.join()
		i+=1

	print "Time Taken = ",time.time()-begin_time

def client(news_type):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                        
	host = "127.0.0.1"
	port = 50011
	
	try :
		s.connect((host, port)) 

		s.settimeout(10.0)

		s.send(news_type)

		data = ''
		while True:
			tm = s.recv(512)
			if not tm:
				break
			data = data+tm
		
		# f1 = open(news_type+".txt",'w')	
		# f1.write(data)
		# f1.close()
		
		print "News Type ",news_type,"Recieved\n"

		s.shutdown(socket.SHUT_RDWR)
		
		print "Socket Shutdown Complete !!"

	except socket.error as msg :
		print 'Connect failed. \nError Code : ' + str(msg)
		sys.exit(0)

	split_data = data.split("aAaAaAaAaAaAaAaAaAaA")

	seperate_files(split_data,news_type)

def seperate_files(split_data,directory):
	
	if os.path.exists(directory)==True:
		shutil.rmtree(directory)
 
	os.mkdir(directory)

	i=0
	while True:
		name = split_data[i]
		if name[-4:]==".jpg":
			f=open(directory+"/"+name,"wb")
			i+=1
			f.write(split_data[i])
			i+=1
		elif name[-4:]==".txt":
			f=open(directory+"/"+name,"wb")
			i+=1
			f.write(split_data[i])
			i+=1
		else:
			break

if __name__=="__main__":
	 main()
