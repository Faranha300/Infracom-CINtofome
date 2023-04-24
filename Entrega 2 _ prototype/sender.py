import socket
import time
import random


class Packet: 

    def __init__(self, seq_n, is_ack, data, checksum=None):
        self.seq_n = seq_n
        self.is_ack = is_ack
        self.data = data
        self.checksum = checksum
        
        if is_ack == "True":
            is_ack = True
        if is_ack == "False":
            is_ack = False

        if checksum is None:
            self.checksum = self.real_checksum()

    def reading_size(self):
        _checksum = self.real_checksum()
        packet_return = (str(self.seq_n) + "|" + str(_checksum) + "|" + str(self.is_ack) + "|")
        return len(packet_return.encode('utf-8')) + 16 

    def make_packet(self):
        _checksum = self.real_checksum()
        packet_return = (str(self.seq_n) + "|" + str(_checksum) + "|" + str(self.is_ack) + "|" + str(self.data))
        return packet_return

    def real_checksum(self):
        data = str(self.seq_n) + str(self.is_ack) + str(self.data)
        data = data.encode()

        polynomial = 0x1021
        crc = 0xFFFF
        for byte in data:
            crc ^= (byte << 8)
            for _ in range(8):
                if (crc & 0x8000):
                    crc = (crc << 1) ^ polynomial
                else:
                    crc = (crc << 1)
        return crc & 0xFFFF

    def is_corrupt(self):
        return self.real_checksum() != self.checksum


def extract_packet(string_packet):
    seq_num, checksum_, is_ack, data = string_packet.decode().split("|", 3)
    return Packet(int(seq_num), is_ack, data, checksum=int(checksum_))

def send_packet(sock, packet, addr):
    print(f"Sending... : {packet.seq_n}")
    print(" " + str(len(packet.make_packet().encode('utf-8'))) + " bytes")
    sock.sendto(packet.make_packet().encode(), addr)

def send_ack(sock, seq_num, addr):
    packet = Packet(seq_num, True, 0, 0)
    print(f"Enviando ACK: {seq_num}")
    sock.sendto(packet.make_packet().encode(), addr)

# def make_ack_packet(seq_num):
#    return (str(seq_num) + "|ACK").encode()

def wait_for_ack(sock, expected_ack):
    try:
        ack = Packet(0, True, "")
        data, _ = sock.recvfrom(BUFFER_SIZE - ack.reading_size())
        ack = extract_packet(data)
        if ack.is_ack and expected_ack == ack.seq_n:
            print(f"ACK recebido: {ack.seq_n}")
            return True
        else:
            print(f"ACK incorreto: {ack.seq_n}, esperado: {expected_ack}")
            # exit()
            return False
    except socket.timeout:
        print(f"Tempo limite de {TIMEOUT_LIMIT} segundos atingido.")
        return False

def packet_loss(probability):
    return random.random() < probability


UDP_IP = "127.0.0.1"
UDP_PORT = 5005
BUFFER_SIZE = 1024
TIMEOUT_LIMIT = 40
perca_pacote_chance = 0.5



####

