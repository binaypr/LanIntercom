import socket
import time
import sys
import subprocess
import selectors
import types


##
##result = subprocess.run('arp -a', stdout=subprocess.PIPE)
##string = result.stdout
##
##split = string.splitlines()
##dynamics = []
##
##for x in split:
##    x = str(x)
##    if "dynamic" not in x:
##        continue;
##    
##    cleaned = []
##    
##    for z in x.split(" "):
##        if len(z) > 2:
##            cleaned.append(z)
##    dynamics.append(cleaned)
##
##print(dynamics)
##
##
##retry = 2
##delay = 1
##timeout = 3
##
##def isOpen(ip, port):
##        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
##        s.settimeout(timeout)
##        try:
##                s.connect((ip, int(port)))
##                s.shutdown(socket.SHUT_RDWR)
##                return True
##        except:
##                return False
##        finally:
##                s.close()
##
##def checkHost(ip, port):
##        print("Checking: ", ip , ": ", port)
##        ipup = False
##        for i in range(retry):
##                if isOpen(ip, port):
##                        ipup = True
##                        break
##                else:
##                        time.sleep(delay)
##        return ipup
##
##iterdynamics = iter(dynamics)
##next(iterdynamics)

listofhosts = ['192.168.1.164', '192.168.1.223']
##
##
##for x in iterdynamics:
##    ip = x[0]
##    flag = False;
##    
##    if checkHost(ip, 445):
##        flag = True
##        print(ip + " is UP")
##    elif checkHost(ip, 139):
##        flag = True
##        print(ip + " is UP")
##    elif checkHost(ip, 138):
##        flag = True
##        print(ip + " is UP")
##    elif checkHost(ip, 135):
##        flag = True
##        print(ip + " is UP")
##    if flag:
##        listofhosts.append(ip)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(False)

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

host  = get_ip()
port =  1234
num_conns = 100
####


sel = selectors.DefaultSelector()


def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print("accepted connection from", addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
        else:
            print("closing connection to", data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print(data.outb.decode())
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]




lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print("listening on", (host, port))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()

        

