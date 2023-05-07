# Importando as bibliotecas necessárias
import socket
import rdt

# Definindo as constantes UDP_IP, UDP_PORT, buf, timeout e loss_prob
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
buf = 1024
timeout = 40
loss_prob = 0.5

# Inicializando as variáveis expected_seq_num e received_data e criando o socket
expected_seq_num = 0
received_data = b""
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Ligando o socket à porta e ao endereço IP especificados
sock.bind((UDP_IP, UDP_PORT))

# Configurando o tempo limite para a recepção de mensagens
sock.settimeout(timeout)

# Loop principal do servidor
while True:
    try:
        # Recebendo dados do socket
        data, addr = sock.recvfrom(buf)

        # Extraindo o pacote recebido usando a biblioteca rdt
        packet = rdt.extract_packet(data)

        # Verificando se o número de sequência esperado é igual ao número de sequência do pacote recebido
        if packet.seq_n == expected_seq_num:

            # Verificando se o checksum do pacote recebido é igual ao checksum calculado pelo protocolo rdt
            if packet.checksum == packet.real_checksum():

                # Se o pacote contém um ACK, atualize o número de sequência esperado
                if packet.data == "0" or packet.data == "1":
                    expected_seq_num = 1 - expected_seq_num

                # Se o pacote contém uma mensagem de dados, envie um ACK de confirmação e atualize o número de sequência esperado
                else:
                    response_packet = rdt.Packet(expected_seq_num, False, packet.data.upper())
                    rdt.send_packet(sock, response_packet, addr)
                    expected_seq_num = 1 - expected_seq_num

            # Se o checksum estiver incorreto, envie um ACK com o número de sequência anterior
            else:
                rdt.send_ack(sock, 1 - expected_seq_num, addr)

        # Se o número de sequência esperado for diferente do número de sequência do pacote recebido, envie um ACK com o número de sequência anterior
        else:
            rdt.send_ack(sock, 1 - expected_seq_num, addr)

    # Se ocorrer um timeout, encerre o loop
    except socket.timeout:
        break

# Fechando o socket
sock.close()
