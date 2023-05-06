import socket
import rdt

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
    packet = rdt.extract_packet(data)

    if packet.seq_n == expected_seq_num:
        print(f"Arquivo recebido: {packet.data}")
        filename = packet.data
        rdt.send_ack(sock, packet.seq_n, addr)
        expected_seq_num = 1 - expected_seq_num
    else:
        print(f"[ERRO] ACK indevido: {packet.seq_n}, enviando ACK anterior")
        rdt.send_ack(sock, 1 - expected_seq_num, addr)

    client_fixed_addr = addr
    received_data = b""

    # recebe arquivo tamanho do buf
    while True:
        try:
           # pega packet
            data, addr = sock.recvfrom(buf)
            packet = rdt.extract_packet(data)
            if packet.seq_n == expected_seq_num:
                # checksum
                if packet.checksum ==  packet.real_checksum():
                    print(f"Pacote recebido: {packet.seq_n}")
                    rdt.send_ack(sock, packet.seq_n, addr)
                    expected_seq_num = 1 - expected_seq_num
                    received_data += packet.data.encode('utf-8')
                    if len(packet.data) + packet.reading_size() < buf:
                        break
                else:
                    print(f"[ERRO] Checksum: {packet.checksum}, esperado: {packet.real_checksum()}")
                    rdt.send_ack(sock, 1 - expected_seq_num, addr)
            else:
                print(f"Pacote incorreto: {packet.seq_n}, enviando ACK anterior")
                rdt.send_ack(sock, 1 - expected_seq_num, addr)
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
        packet = rdt.Packet(seq_num, False, "")
        data = f.read(buf - packet.reading_size())

        while data:
            # envia pedaço do arquivo q der respectivo tamanho bufas
            packet = rdt.Packet(seq_num, False, data.decode('utf-8'))
            
            rdt.send_packet(sock, packet, client_fixed_addr)
            ack_received = rdt.wait_for_ack(sock, seq_num)
            if ack_received:
                seq_num = 1 - seq_num

                packet = rdt.Packet(seq_num, False, "")
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