import serial
from time import sleep
import socket

state = 'auto'

try:
    arduino_Serial = serial.Serial('/dev/ttyACM0', 115200)
    print('connected to /dev/ttyACM0')
except Exception as e:
    print(e)
    arduino_Serial = serial.Serial('/dev/ttyACM1', 115200)
    print('connected to /dev/ttyACM1')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDP_address = ('127.0.0.1', 10000)

try:
    sock.bind(UDP_address)
    print('bind to socket:', UDP_address)
except Exception as e:
    print(e)
    arduino_Serial.close()
    exit()

while True:
    try:
        msg, address = sock.recvfrom(1024)
        msg = msg.decode('utf-8')
        if msg == 'man':
            state = 'man'
        if msg == 'auto':
            state = 'auto'
        if state == 'auto':
            arduino_Serial.write(bytes(msg + '\n', 'utf-8'))
            arduinoIn = ""
            sleep(0.1)
            while arduino_Serial.inWaiting() > 0:
                arduinoIn = arduino_Serial.readline().strip().decode("ascii")
                if msg == 'frontDist' and address[1] == 10002:
                    sock.sendto(bytes(arduinoIn, 'utf-8'), address)
                if address[1] != 10002:
                    sock.sendto(bytes(arduinoIn, 'utf-8'), address)
        if state == 'man' and address[1] == 10001:
            arduino_Serial.write(bytes(msg + '\n', 'utf-8'))
            arduinoIn = ""
            sleep(0.1)
            while arduino_Serial.inWaiting() > 0:
                arduinoIn = arduino_Serial.readline().strip().decode("ascii")
                if msg == 'frontDist' and address[1] == 10002:
                    sock.sendto(bytes(arduinoIn, 'utf-8'), address)
                if address[1] != 10002:
                    sock.sendto(bytes(arduinoIn, 'utf-8'), address)
    except Exception as e:
        print(e)
