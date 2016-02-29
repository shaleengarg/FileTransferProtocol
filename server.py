#!/usr/bin/python          

import socket               
import time
import os , sys
import re
from datetime import datetime
import hashlib
import re 

def md5(fname):
    hash = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash.update(chunk)
    return hash.hexdigest()


def send_file(filename):  
    if os.path.isfile(filename) == True:
        checksum = md5(filename)
        c.sendall(checksum + "<NULL>")
        txt = open(filename, 'r')
        for line in txt:
            c.send(line)

    else:
        c.send("File " + filename +  " does not exists in the current directory")
    c.send("None")

def udp():
    try :
        u = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print 'Socket created'
    except socket.error, msg :
        print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
     
     
    # Bind socket to local host and port
    try:
        u.bind((host, port2))
    except socket.error , msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
    return u

def usingudp(u):
        d = u.recvfrom(1024)
        addr = d[1]
        if os.path.isfile(d[0]) == True:
            checksum = md5(d[0])
            u.sendto(checksum , addr)
            txt = open(d[0], 'r')
            for line in txt:
                u.sendto(line , addr)
            u.sendto("NULL" , addr)
        else:
            u.sendto("NULL" , addr)
            u.sendto("File does not exist" , addr)   

if __name__ == "__main__" :

    s = socket.socket()         
    host = socket.gethostname() 
    port1 = 8000
    port2 = 8888
    s.bind((host, port1))        
    s.listen(5)
    newu = udp()
    while True:
        c, addr = s.accept()     
        print 'Got connection from', addr
        currentTime = time.ctime(time.time()) + "\r\n"
        c.send(currentTime.encode('ascii'))
        c.send('Thank you for connecting')
        data = "abc"
        history = []
        using_udp = 0
        while 1:
            data = c.recv(1024)
            m = re.search("(udp.*)", data)

            if m:
                using_udp=1
                usingudp(newu)

            else:
                request_command = filter(None, data.split(' ',10))
                verify_flag=0
                regex_flag=0
                
                if request_command[0] == "IndexGet" and request_command[1] == "longlist":
                    history.append(data+ "\n")
                    p = os.popen("ls -l | cut -d \' \' -f1,5- ")
                    
                    while 1:
                        line = p.readline()
                        if not line[-1:] : break
                        c.send(line)
                    c.send("None")

                elif request_command[0] == "IndexGet" and request_command[1] == "shortlist":
                    import datetime
                    history.append(data+ "\n")
                    p = os.popen('ls -l | awk -F \' \' {\'print $6,$7,$8\'}' , "r")

                    output = os.popen("ls -l | cut -d \' \' -f1,5- ")

                    temp = "20 " +  request_command[2] + " 00"  
                    starttime = (datetime.datetime(int(request_command[4]),int(time.strptime(temp, "%d %b %y")[1]),int(request_command[3]),0,0)-datetime.datetime(1970,1,1)).total_seconds()

                    temp = "20 " +  request_command[5] + " 00"  
                    endtime = (datetime.datetime(int(request_command[7]),int(time.strptime(temp, "%d %b %y")[1]),int(request_command[6]),0,0)-datetime.datetime(1970,1,1)).total_seconds()

                    while 1:
                        line = p.readline()
                        if not line[-1:] : break
                        final_output = output.readline()
                        if line.split(' ',3)[0].isalpha():   
                            temp = "20 " +  line.split(' ',3)[0] + " 00"  
                            month = time.strptime(temp, "%d %b %y")[1]
                            
                            if len((line.split(' ',4))[2].split(':',1)) == 2:
                                year = 2016
                            else:
                                year = line.split(' ' , 4)[2]

                            t = datetime.datetime(int(year),int(month),int(line.split(' ' , 4)[1]),0,0)
                            totalsec = (t-datetime.datetime(1970,1,1)).total_seconds()
                            if totalsec >= starttime and totalsec <= endtime:
                                c.send(final_output)
                    c.send("None")

                elif request_command[0] == "FileHash" and request_command[1] == "verify":
                    history.append(data+ "\n")
                    if os.path.isfile(request_command[2]) == True:
                        checksum = md5(request_command[2])
                    p = os.popen('ls -l | awk -F \' \' {\'print $6,$7,$8,$9\'}' , "r")
                    while 1:
                        line = p.readline()
                        if not line:
                            if verify_flag==0:
                                c.send("File of name \"" + request_command[2] + "\" does not exist")
                            c.send("None")
                            break

                        if line.split(' ',6)[0].isalpha():
                            if line.split(' ',6)[3] == request_command[2] + "\n" and os.path.isfile(request_command[2]) == True:
                                c.send(line.split(' ',6)[0] + " " + line.split(' ',6)[1] + " " + line.split(' ',6)[2] + " " + checksum)
                                verify_flag=1

                elif request_command[0] == "IndexGet" and request_command[1] == "regex":
                    p = os.popen('ls -l | awk -F \' \' {\'print $6,$7,$8,$9\'}' , "r")
                    while 1:
                        line = p.readline()
                        if not line:
                            if regex_flag==0:
                                c.send("ERROR: Invalid Regex")
                            c.send("None")
                            break
                        m = re.search(request_command[2],(line.split(' ',10)[3]).split('\n',2)[0])
                        if m:
                            c.send(line.split(' ',10)[3])
                            regex_flag=1


                elif request_command[0] == "FileHash" and request_command[1] == "checkall":
                    history.append(data+ "\n")
                    p = os.popen('ls -l | awk -F \' \' {\'print $6,$7,$8,$9\'}' , "r")
                    while 1:
                        line = p.readline()
                        if not line:
                            c.send("None")
                            break
                        if line.split(' ',6)[0].isalpha():
                            if os.path.isfile((line.split(' ',10)[3]).split('\n',2)[0]) == True:
                                checksum = md5((line.split(' ',10)[3]).split('\n',2)[0])
                                c.send(line.split(' ',6)[0] + " - " + line.split(' ',6)[1] + " - " + line.split(' ',6)[2] + " - " + (line.split(' ',10)[3]).split('\n',2)[0] + " || " + checksum + "\n")

                
                elif request_command[0] == "FileDownload" and request_command[1] == "tcp":
                    history.append(data + "\n")
                    send_file(request_command[2])
                
                elif request_command[0] == "exit":
                    c.send("Good Bye! None")          
                    c.close()
                    break

                elif request_command[0] == "history":
                    for x in xrange(0,len(history)):
                        c.send(history[x])
                    c.send("None")

                else:
                    history.append(data+ "\n")
                    c.send("None")

        c.close()
    s.close()
    u.close()