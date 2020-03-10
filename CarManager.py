import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDP_address = ('127.0.0.1', 10002)

try:
    sock.bind(UDP_address)
except Exception as e:
    print(e)
    exit()

while True:
    sock.sendto(bytes('frontDist', 'utf-8'), ('127.0.0.1', 10000))
    while True:
        frontDist, arduino_address = sock.recvfrom(1024)
        if arduino_address[1] == 10000:
            break
    frontDist = int(frontDist.decode('utf-8'))
    if frontDist < 250:
        sock.sendto(bytes('a', 'utf-8'), ('127.0.0.1', 10000))
        while True:
            verify, arduino_address = sock.recvfrom(1024)
            if arduino_address[1] == 10000:
                break
    else:
        sock.sendto(bytes('w', 'utf-8'), ('127.0.0.1', 10000))
        while True:
            verify, arduino_address = sock.recvfrom(1024)
            if arduino_address[1] == 10000:
                break