file_name = 'arquivo_teste.txt'
file = open(file_name, 'w')
file.write('Lorem ipsum dolor sit amet, consectetur adipiscing elit. In sit amet ornare odio, in pretium sem. Phasellus vitae augue nunc. Vivamus nunc nunc, elementum eu mi eget, aliquet finibus nisl. Fusce quis urna lorem. Donec vestibulum, ipsum id luctus pulvinar, nibh ligula posuere ante, sit amet imperdiet eros tortor nec nisl. Praesent pretium lobortis dapibus. Fusce sit amet finibus ante, id sodales tortor. Pellentesque lobortis massa vitae interdum gravida. Sed aliquam lacinia risus vitae ornare. Phasellus ultrices dolor a urna laoreet, id tempus dolor tempus. Quisque ut porttitor nisl. Nunc convallis nisl id tempus tempor. Integer cursus purus eget faucibus suscipit. Nulla eget arcu in dolor egestas tempor. Nullam luctus sit amet risus eget auctor.\
\
Cras id ullamcorper enim, vestibulum efficitur libero. Quisque porta eget diam a vestibulum. Aliquam vehicula nulla vitae nisl ornare, vitae rutrum urna eleifend. Morbi vulputate dolor a sem faucibus scelerisque. Phasellus ut porta dui, convallis imperdiet ex. Integer congue nisl ac erat aliquet gravida. Sed ut elit sem. Nam malesuada ac mi ac imperdiet. Fusce euismod ex quis lacinia mollis. Vestibulum et hendrerit dolor, ac malesuada magna. Maecenas pulvinar tincidunt risus vel faucibus. Mauris commodo mattis elit ullamcorper faucibus.\
\
Praesent fringilla pulvinar tellus, vitae posuere felis. Curabitur viverra maximus magna, et egestas sem semper eget. Sed gravida, turpis id convallis mattis, magna orci fermentum nisi, a elementum dui purus eu tellus. Mauris aliquam massa eget neque ultricies, ac semper lacus auctor. Maecenas maximus lectus lacus, eget cursus felis cursus at. Nulla luctus risus eu odio rhoncus, vel tincidunt magna tempus. Quisque dapibus dignissim eros vitae fringilla. Mauris ac mauris vel turpis euismod vestibulum a vel augue. Fusce non nulla nec mi tincidunt volutpat. Nam nec lorem ante. Proin pharetra dui quis massa viverra, in rutrum enim tincidunt. Duis cursus rutrum diam, suscipit volutpat libero tristique ut. Sed ornare tellus ut sapien vehicula, ac viverra mauris dapibus. Morbi sodales dictum erat, et blandit elit hendrerit eget.\
\
Sed iaculis erat ac nisl tempus ultricies. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Sed magna arcu, mattis ut pellentesque in, mattis in turpis. Aenean non bibendum justo. Fusce condimentum felis nec quam vulputate, sed scelerisque justo lobortis. Nulla facilisi. Aliquam congue enim est, sed tristique risus egestas eu. Etiam vel egestas erat. Integer laoreet sagittis scelerisque.\
\
Nam placerat risus eget volutpat congue. Phasellus nec tortor venenatis, porttitor augue in, fermentum quam. Nulla a enim ac felis viverra porttitor. Suspendisse fringilla odio sit amet tellus vestibulum pellentesque. Mauris vestibulum scelerisque posuere. Proin dolor elit, rutrum in risus id, feugiat mattis purus. Integer cursus feugiat risus nec sollicitudin. Vestibulum id eros feugiat leo vehicula tincidunt. Vivamus congue tellus sed ante scelerisque, et tempor leo porttitor. Morbi vel dolor erat. Pellentesque quis volutpat quam. In at congue mauris. Proin eu enim vel felis rutrum malesuada. Curabitur aliquet turpis non fermentum aliquet.')
file.close()



####
filename = "arquivo_teste.txt"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Define um tempo limite para receber uma resposta do servidor (em segundos)
sock.settimeout(TIMEOUT_LIMIT)

seq_num = 0

# Envia o nome do arquivo para o servidor
packet = Packet(seq_num, False, filename)
send_packet(sock, packet, (UDP_IP, UDP_PORT))
if wait_for_ack(sock, seq_num):
    seq_num = 1 - seq_num
else:
    print("Resending...")

# Abre o arquivo que será enviado
with open(filename, "rb") as f:
    # Lê o arquivo em pedaços de tamanho BUFFER_SIZE
    packet = Packet(seq_num, False, "") 
    data = f.read(BUFFER_SIZE - packet.reading_size())

    while data:
        # Envia o pedaço de arquivo para o servidor usando rdt3.0
        packet = Packet(seq_num, False, data.decode('utf-8'))
        if not packet_loss(PACKET_LOSS_PROB):
            send_packet(sock, packet, (UDP_IP, UDP_PORT))
            ack_received = wait_for_ack(sock, seq_num)
        else:
            print("[Pulando pacotes]")
            ack_received = False

        if ack_received:
            seq_num = 1 - seq_num

            data = f.read(BUFFER_SIZE - packet.reading_size())
        else:
            print("Resending packet...")

received_data = b""
while True:
    try:
        # Recebe um pacote do servidor
        data, addr = sock.recvfrom(BUFFER_SIZE)
        packet = extract_packet(data)
        if packet.seq_n == seq_num:
            # Avalia o checksum dele
            if packet.checksum == packet.real_checksum(): 
                print(f"Recebido: {packet.seq_n}")
                send_ack(sock, packet.seq_n, addr)
                seq_num = 1 - seq_num
                received_data += packet.data.encode('utf-8')
                if len(packet.data) + packet.reading_size() < BUFFER_SIZE:
                    break
            else:
                print(f"[Erro] Checksum: {packet.checksum}, esperado: {packet.real_checksum()}") 
                send_ack(sock, 1 - seq_num, addr)
        else:
            print(f"Pacote inesperado: {packet.seq_n}, enviando ACK anterior")
            send_ack(sock, 1 - seq_num, addr)
    except socket.timeout:
        print(
            f"Tempo limite excedido: {TIMEOUT_LIMIT} segundos. Encerrando...")
        break

# Salva o arquivo recebido
with open("received_on_client_" + filename, "wb") as f:
    f.write(received_data)

# Fecha o socket
sock.close()
