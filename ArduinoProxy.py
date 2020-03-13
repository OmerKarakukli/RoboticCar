import serial
from time import sleep
import socket
from Communication import ArduinoCom, UDP

UDP_global_address = ('127.0.0.1', 10000)

Ardu = ArduinoCom()
UDP_global = UDP(UDP_global_address)
UDP_global.bind()

while True:
    msg, address = UDP_global.recv()
    Ardu.send(msg)
    arduino_msg = Ardu.recv()
    UDP_global.sendto(arduino_msg, address)




# while True:
#     try:
#         msg, address = sock.recvfrom(1024)
#         msg = msg.decode('utf-8')
#         if msg == 'man':
#             state = 'man'
#         if msg == 'auto':
#             state = 'auto'
#         if state == 'auto':
#             arduino_Serial.write(bytes(msg + '\n', 'utf-8'))
#             arduinoIn = ""
#             sleep(0.1)
#             while arduino_Serial.inWaiting() > 0:
#                 arduinoIn = arduino_Serial.readline().strip().decode("ascii")
#                 if msg == 'frontDist' and address[1] == 10002:
#                     sock.sendto(bytes(arduinoIn, 'utf-8'), address)
#                 if address[1] != 10002:
#                     sock.sendto(bytes(arduinoIn, 'utf-8'), address)
#         if state == 'man' and address[1] == 10001:
#             arduino_Serial.write(bytes(msg + '\n', 'utf-8'))
#             arduinoIn = ""
#             sleep(0.1)
#             while arduino_Serial.inWaiting() > 0:
#                 arduinoIn = arduino_Serial.readline().strip().decode("ascii")
#                 if msg == 'frontDist' and address[1] == 10002:
#                     sock.sendto(bytes(arduinoIn, 'utf-8'), address)
#                 if address[1] != 10002:
#                     sock.sendto(bytes(arduinoIn, 'utf-8'), address)
#     except Exception as e:
#         print(e)
