import serial
from time import sleep
import socket

try:
    arduino_Serial = serial.Serial('/dev/ttyACM0', 115200)
except Exception as e:
    print(e)
    arduino_Serial = serial.Serial('/dev/ttyACM1', 115200)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDP_address = ("127.0.0.1", 10000)

try:
    sock.bind(UDP_address)
except Exception as e:
    print(e)
    arduino_Serial.close()
    exit()

while True:
    msg, address = sock.recvfrom(1024)
    msg = msg.decode('utf-8')
    arduino_Serial.write(bytes(msg + '\n', 'utf-8'))
    arduinoIn = ""
    sleep(0.1)
    while arduino_Serial.inWaiting() > 0:
        arduinoIn = arduino_Serial.readline().strip().decode("ascii")
        sock.sendto(bytes(arduinoIn, 'utf-8'), address)

