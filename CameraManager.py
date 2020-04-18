import io
import socket
import struct
from PIL import Image
from time import sleep
from Communication import UDP

local_UDP_address = ('192.168.1.162', 10102)
remote_TCP_address = ('192.168.1.162', 10101)
remote_UDP_address = ('192.168.1.162', 10100)   # CameraStreamer UDP

local_UDP = UDP(local_UDP_address)
local_UDP.bind()

remote_TCP = socket.socket()
remote_TCP.connect(remote_TCP_address)
stream_connection = remote_TCP.makefile('rb')

# create the steam from bytesIO
stream = io.BytesIO()
stream.seek(0)
stream.truncate()

while True:

    local_UDP.sendto('getFrame', remote_UDP_address)
    image_len = struct.unpack('<L', local_UDP.recv_bytes_io(struct.calcsize('<L'))[0])[0]
    print('image_len = ', image_len)
    stream.write(stream_connection.read(image_len))
    stream.seek(0)
    image = Image.open(stream)  # .transpose(Image.ROTATE_180)
    # image.show()
    print('Image is %dx%d' % image.size)
    print(image)

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
# server_socket = socket.socket()
# server_socket.bind(('192.168.1.189', 10100))
# server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
# connection = server_socket.accept()[0].makefile('rb')
# cnt = 0
# start_time = time.time()
# try:
#     while True:
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        # image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        # if not image_len:
        #     break
        # Construct a stream to hold the image data and read the image
        # data from the connection
        # image_stream = io.BytesIO()
        # image_stream.write(connection.read(image_len))
        # Rewind the stream, open it as an image with PIL and do some
        # processing on it
        # image_stream.seek(0)
        # image = Image.open(image_stream).transpose(Image.ROTATE_180)
        # print('Image is %dx%d' % image.size)
        # image.verify()
        # print('Image is verified')
        # image = image.rotate(180)
        # image = image.transpose(Image.ROTATE_180)
        # image.show()
        # print(1/(time.time()-startTime))
        # cnt = cnt + 1
        # image.close()

# finally:
#     connection.close()
#     server_socket.close()
#     print(cnt / (time.time() - start_time))
