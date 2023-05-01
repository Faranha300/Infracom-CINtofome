# Importando bibliotecas
import socket
import select
import time

# Definindo variáveis
UDP_IP = "127.0.0.1"
IN_PORT = 5005
timeout = 3
buf = 1024

# Criando socket e vinculando ao "cliente"
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, IN_PORT))

# Recebendo envios de 1024 em 1024 bits
while True:
    data, addr = sock.recvfrom(1024)
    if data:
        print("File name:", data.decode())
        file_name = data.strip()
    # Criando arquivo para armezanar os dados recebidos
    f = open('received_file.txt', 'w+b')
    # Armazenando os dados no arquivo
    while True:
        ready = select.select([sock], [], [], timeout)
        print(ready)
        if ready[0]:
            data, addr = sock.recvfrom(1024)
            f.write(data)
        else:
            print("%s Finish!" % file_name.decode())
            f.close()
            break
    # Enviando o arquivo gerado a partir do que foi recebido
    f = open('received_file.txt', "rb")
    data_send = f.read(buf)
    while data_send:
        if sock.sendto(data_send, addr):
            data_send = f.read(buf)
            time.sleep(0.02)  # Tempo para recebimento no destino
