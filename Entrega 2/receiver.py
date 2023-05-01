import socket
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
    print(f"Enviando: {packet.seq_n}")
    print(" " + str(len(packet.make_packet().encode('utf-8'))) + " bytes")
    sock.sendto(packet.make_packet().encode(), addr)

def send_ack(sock, seq_num, addr):
    packet = Packet(seq_num, True, 0, 0)
    print(f"Enviando ACK: {seq_num}")
    sock.sendto(packet.make_packet().encode(), addr)

def wait_for_ack(sock, expected_ack):
    try:
        ack = Packet(0, True, "")
        data, _ = sock.recvfrom(buf - ack.reading_size())
        ack = extract_packet(data)
        if ack.is_ack and expected_ack == ack.seq_n:
            print(f"ACK recebido: {ack.seq_n}")
            return True
        else:
            print(f"[ERRO] ACK: {ack.seq_n}, esperado: {expected_ack}")
            return False
    except socket.timeout:
        print(f"Tempo limite excedido: {timeout} segundos.")
        return False

def packet_loss(probability):
    return random.random() < probability


UDP_IP = "127.0.0.1"
UDP_PORT = 5005
buf = 1024
timeout = 40
loss_prob = 0.5

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.settimeout(timeout)
print("Aguardando arquivos.")
filename = ""

try:
    expected_seq_num = 0

    # pega nome
    data, addr = sock.recvfrom(buf)
    packet = extract_packet(data)

    if packet.seq_n == expected_seq_num:
        print(f"Arquivo recebido: {packet.data}")
        filename = packet.data
        send_ack(sock, packet.seq_n, addr)
        expected_seq_num = 1 - expected_seq_num
    else:
        print(f"[ERRO] ACK indevido: {packet.seq_n}, enviando ACK anterior")
        send_ack(sock, 1 - expected_seq_num, addr)

    client_fixed_addr = addr
    received_data = b""

    # recebe arquivo tamanho do buf
    while True:
        try:
           # pega packet
            data, addr = sock.recvfrom(buf)
            packet = extract_packet(data)
            if packet.seq_n == expected_seq_num:
                # checksum
                if packet.checksum ==  packet.real_checksum():
                    print(f"Pacote recebido: {packet.seq_n}")
                    send_ack(sock, packet.seq_n, addr)
                    expected_seq_num = 1 - expected_seq_num
                    received_data += packet.data.encode('utf-8')
                    if len(packet.data) + packet.reading_size() < buf:
                        break
                else:
                    print(f"[ERRO] Checksum: {packet.checksum}, esperado: {packet.real_checksum()}")
                    send_ack(sock, 1 - expected_seq_num, addr)
            else:
                print(f"Pacote incorreto: {packet.seq_n}, enviando ACK anterior")
                send_ack(sock, 1 - expected_seq_num, addr)
        except socket.timeout:
            print(
                f"Tempo limite excedido: {timeout} segundos. Encerrando...")
            break

    # salve arquivo
    with open("received_on_server_" + filename, "wb") as f:
        f.write(received_data)

    seq_num = 0

    # pega o arquivo salvo e manda de volta em parcelas tamanho do buf
    with open("received_on_server_" + filename, "rb") as f:
        packet = Packet(seq_num, False, "")
        data = f.read(buf - packet.reading_size())

        while data:
            # envia pedaço do arquivo q der respectivo tamanho bufas
            packet = Packet(seq_num, False, data.decode('utf-8'))
            
            send_packet(sock, packet, client_fixed_addr)
            ack_received = wait_for_ack(sock, seq_num)
            if ack_received:
                seq_num = 1 - seq_num

                packet = Packet(seq_num, False, "")
                data = f.read(buf - packet.reading_size())
            else:
                print("Reenviando pacote...")

except socket.timeout:
    f.close()
    print(
        f"Tempo limite excedido: {timeout} segundos. Encerrando...")

#fim
print('Finish.')
sock.close()
