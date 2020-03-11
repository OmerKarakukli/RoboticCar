import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDP_address = ('192.168.1.23', 10001)

try:
    sock.bind(UDP_address)
except Exception as e:
    print(e)
    exit()

while True:
    msg, address = sock.recvfrom(1024)
    sock.sendto(msg, ('127.0.0.1', 10000))
    while True:
        arduino_msg, arduino_address = sock.recvfrom(1024)
        if arduino_address[1] == 10000:
            break
    sock.sendto(arduino_msg, address)

