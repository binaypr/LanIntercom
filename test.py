import socket

HOST = '192.168.1.62'
PORT = int('1234')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    sendme = input()
    s.sendall(sendme.encode())
    data = s.recv(1024)

