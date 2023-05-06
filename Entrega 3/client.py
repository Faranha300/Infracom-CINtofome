import socket
import rdt

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
buf = 1024
timeout = 40
loss_prob = 0.5

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



##
filename = "arquivo_teste.txt"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Define um tempo limite para receber uma resposta do servidor (em segundos)
sock.settimeout(timeout)

seq_num = 0

# Envia o nome do arquivo para o servidor
packet = rdt.Packet(seq_num, False, filename)
rdt.send_packet(sock, packet, (UDP_IP, UDP_PORT))
if rdt.wait_for_ack(sock, seq_num):
    seq_num = 1 - seq_num
else:
    print("Resending...")

# Abre arquivo
with open(filename, "rb") as f:
    # le pelo tamanho do buf
    packet = rdt.Packet(seq_num, False, "") 
    data = f.read(buf - packet.reading_size())

    while data:
        # Envia pedaço usandoa logica do rdt3
        packet = rdt.Packet(seq_num, False, data.decode('utf-8'))
        if not rdt.packet_loss(loss_prob):
            rdt.send_packet(sock, packet, (UDP_IP, UDP_PORT))
            ack_received = rdt.wait_for_ack(sock, seq_num)
        else:
            print("[Pulando pacotes]")
            ack_received = False

        if ack_received:
            seq_num = 1 - seq_num

            data = f.read(buf - packet.reading_size())
        else:
            print("Resending packet...")

received_data = b""
while True:
    try:
        # pega o packet
        data, addr = sock.recvfrom(buf)
        packet = rdt.extract_packet(data)
        if packet.seq_n == seq_num:
            # checksum
            if packet.checksum == packet.real_checksum(): 
                print(f"Recebido: {packet.seq_n}")
                rdt.send_ack(sock, packet.seq_n, addr)
                seq_num = 1 - seq_num
                received_data += packet.data.encode('utf-8')
                if len(packet.data) + packet.reading_size() < buf:
                    break
            else:
                print(f"[Erro] Checksum: {packet.checksum}, esperado: {packet.real_checksum()}") 
                rdt.send_ack(sock, 1 - seq_num, addr)
        else:
            print(f"Pacote inesperado: {packet.seq_n}, enviando ACK anterior")
            rdt.send_ack(sock, 1 - seq_num, addr)
    except socket.timeout:
        print(
            f"Tempo limite excedido: {timeout} segundos. Encerrando...")
        break

# Salva arquivo
with open("received_on_client_" + filename, "wb") as f:
    f.write(received_data)

#fim
sock.close()