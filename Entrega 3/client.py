# Importação dos módulos socket e rdt
import socket
import rdt

# Definição do endereço IP e da porta utilizados
UDP_IP = "127.0.0.1"
UDP_PORT = 5005

# Definição do tamanho do buffer e do tempo limite para recebimento de dados
buf = 1024
timeout = 40

# Definição da probabilidade de perda de pacotes
loss_prob = 0.5

# Criação do socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Definição do tempo limite para o socket
sock.settimeout(timeout)

# Definição do número de sequência inicial
seq_num = 0

# Variável que receberá a resposta do servidor
serverToUser = ""

# Loop principal
while True:
    # Exibição de mensagem ao usuário
    if serverToUser == " 1":
        print('UNO')
    elif serverToUser == " 2":
        print('DOS')
    elif serverToUser == " 3":
        print('TRES')
    elif serverToUser == " 4":
        print('QUATRO')
    elif serverToUser == " 5":
        print('CINCO')
    elif serverToUser == " 6":
        print('SEIS')
    else:
        pass
        #print('bruh???????? dafuck dawg shit nah hell nah')
        
    # Leitura de mensagem digitada pelo usuário
    message = input("Enter a message to send to server: ")

    # Criação do pacote a ser enviado
    packet = rdt.Packet(seq_num, False, " "+message)

    # Envio do pacote para o servidor
    rdt.send_packet(sock, packet, (UDP_IP, UDP_PORT))

    # Espera por uma resposta do servidor
    try:
        data, addr = sock.recvfrom(buf)
        packet = rdt.extract_packet(data)

        # Verificação do número de sequência do pacote recebido
        if packet.seq_n == seq_num:

            # Verificação da integridade do pacote recebido
            if packet.checksum == packet.real_checksum():

                # Exibição da mensagem recebida em letras maiúsculas
                #print(f"Received from server: {packet.data.upper()}")

                # Armazenamento da resposta do servidor
                serverToUser = packet.data

                # Alternância do número de sequência
                seq_num = 1 - seq_num
            else:
                pass
                #print(f"[Error] Checksum: {packet.checksum}, expected: {packet.real_checksum()}")
        else:
            #print(f"Unexpected packet: {packet.seq_n}, sending ACK for previous packet")
            rdt.send_ack(sock, 1 - seq_num, addr)
    except socket.timeout:
        #print(f"Timeout exceeded ({timeout} seconds).")
        break

# Fechamento do socket
sock.close()
