import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDP_address = (socket.gethostname(), 10001)

try:
    sock.bind(UDP_address)
except Exception as e:
    print(e)
    exit()

while True:
    msg, address = sock.recvfrom(1024)
    print(msg.decode('utf-8'))
    sock.sendto(msg, ("127.0.0.1", 10000))
    arduino_msg, arduino_address = sock.recvfrom(1024)
    sock.sendto(arduino_msg, address)

