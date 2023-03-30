import socket
import time
import select

timeout = 3
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
buf = 1024
file_name = 'example.txt'.encode()


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(file_name, (UDP_IP, UDP_PORT))
print ("Sending %s ..." % file_name)

f = open(file_name, "rb")
data = f.read(buf)
while data:
    if sock.sendto(data, (UDP_IP, UDP_PORT)):
        data = f.read(buf)
        time.sleep(0.02) # Give receiver a bit time to save

data_recv, addr = sock.recvfrom(1024)
if data_recv:
    print("File name:", data_recv)
    file_name = data_recv.strip()

f = open('novo_arquivo.txt', 'wb')

while True:
    ready = select.select([sock], [], [], timeout)
    if ready[0]:
        data, addr = sock.recvfrom(1024)
        f.write(data)
    else:
        print("%s Finish!" % file_name)
        f.close()
        break

sock.close()
f.close()