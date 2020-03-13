import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    user_msg = input("type your input:")
    sock.sendto(bytes(user_msg, 'utf-8'), ('192.168.1.22', 10001))
    back_msg, address = sock.recvfrom(1024)
    back_msg = back_msg.decode('utf-8')
    print(back_msg)
    # back_msg = back_msg.split(',')
    # for i in range(0, len(back_msg)):
    #     back_msg[i] = int(back_msg[i])
    # print(back_msg)
