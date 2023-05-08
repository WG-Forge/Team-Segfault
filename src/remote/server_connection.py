import socket


class ServerConnection:
    def __init__(self) -> None:
        self.__socket: socket = socket.socket()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.disconnect()

    def connect(self, host: str, port: int) -> None:
        self.__socket.connect((host, port))

    def disconnect(self) -> None:
        self.__socket.close()

    def send_data(self, out: bytes) -> bool:
        try:
            self.__socket.sendall(out)
            return True
        except socket.error:
            return False

    def receive_data(self, message_size: int) -> bytes:
        buffer: bytearray = bytearray(message_size)
        position: int = 0
        while position < message_size:
            cr = self.__socket.recv_into(memoryview(buffer)[position:])
            if cr == 0:
                raise EOFError  # Nothing was received!
            position += cr

        return buffer
