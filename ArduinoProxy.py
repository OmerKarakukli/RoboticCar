from Communication import ArduinoCom, UDP

UDP_global_address = ('127.0.0.1', 10000)

UDP_global = UDP(UDP_global_address)
UDP_global.bind()

Ardu = ArduinoCom()

while True:
    msg, address = UDP_global.recv()
    arduino_msg = Ardu.recv(msg)
    UDP_global.sendto(arduino_msg, address)
