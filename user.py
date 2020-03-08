import socket
from time import sleep

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    user_msg = input("type your input:")
    sock.sendto(bytes(user_msg, 'utf-8'), ('192.168.1.23', 10001))
    sleep(0.2)
    back_msg, address = sock.recvfrom(1024)
    back_msg = back_msg.decode('utf-8')
    print(back_msg)
