import asyncio
import uuid
import json


def receive(ref, data, cb):
    ref.chunck["bufferStack"] = b"".join([ref.chunck["bufferStack"], data])

    re_check = True

    while re_check:
        re_check = False

        if ref.chunck["messageSize"] == 0 and len(ref.chunck["bufferStack"]) >= 4:
            ref.chunck["messageSize"] = int.from_bytes(ref.chunck["bufferStack"][0:4], byteorder='little')

        if len(ref.chunck["bufferStack"]) >= 8:
            ref.chunck["headerSize"] = int.from_bytes(ref.chunck["bufferStack"][4:8], byteorder='little')

        if 0 < ref.chunck["messageSize"] <= len(ref.chunck["bufferStack"]):
            buffer_header = ref.chunck["bufferStack"][8:ref.chunck["headerSize"] + 8]
            buffer_message = ref.chunck["bufferStack"][ref.chunck["headerSize"] + 8:ref.chunck["messageSize"]]

            ref.chunck["bufferStack"] = ref.chunck["bufferStack"][ref.chunck["messageSize"]:]

            ref.chunck["messageSize"] = 0
            ref.chunck["headerSize"] = 0

            cb(json.loads(buffer_header), buffer_message, ref)

            re_check = len(ref.chunck["bufferStack"]) > 0


def send(ref, header, message):
    if ref.transport.is_closing():
        raise Exception("Error sending message for a connection (" + str(ref.id) + ") closed ")

    str_header = json.dumps(header)

    b_header = str_header.encode('utf-8')
    b_message = message.encode('utf-8') if isinstance(message, str) else message

    int.from_bytes(ref.chunck["bufferStack"][0:4], byteorder='little')

    b_sz_data = (len(b_header) + len(b_message) + 8).to_bytes(4, byteorder='little')
    b_sz_head = (len(b_header)).to_bytes(4, byteorder='little')

    buff = b"".join([b_sz_data, b_sz_head, b_header, b_message])

    ref.transport.write(buff)


class HachiNIOServer(asyncio.Protocol):

    def __init__(self,
                 data,
                 client_connected=None,
                 client_close=None,
                 client_end=None,
                 client_timeout=None,
                 client_error=None,
                 ):

        self.fn_client_connected = client_connected
        self.fn_client_close = client_close
        self.fn_client_end = client_end
        self.fn_client_timeout = client_timeout
        self.fn_client_error = client_error
        self.fn_data = data
        self.id = uuid.uuid4()
        self.chunck = {
            "messageSize": 0,
            "headerSize": 0,
            "buffer": bytearray(),
            "bufferStack": bytearray()
        }

    def send(self, header, message):
        send(self, header, message)

    def connection_made(self, transport):
        # transport.write(self.message.encode())
        # print('Data sent: {!r}'.format(self.message))
        self.transport = transport

        if self.fn_client_connected is not None:
            self.fn_client_connected(self)

    def data_received(self, data):
        #print('Data received: {!r}'.format(data.decode()))
        #print(self)
        #print(data[0:2].hex())
        receive(self, data, self.fn_data)

    def connection_lost(self, exc):
        if self.fn_client_close is not None:
            self.fn_client_close(self)


class HachiNIOClient(HachiNIOServer):
    def __init__(self,
                 data,
                 client_connected=None,
                 client_close=None,
                 client_end=None,
                 client_timeout=None,
                 client_error=None,
                 ):

        self.fn_client_connected = client_connected
        self.fn_client_close = client_close
        self.fn_client_end = client_end
        self.fn_client_timeout = client_timeout
        self.fn_client_error = client_error
        self.fn_data = data
        self.id = uuid.uuid4()
        self.chunck = {
            "messageSize": 0,
            "headerSize": 0,
            "buffer": bytearray(),
            "bufferStack": bytearray()
        }