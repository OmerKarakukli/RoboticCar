import socket
from time import sleep
from Communication import UDP

UDP_address = ('127.0.0.1', 10002)

UDP1 = UDP(UDP_address)
UDP1.bind()


def getDist():
    UDP1.sendto('dist', ('127.0.0.1', 10000))
    dist_array, address = UDP1.recv()
    dist_array = dist_array.split(',')
    for j in range(0, len(dist_array)):
        dist_array[j] = int(dist_array[j])
    return dist_array


while True:
    # sleep(0.01)
    dist = getDist()
    print(dist)
    if dist[1] < 250 or dist[2] < 250:
        if dist[0] <= dist[3]:
            UDP1.sendto('d', ('127.0.0.1', 10000))
            UDP1.recv()
            print("turn Right")
        else:
            UDP1.sendto('a', ('127.0.0.1', 10000))
            UDP1.recv()
            print("turn Left")

    elif dist[0] < 250:
        UDP1.sendto('d', ('127.0.0.1', 10000))
        UDP1.recv()
        print("turn Right")

    elif dist[3] < 250:
        UDP1.sendto('a', ('127.0.0.1', 10000))
        UDP1.recv()
        print("turn Left")

    else:
        UDP1.sendto('w', ('127.0.0.1', 10000))
        UDP1.recv()
        print("go Forward")






# while True:
#     # sock.sendto(bytes('frontDist', 'utf-8'), ('127.0.0.1', 10000))
#     try:
#         while True:
#             frontDist, arduino_address = sock.recvfrom(1024)
#             if arduino_address[1] == 10000:
#                 break
#         frontDist = int(frontDist.decode('utf-8'))
#         print(frontDist)
#         if frontDist < 250:
#             sock.sendto(bytes('a', 'utf-8'), ('127.0.0.1', 10000))
#             sleep(1)
#         else:
#             sock.sendto(bytes('w', 'utf-8'), ('127.0.0.1', 10000))
#     except Exception as e:
#         print(e)

