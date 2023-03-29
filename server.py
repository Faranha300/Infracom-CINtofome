import socket

HOST = 'localhost'
PORT = 5000
orig = (HOST, PORT)

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind(orig)

while True:
    msg, clientAddr = udp.recvfrom(1024)
    if (msg == '\x18'):
        break
    print(clientAddr, msg.decode())

udp.close()