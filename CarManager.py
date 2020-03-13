import socket
from time import sleep
from Communication import UDP

state = 'auto'
front_dist_value = 300  #400
side_dist_value = 250   #300
back_value = 200    #200

UDP_address = ('127.0.0.1', 10002)
User_server_UDP_address = ('127.0.0.1', 10004)

UDP1 = UDP(UDP_address)
UDP1.bind()
UDP2 = UDP(User_server_UDP_address)
UDP2.bind()


def getDist():
    UDP1.sendto('dist', ('127.0.0.1', 10000))
    dist_array, address = UDP1.recv()
    dist_array = dist_array.split(',')
    for j in range(0, len(dist_array)):
        dist_array[j] = int(dist_array[j])
    return dist_array


while True:
    # sleep(0.25)
    user_msg, user_address = UDP2.recv(0)
    if user_msg == 'man' or user_msg == 'auto':
        if state == 'auto' and user_msg == 'man':
            UDP1.sendto('s', ('127.0.0.1', 10000))
            UDP1.recv()
            UDP2.sendto('changed to MANUAL MODE', user_address)

        elif state == 'auto' and user_msg == 'auto':
            UDP2.sendto('already in AUTO MODE', user_address)

        elif state == 'man' and user_msg == 'man':
            UDP2.sendto('already in MANUAL MODE', user_address)

        else:
            UDP2.sendto('changed to AUTO MODE', user_address)
        state = user_msg

    if state == 'auto':
        dist = getDist()
        print(dist)
        if (dist[1]+dist[2])/2 < back_value:
            UDP1.sendto('x', ('127.0.0.1', 10000))
            UDP1.recv()
            print("go Back")
            sleep(0.25)

        elif dist[1] < front_dist_value or dist[2] < front_dist_value:
            if dist[0] < dist[3]:
                UDP1.sendto('d', ('127.0.0.1', 10000))
                UDP1.recv()
                print("turn Right")
                sleep(0.5)
            elif dist[0] > dist[3]:
                UDP1.sendto('a', ('127.0.0.1', 10000))
                UDP1.recv()
                print("turn Left")
                sleep(0.5)
            else:
                if dist[1] < dist[2]:
                    UDP1.sendto('d', ('127.0.0.1', 10000))
                    UDP1.recv()
                    print("turn Right")
                    sleep(0.5)
                elif dist[1] > dist[2]:
                    UDP1.sendto('a', ('127.0.0.1', 10000))
                    UDP1.recv()
                    print("turn Left")
                    sleep(0.5)
                else:
                    UDP1.sendto('s', ('127.0.0.1', 10000))
                    UDP1.recv()
                    print("stop")
                    sleep(0.5)

        elif dist[0] < side_dist_value:
            UDP1.sendto('d', ('127.0.0.1', 10000))
            UDP1.recv()
            print("turn Right")
            sleep(0.5)

        elif dist[3] < side_dist_value:
            UDP1.sendto('a', ('127.0.0.1', 10000))
            UDP1.recv()
            print("turn Left")
            sleep(0.5)

        else:
            UDP1.sendto('w', ('127.0.0.1', 10000))
            UDP1.recv()
            print("go Forward")
    else:
        # print('ready')
        sleep(0.001)






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

