# Importando as bibliotecas necessárias
import socket
import rdt
import functions

# Definindo as constantes UDP_IP, UDP_PORT, buf, timeout e loss_prob
UDP_IP = socket.gethostbyname(socket.gethostname())
UDP_PORT = 5005
buf = 1024
timeout = 40
loss_prob = 0.5

menu = [(1, "Hamburguer", 15.00),
        (2, "Pastel",     12.00),
        (3, "Coxinha",    10.00),
        (4, "Empada",      5.00),
        (5, "Sorvete",     7.00)]

serverToUser = ""
secondInput_var = 0
chefiaInput_var = 0
fifthInput_var = 0

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
        
        clientAddr = addr[0]+":"+str(addr[1])

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

                    
                    if packet.data == " 1" and secondInput_var == 0 and fifthInput_var == 0:
                        serverToUser = functions.getDefaultMessage() + functions.getMenu(menu)

                    elif packet.data == " 2" and secondInput_var == 0 and fifthInput_var == 0:
                        secondInput_var = 1
                        serverToUser = (functions.getDefaultMessage() + "Digite qual o primeiro item que gostaria (apenas o número):")
                        #functions.addOrder(packet.data, menu, clientAddr)
                        
                    elif packet.data == " 3" and secondInput_var == 0 and fifthInput_var == 0:
                        serverToUser = (functions.getDefaultMessage() + functions.getIndividualBill(menu, clientAddr)[0])

                    elif packet.data == " 4" and secondInput_var == 0 and fifthInput_var == 0:
                        serverToUser = (functions.getDefaultMessage() + functions.getTableBill(menu, clientAddr)[0])

                    
                    elif packet.data == " 5" and secondInput_var == 0 and fifthInput_var == 0:
                        fifthInput_var = 1
                        data, tableTotal, individualTotal = functions.getPayMessage(menu, clientAddr)

                        serverToUser = data

                     
                    elif packet.data == " 6" and secondInput_var == 0 and fifthInput_var == 0:
                        data, tableTotal, individualTotal = functions.getPayMessage(menu, clientAddr)
                        if individualTotal == 0.0:
                            serverToUser = functions.getDefaultMessage() + "Volte sempre ^^"
                            functions.delClient(clientAddr)
                            
                        else:
                            serverToUser = functions.getDefaultMessage() + "Você ainda não pagou sua conta"
                            
                
                    elif secondInput_var != 0 :
                        serverToUser = (functions.getDefaultMessage() + "Gostaria de mais algum item? (apenas o número/digite 'nao' para sair):")
                        if packet.data != " nao":
                            functions.addOrder(packet.data, menu, clientAddr)
                        else:
                            serverToUser = ""
                            secondInput_var = 0
                        #functions.addOrder(packet.data, menu, clientAddr)
                        #secondInput_var = 0
                        #serverToUser = ""
                        
                    elif fifthInput_var != 0:
                        data, tableTotal, individualTotal = functions.getPayMessage(menu, clientAddr)

                        serverToUser = data

                        print(float(packet.data))
                        
                        if individualTotal >= float(packet.data) and float(packet.data)<= tableTotal:
                            functions.payBill(float(packet.data), individualTotal, clientAddr)
                            serverToUser = "Conta paga."
                            fifthInput_var = 0
                            
    
                    elif packet.data == " chefia" and chefiaInput_var == 0:
                        chefiaInput_var = 1
                        serverToUser = (functions.getDefaultMessage() + "Por favor, digite seu nome e em qual mesa irá sentar:")                      


                    elif chefiaInput_var != 0:
                        serverToUser = functions.getDefaultMessage() + """Digite uma das opções a seguir (apenas o número):
                1 - Cardápio
                2 - Pedir
                3 - Conta individual
                4 - Conta da mesa
                5 - Pagar conta
                6 - Sair da mesa\n"""
                        
                        packet.data = packet.data.split(' ')
                        #print(packet.data)
                        functions.addClient((packet.data[1], int(packet.data[2])), clientAddr)
                        chefiaInput_var = 0



                    

                    response_packet = rdt.Packet(expected_seq_num, False, serverToUser)
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
