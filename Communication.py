import socket
import serial
from time import sleep


class UDP:

    def __init__(self, udp_address):
        self.IP = udp_address[0]
        self.PORT = udp_address[1]
        self.udp_address = udp_address
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def bind(self):
        try:
            self.sock.bind(self.udp_address)
            print('bind to socket:', self.udp_address)
            return 0
        except Exception as e:
            print(e)
            return 1

    def sendto(self, msg, target):
        try:
            self.sock.sendto(bytes(msg, 'utf-8'), target)
        except Exception as e:
            print(e)
            try:
                self.sock.sendto(msg, target)
            except Exception as e:
                print(e)

    def recvfrom(self, target, timeout=0.01, iterations=5):
        self.sock.settimeout(timeout)
        i = 1
        while True:
            if i > iterations:
                break
            try:
                i = i + 1
                msg, address = self.sock.recvfrom(1024)
                if address == target:
                    return msg.decode('utf-8')
            except Exception as e:
                print(e)
                print('didnt recv message from target:', target, 'iteration num:', i)
        return None

    def recv(self, timeout=None):
        self.sock.settimeout(timeout)
        try:
            msg, address = self.sock.recvfrom(1024)
            return msg.decode('utf-8'), address
        except Exception as e:
            # print('no messages in socket:' + str(self.udp_address))
            return None, None


class ArduinoCom:

    def __init__(self, tty0='/dev/ttyACM0', tty1='/dev/ttyACM1', baudrate=115200):
        self.tty0 = tty0
        self.tty1 = tty1
        self.baudrate = baudrate
        self.serial = None
        self.bindSuccess = False
        while not self.bindSuccess:
            self.bind()

    def bind(self):
        try:
            self.serial = serial.Serial(self.tty0, self.baudrate)
            print('connected to /dev/ttyACM0')
            self.bindSuccess = True
            return 0
        except Exception as e:
            print(e)
            try:
                self.serial = serial.Serial(self.tty1, self.baudrate)
                print('connected to /dev/ttyACM1')
                self.bindSuccess = True
                return 0
            except Exception as e:
                print(e)
                self.bindSuccess = False
                return 1

    def re_init(self):
        self.bindSuccess = False
        while not self.bindSuccess:
            self.bind()

    def send(self, msg):
        try:
            self.serial.write(bytes(msg + '\n', 'utf-8'))
            return 0

        except Exception as e:
            print(e)
            self.re_init()
            return 'arduino lost connection and re_init'

    def recv(self):
        try:
            return self.serial.readline().strip().decode("ascii")

        except Exception as e:
            print(e)
            self.re_init()
            return 'arduino lost connection and re_init'


