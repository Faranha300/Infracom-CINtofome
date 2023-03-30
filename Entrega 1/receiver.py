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
        print("File name:", data.decode())
        file_name = data.strip()

    f = open('received_file.txt', 'w+b')

    while True:
        ready = select.select([sock], [], [], timeout)
        if ready[0]:
            data, addr = sock.recvfrom(1024)
            f.write(data)
        else:
            print("%s Finish!" % file_name.decode())
            f.close()
            break

    f = open('received_file.txt', "rb")
    data_send = f.read(buf)
    while data_send:
        if sock.sendto(data_send, addr):
            data_send = f.read(buf)
            time.sleep(0.02)  # Give receiver a bit time to save