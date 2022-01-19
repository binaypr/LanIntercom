import os
import socket
import tkinter as tk

import threading
import selectors
import types
import pyttsx3
import concurrent.futures
import subprocess
import time


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


def startServer(window):
    
    host = get_ip()
    port = 2345
    num_conns = 1000

    sel = selectors.DefaultSelector()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(False)

    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.bind((host, port))
    lsock.listen()
    print("listening on", (host, port))
    print("\n"*2)
    print("--"*15)
    lsock.setblocking(False)
    sel.register(lsock, selectors.EVENT_READ, data=None)

    try:
        while True:
            events = sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    accept_wrapper(key.fileobj, sel)
                else:
                    service_connection(key, mask, sel, window)
    except KeyboardInterrupt:
        print("caught keyboard interrupt, exiting")
    finally:
        sel.close()

def service_connection(key, mask, sel, window):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024) 
        if recv_data:
            data.outb += recv_data
        else:
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            # PRINTS
            incoming = data.outb.decode()
            s = threading.Thread(target=readOutLoud, args=(incoming,))

            print("Incoming: ", incoming)
            q = threading.Thread(target = update, args=(window,incoming,))

            update(window, incoming)
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]

def readOutLoud(incoming):
    engine = pyttsx3.init()
    engine.say(incoming)
    engine.runAndWait()


def accept_wrapper(sock, sel):
    conn, addr = sock.accept()
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def gui(window, listofhosts):
    messages = tk.Text(font = ('calibre', 14, "normal"))
    messages.pack(fill ="both", expand = True)
    inputVar = tk.StringVar()

    inputField = tk.Text(font = ('calibre', 14, "normal"), height= .1)
    inputField.pack(fill= "both")
    message = inputField.get("1.0",tk.END)
    
    inputField.bind("<Return>", lambda eff: sendMessage(window, inputField, listofhosts, eff))


def sendMessage(window, inputField, listofhosts, event=None):
    message = inputField.get("1.0",tk.END)
    t = threading.Thread(target=sendtoHosts, args=(listofhosts, message,))
    t.start()
    window.winfo_children()[0].insert(tk.END, "Sent: ")
    window.winfo_children()[0].insert(tk.END, message)
    window.winfo_children()[0].insert(tk.END, "\n")
    inputField.delete('1.0',tk.END)
    t.join()

def sendtoHosts(listofhosts, message):
    for x in listofhosts:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((x, 2345))
                sendme = message
                s.sendall(sendme.encode())
                data = s.recv(1024)
                s.close()
                print("Was sent to: ", x)
        except:
            print("Was not sent to: ", x)
            pass
    

def update(window, message):
    window.winfo_children()[0].insert(tk.END, "Incoming: ")
    window.winfo_children()[0].insert(tk.END, message)
    window.winfo_children()[0].insert(tk.END, "\n")


def findListofIps():
    result = subprocess.run('arp -a', stdout=subprocess.PIPE)
    string = result.stdout

    split = string.splitlines()
    dynamics = []

    for x in split:
        x = str(x)
        if "dynamic" not in x:
            continue

        cleaned = []

        for z in x.split(" "):
            if len(z) > 2:
                cleaned.append(z)
        dynamics.append(cleaned)
    print(dynamics)
    return dynamics


def isOpen(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((ip, int(port)))
        s.shutdown(socket.SHUT_RDWR)
        return True
    except:
        return False
    finally:
        s.close()


def checkHost(ip, port):
    print("Checking: ", ip, ": ", port)
    ipup = False
    for i in range(retry):
        if isOpen(ip, port):
            ipup = True
            break
        else:
            time.sleep(delay)
    return ipup


def findlistofHosts():
    iterdynamics = iter(findListofIps())
    next(iterdynamics)
    returndicts = []

    # listofhosts = ['192.168.1.164', '192.168.1.223']
    for x in iterdynamics:
        ip = x[0]
        flag = False

        if checkHost(ip, 445):
            flag = True
            print(ip + " is UP")
        elif checkHost(ip, 139):
            flag = True
            print(ip + " is UP")
        # elif checkHost(ip, 138):
        #     flag = True
        #     print(ip + " is UP")
        # elif checkHost(ip, 135):
        #     flag = True
        #     print(ip + " is UP")
        if flag:
            print(ip)
            returndicts.append(ip)
    return returndicts
            

retry = 2
delay = 1
timeout = 3



window = tk.Tk()

with concurrent.futures.ThreadPoolExecutor() as executor:
    future = executor.submit(findlistofHosts)
    listofhosts = future.result()
    executor.shutdown()

print(listofhosts)

x = threading.Thread(target=startServer, args=(window,))
x.start()

y = threading.Thread(target=gui, args=(window, listofhosts))
y.start()


window.mainloop()
print("Done")


