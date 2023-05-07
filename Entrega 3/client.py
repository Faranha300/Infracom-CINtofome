# Importação dos módulos socket e rdt
import socket
import rdt
import functions

# Definição do endereço IP e da porta utilizados
UDP_IP = socket.gethostbyname(socket.gethostname())
UDP_PORT = 5005
seq_num = 0
serverAddress = (UDP_IP, UDP_PORT)
# Criação do socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Loop principal
def run():
    print(functions.getDefaultMessage() + "Bem vindo ao CIntofome")
    print(functions.getDefaultMessage() + "Digite 'chefia' para chamar um garçon")
    while True:
        resp = input()
        if resp == "chefia":
            print(functions.getDefaultMessage() + "Por favor, digite seu nome e em qual mesa irá sentar:")
            resp = input()
            name, table = resp.split()
            message = (name, table)
            packet = rdt.Packet(seq_num, False, message)
            rdt.send_packet(sock, packet, serverAddress)
            break
        
    msg, address = sock.recvfrom(rdt.buf)
    packet = rdt.extract_packet(msg)
    print(packet.data)
    while True:
        resp = input()
        packet = rdt.Packet(seq_num, False, resp)
        rdt.send_packet(sock, packet, serverAddress)
        match(resp):
            case 1:
                pass
                
            case 2:
                msg, address = sock.recvfrom(rdt.buf)
                packet = rdt.extract_packet(msg)
                print(packet.data)
                order = input()
                packet = rdt.Packet(seq_num, False, order)
                rdt.send_packet(sock, packet, serverAddress)
                
            case 3:
                pass
                
            case 4:
                pass
                
            case 5:
                pass
                
            case 6:
                pass
            
run()
# Fechamento do socket
sock.close()
