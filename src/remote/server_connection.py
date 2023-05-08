from socket import socket

from src.constants import DEFAULT_BUFFER_SIZE


class ServerConnection:
    def __init__(self) -> None:
        self.__socket: socket = socket()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.disconnect()

    def connect(self, host: str, port: int) -> None:
        self.__socket.connect((host, port))

    def disconnect(self) -> None:
        self.__socket.close()

    def send_data(self, out: bytes) -> bool:
        ret: bool = self.__socket.send(out) > 0
        return ret

    def receive_data(self, message_size: int, buffer_size: int = DEFAULT_BUFFER_SIZE) -> bytes:
        received: int = 0
        msg: bytes = bytes()
        while received < message_size:
            packet: bytes = self.__socket.recv(buffer_size)
            received += len(packet)
            msg += packet

        return msg
