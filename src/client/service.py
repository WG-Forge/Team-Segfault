import socket


class Service:
    def __init__(self) -> None:
        self.__buffer_size = 4096
        self.__socket: socket = socket.socket()

    def __enter__(self):
        return Service

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.disconnect()

    def connect(self, host: str, port: int) -> None:
        self.__socket.connect((host, port))

    def disconnect(self) -> None:
        self.__socket.close()

    def send_data(self, out: bytes) -> bool:
        ret: bool = self.__socket.send(out) > 0
        return ret

    def receive_data(self) -> bytes:
        msg: bytes = self.__socket.recv(self.__buffer_size)
        return msg
