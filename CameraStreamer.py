import io
import struct
from time import sleep
from picamera import PiCamera
from Communication import UDP

UDP_manager = ('127.0.0.1', 10100)
UDP_user = ('192.168.1.162', 10101)

UDP1 = UDP(UDP_manager)
UDP2 = UDP(UDP_user)

UDP1.bind()
UDP2.bind()

# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
# client_socket = socket.socket()
# client_socket.connect(('192.168.1.189', 10100))

# Make a file-like object out of the connection
# connection = client_socket.makefile('wb')

camera = PiCamera(resolution=(640, 480), framerate=80)
#camera = PiCamera(resolution=(1280, 720), framerate=30)
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
# Finally, take several photos with the fixed settings
stream = io.BytesIO()
stream.seek(0)
stream.truncate()

while True:

    manager_msg, manager_address = UDP1.recv(timeout=0)
    user_msg, user_address = UDP2.recv(timeout=0)

    if user_msg == 'getFrame':
        camera.capture(stream, 'jpeg', use_video_port=True)
        UDP2.sendto(struct.pack('<L', stream.tell()), user_address)
        stream.seek(0)
        UDP2.sendto(stream.read(), user_address)
        stream.seek(0)
        stream.truncate()

    sleep(0.001)

# try:
#     camera = picamera.PiCamera()
#     camera.resolution = (640, 480)
#     camera.framerate = 60
#     # Start a preview and let the camera warm up for 2 seconds
#     # camera.start_preview()
#     time.sleep(2)
#
#     # Note the start time and construct a stream to hold image data
#     # temporarily (we could write it directly to connection but in this
#     # case we want to find out the size of each capture first to keep
#     # our protocol simple)
#     start = time.time()
#     stream = io.BytesIO()
#     for foo in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
#         # Write the length of the capture to the stream and flush to
#         # ensure it actually gets sent
#         connection.write(struct.pack('<L', stream.tell()))
#         connection.flush()
#         # Rewind the stream and send the image data over the wire
#         stream.seek(0)
#         connection.write(stream.read())
#         # If we've been capturing for more than 5 seconds, quit
#         if time.time() - start > 10:
#             break
#         # Reset the stream for the next capture
#         stream.seek(0)
#         stream.truncate()
#     # Write a length of zero to the stream to signal we're done
#     connection.write(struct.pack('<L', 0))
# finally:
#     connection.close()
#     client_socket.close()
