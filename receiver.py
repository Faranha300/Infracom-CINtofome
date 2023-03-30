import socket
import select
import time

UDP_IP = "127.0.0.1"
IN_PORT = 5005
timeout = 3
buf = 1024


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, IN_PORT))

while True:
    data, addr = sock.recvfrom(1024)
    if data:
        print("File name:", data)
        file_name = data.strip()

    f = open('novo_arquivo.txt', 'w+b')

    while True:
        ready = select.select([sock], [], [], timeout)
        if ready[0]:
            data, addr = sock.recvfrom(1024)
            f.write(data)
        else:
            print("%s Finish!" % file_name)
            f.close()
            break
    f = open('novo_arquivo.txt', "rb")
    data = f.read(buf)
    while data:
        if sock.sendto(data, addr):
            data = f.read(buf)
            time.sleep(0.02)  # Give receiver a bit time to save