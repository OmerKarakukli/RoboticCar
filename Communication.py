class UDP:

    def __init__(self, udp_address):
        import socket
        self.IP = udp_address[0]
        self.PORT = udp_address[1]
        self.udp_address = udp_address
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def bind(self):
        try:
            self.sock.bind(self.udp_address)
            print('bind to socket:' + self.udp_address)
            return 0
        except Exception as e:
            print(e)
            return 1

    def sendto(self, msg, target):
        try:
            self.sock.sendto(bytes(msg, 'utf-8'), target)
        except Exception as e:
            print(e)
            self.sock.sendto(msg, target)

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
                print('didnt recv message from target:' + target + 'iteration num:' + i)
        return None


class ArduinoCom:

    def __init__(self, tty0='/dev/ttyACM0', tty1='/dev/ttyACM0',baudrate=115200):
        import serial
        self.baudrate = baudrate
        self.tty0 = tty0
        self.tty1 = tty1
        try:
            self.serial = serial.Serial('/dev/ttyACM0', 115200)
            print('connected to /dev/ttyACM0')
        except Exception as e:
            print(e)
            self.serial = serial.Serial('/dev/ttyACM1', 115200)
            print('connected to /dev/ttyACM1')

    def send(self, msg):
        self.serial.write(bytes(msg + '\n', 'utf-8'))

    def recv(self, timeout=0.01, iterations = 5):
        from time import sleep
        i = 1
        while True:
            if i > iterations:
                break
            i = i + 1
            while self.serial.inWaiting() > 0:
                return self.serial.readline().strip().decode("ascii")
            sleep(timeout)

