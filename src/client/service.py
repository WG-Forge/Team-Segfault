import socket


class Service:
    def __init__(self) -> None:
        self.__buffer_size = 4096
        self.__socket: socket = socket.socket()

    def __del__(self) -> None:
        self.disconnect()

    def connect(self, host: str, port: int) -> None:
        self.__socket.connect((host, port))

    def send_data(self, out: bytes) -> bool:
        ret: bool = self.__socket.send(out) > 0
        return ret

    def receive_data(self) -> bytes:
        msg: bytes = self.__socket.recv(self.__buffer_size)
        return msg

    def disconnect(self) -> None:
        self.__socket.close()

    def function(self) -> None:
        pass
