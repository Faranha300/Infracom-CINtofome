import socket

HOST = 'localhost'
PORT = 5000
dest = (HOST, PORT)

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind(('localhost', 3000))

print('para sair use CTRL+X\n')

while True:
    msg = input()
    udp.sendto(msg.encode(), dest)
    if (msg == '\x18'):
        break

udp.close()    