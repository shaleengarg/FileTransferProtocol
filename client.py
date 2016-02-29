#!/usr/bin/python           
import socket               
import time
import os ,sys
import hashlib
import re 

def md5(fname):
    hash = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash.update(chunk)
    return hash.hexdigest()

def udp():
	try:
	    u = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	except socket.error:
	    print 'Failed to create socket'
	    sys.exit()
	return u

if __name__ == "__main__" :

	s = socket.socket()         
	host = socket.gethostname() 
	port1 = 8000          
	port2 = 8888      
	s.connect((host, port1))
	tm = s.recv(1024)
	print "Connection Time:  " , tm
	request = "null"

	break_flag=0
	m_flag=0
	content =""
	u = udp()

	while request != "exit":
		request = raw_input('$> ')
		request_command = filter(None, request.split(' ',10))	
		s.sendall(request)
		content =""
		list1 = []
		break_flag=0
		m_flag=0
		m = re.search("(udp.*)", request)
		if not m:
			while 1:
				data = s.recv(1024)

				if request_command[0] == "FileDownload":
					m = re.search("(<NULL>.*)", data)
					if m:
						list1 = filter(None, data.split('<NULL>',10))
						initial_checksum = list1[0]
						m_flag=1

					else:		
						if m_flag==0:
							print "File " + request_command[2] +  " does not exist in the current directory"
							break
						if data[-4:] == "None":
							content = content +  data[:-4]
							break_flag=1
						else:
							content = content + data

					if break_flag==1:
							with open(request_command[2], 'wb') as download_file:
								download_file.write(content)

							final_checksum = md5(request_command[2])
							if final_checksum != initial_checksum:
								os.remove(request_command[2])
							else:
								statinfo = os.stat(request_command[2])
								print "Size: " , statinfo.st_size , "File name: " , request_command[2] , "MD5: " , final_checksum
							break

				elif data[-4:] == "None" and request_command[0] != "FileDownload":
					print data[:-4]
					break

				else:	
					print data
		elif request_command[1] == "udp":
			    msg = request_command[2]
			     
			    try :
			        u.sendto(msg, (host, port2))
			        
			        check = u.recvfrom(1024) 
			        checksumudp = check[0]

			        d = u.recvfrom(1024)
			        reply = d[0]
			        addr = d[1]

			        if checksumudp == "NULL":
						print reply				    

			        elif checksumudp != "NULL":
				       	with open(request_command[2], 'wb') as download_file: 
				        	while reply != "NULL":
					        	download_file.write(reply)
					        	d = u.recvfrom(1024)
					        	reply = d[0]

						statinfo = os.stat(request_command[2])
						print "File name: " , request_command[2] , "MD5: " , checksumudp

			    except socket.error, msg:
			        print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
			        sys.exit()
	s.close()
