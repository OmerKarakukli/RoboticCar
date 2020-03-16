from Communication import UDP

# import socket
#
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDP_user = ('192.168.1.22', 10001)
# UDP_user = ('192.168.1.31', 10001)
UDP_ardu = ('127.0.0.1', 10003)
UDP_manager = ('127.0.0.1', 10005)
#
# try:
#     sock.bind(UDP_user)
# except Exception as e:
#     print(e)
#     exit()
#
# while True:
#     msg, address = sock.recvfrom(1024)
#     sock.sendto(msg, ('127.0.0.1', 10000))
#     while True:
#         arduino_msg, arduino_address = sock.recvfrom(1024)
#         if arduino_address[1] == 10000:
#             break
#     sock.sendto(arduino_msg, address)


UDP1 = UDP(UDP_user)
UDP2 = UDP(UDP_ardu)
UDP3 = UDP(UDP_manager)
UDP1.bind()
UDP2.bind()
UDP3.bind()
# msg, address = UDP1.recv()
while True:
    msg, address = UDP1.recv()
    if msg == 'auto' or msg == 'man':
        UDP3.sendto(msg, ('127.0.0.1', 10004))
        manager_msg, manager_address = UDP3.recv()
        UDP1.sendto(manager_msg, address)
    else:
        UDP2.sendto(msg, ('127.0.0.1', 10000))
        arduino_msg = UDP2.recvfrom(('127.0.0.1', 10000), None)
        UDP1.sendto(arduino_msg, address)
    # msg, address = UDP1.recv()
    # while address == ('127.0.0.1', 10000):
    #       msg, address = UDP1.recv()

