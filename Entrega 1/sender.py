import socket
import time
import select

timeout = 3
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
buf = 1024

file_name = 'new_file.txt'
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

file_name = 'new_file.txt'.encode()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(file_name, (UDP_IP, UDP_PORT))
print("Sending %s ..." % file_name)

f = open(file_name, "rb")
data = f.read(buf)
while data:
    if sock.sendto(data, (UDP_IP, UDP_PORT)):
        data = f.read(buf)
        time.sleep(0.02)  # Give receiver a bit time to save
f.close()

f = open('received_file_from_server.txt', 'w+b')

data_recv, addr = sock.recvfrom(1024)
if data_recv:
    print("File name:", data_recv.decode())
    file_name = data_recv.strip()
    f.write(data_recv)

while True:
    ready = select.select([sock], [], [], timeout)
    if ready[0]:
        data_recv, addr = sock.recvfrom(1024)
        f.write(data_recv)
    else:
        print("%s Finish!" % file_name.decode())
        f.close()
        break

sock.close()
