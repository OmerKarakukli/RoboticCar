import io
import socket
import struct
from PIL import Image
from time import sleep
from Communication import UDP

# UDP_streamer = ('127.0.0.1', 10100)
UDP_streamer = ('192.168.1.162', 10101)
UDP_address = ('127.0.0.1', 10102)

UDP_local = UDP(UDP_address)
UDP_local.bind()

while True:
    UDP_local.sendto('getFrame', UDP_streamer)
    image_len = struct.unpack('<L', UDP_local.recv_bytes(bytes_num=struct.calcsize('<L'))[0])[0]
    image_stream = io.BytesIO()
    image_stream.write(UDP_local.recv_bytes(bytes_num=image_len))
    image_stream.seek(0)
    image = Image.open(image_stream).transpose(Image.ROTATE_180)
    print('Image is %dx%d' % image.size)


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
