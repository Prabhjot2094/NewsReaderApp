# client.py  
import socket
from threading import Thread

# create a socket object
def client_in_the_house(imt):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                        
	port = 50005
	s.connect(('127.0.0.1', port)) 

	s.send(imt+imt+imt+imt+imt+"Hello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client sideHello This is the client side\n")
	s.send('')
	while True:
		tm = s.recv(1024)
		if tm=='':
			break
		print tm                                     

	s.close()
	print "Socket Closed"

def main():
	i=0
	while i<9:
		i+=1
		t=Thread(target = client_in_the_house,args = str(i))
		t.start()

if __name__=="__main__":
	main()

#print("The time got from the server is %s" % tm.decode('ascii'))