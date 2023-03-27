import json
import struct

from server_enum import Action
from service import Service


class GameClient:
    def __init__(self) -> None:
        self.__service = Service()
        self.__service.connect("wgforge-srv.wargaming.net", 443)

    def __del__(self) -> None:
        self.__service.disconnect()

    def login(self, name: str) -> int:
        d: dict = {
            "name": name
        }

        msg: bytes = bytes(json.dumps(d), 'utf-8')
        out: bytes = struct.pack('ii', Action.LOGIN, len(msg)) + msg

        self.__service.send_data(out)
        ret = self.__service.receive_data()
        print(ret)
        return 0


if __name__ == "__main__":
    c = GameClient()
    c.login("MegatronJeremy")
