# Importando as bibliotecas necessárias
import socket
import rdt
import functions

# Definindo as constantes UDP_IP, UDP_PORT, buf, timeout e loss_prob
UDP_IP = socket.gethostbyname(socket.gethostname())
UDP_PORT = 5005

# Inicializando as variáveis expected_seq_num e criando o socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
seq_num = 0
menu = [(1, "Hamburguer", 15.00),
        (2, "Pastel",     12.00),
        (3, "Coxinha",    10.00),
        (4, "Empada",      5.00),
        (5, "Sorvete",     7.00)]

# Ligando o socket à porta e ao endereço IP especificados
sock.bind((UDP_IP, UDP_PORT))

def run():
    while True:
        msg, address = sock.recvfrom(rdt.buf)
        clientAddress = str(address[0]) + ":" + str(address[1])
        packet = rdt.extract_packet(msg)
        msg = packet.data[2:-2] 
        name, table = msg.split("', '")
        functions.addClient((name, int(table)), clientAddress)
        
        msg = functions.getDefaultMessage() + """Digite uma das opções a seguir (apenas o número):
                        1 - Cardápio
                        2 - Pedir
                        3 - Conta individual
                        4 - Conta da mesa
                        5 - Pagar conta
                        6 - Sair da mesa\n"""
        packet = rdt.Packet(seq_num, False, msg)
        rdt.send_packet(sock, packet, address)
        break

    while True:
        msg, clientAddress = sock.recvfrom(rdt.buf)
        packet = rdt.extract_packet(msg)
        match(int(packet.data)):
            case 1:
                pass
        
            case 2:
                msg = functions.getDefaultMessage() + "Digite qual o primeiro item que gostaria (apenas o número):"
                packet = rdt.Packet(seq_num, False, msg)
                rdt.send_packet(sock, packet, address)
                msg, address = sock.recvfrom(rdt.buf)
                packet = rdt.extract_packet(msg)
                order = packet.data
                print(order)
                functions.addOrder(order, menu, clientAddress)     
            case 3:
                pass
                        
            case 4:
                pass
                        
            case 5:
                pass
                        
            case 6:
                pass


run()
sock.close()
