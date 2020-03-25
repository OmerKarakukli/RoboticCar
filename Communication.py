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
            return 0
        except Exception as e:
            print(e)
            try:
                self.sock.sendto(msg, target)
                return 0
            except Exception as e:
                print(e)
                return 1

    def recvfrom(self, target, timeout=0.01, iterations=5):
        oldtimeout = self.sock.gettimeout()
        self.sock.settimeout(timeout)
        i = 1
        while i <= iterations:
            i = i + 1
            try:
                msg, address = self.sock.recvfrom(1024)
                if address == target:
                    self.sock.settimeout(oldtimeout)
                    return msg.decode('utf-8')
            except Exception as e:
                print(e)
                print('did not recv message from target:', target, 'iteration num:', i)
        self.sock.settimeout(oldtimeout)
        return None

    def recv(self, timeout=None):
        oldtimeout = self.sock.gettimeout()
        self.sock.settimeout(timeout)
        try:
            msg, address = self.sock.recvfrom(1024)
            self.sock.settimeout(oldtimeout)
            return msg.decode('utf-8'), address
        except IOError:  # Exception as e:
            # print(str(e) + ',no messages in socket:' + str(self.udp_address))
            return None, None


class ArduinoCom:

    def __init__(self, tty0='/dev/ttyACM0', tty1='/dev/ttyACM1', baudrate=115200):
        self.tty0 = tty0
        self.tty1 = tty1
        self.baudrate = baudrate
        self.serial = None
        self.bindSuccess = False
        self.init()

    def bind(self):
        try:
            self.serial = serial.Serial(self.tty0, self.baudrate)
            print('connected to /dev/ttyACM0')
            self.bindSuccess = True
            self.serial.flushInput()
            self.serial.flushOutput()
            self.serial.setRTS(0)
            sleep(2)
            self.serial.setRTS(1)
            sleep(2)
            return 0
        except Exception as e:
            print(e)
            try:
                self.serial = serial.Serial(self.tty1, self.baudrate)
                print('connected to /dev/ttyACM1')
                self.bindSuccess = True
                self.serial.setRTS(0)
                sleep(2)
                self.serial.setRTS(1)
                sleep(2)
                self.serial.flushInput()
                self.serial.flushOutput()
                return 0
            except Exception as e:
                print(e)
                self.bindSuccess = False
                return 1

    def init(self):
        self.bindSuccess = False
        while not self.bindSuccess:
            print('trying to bind')
            sleep(2)
            self.bind()
        return 0

    def send(self, msg):
        try:
            self.serial.write(bytes(msg + '\n', 'utf-8'))

        except Exception as e:
            print(e)
            self.init()
            self.send(msg)

    def recv(self, msg):
        try:
            self.send(msg)
            return self.serial.readline().strip().decode("ascii")

        except Exception as e:
            print(e)
            self.init()
            return self.recv(msg)
