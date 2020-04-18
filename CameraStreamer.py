import io
import struct
from time import sleep
from picamera import PiCamera
from Communication import UDP
import socket

local_UDP_address = ('192.168.1.162', 10100)
local_TCP_address = ('192.168.1.162', 10101)

local_UDP = UDP(local_UDP_address)
local_UDP.bind()

stream_socket = socket.socket()
stream_socket.bind(local_TCP_address)
stream_socket.listen(0)

stream_connection = stream_socket.accept()[0].makefile('wb')

camera = PiCamera(resolution=(640, 480), framerate=80)
# camera = PiCamera(resolution=(1280, 720), framerate=30)
# Set ISO to the desired value
camera.iso = 100
# Wait for the automatic gain control to settle
sleep(2)
# Now fix the values
camera.shutter_speed = camera.exposure_speed
camera.exposure_mode = 'off'
g = camera.awb_gains
camera.awb_mode = 'off'
camera.awb_gains = g
# create the steam from bytesIO
stream = io.BytesIO()
stream.seek(0)
stream.truncate()

while True:

    client_msg, client_address = local_UDP.recv()
    if client_msg == 'getFrame':
        camera.capture(stream, 'jpeg', use_video_port=True)
        image_len = stream.tell()
        stream.seek(0)  # return to stream start
        print('image_len = ', image_len)
        stream_connection.write(stream.read())
        stream_connection.flush()
        local_UDP.sendto(str(struct.pack('<L', image_len)), client_address)
        stream.seek(0)
        stream.truncate()
