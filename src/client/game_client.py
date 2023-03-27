import json
import struct

from server_enum import Action
from server_enum import Result
from service import Service


def result_handler(result: Result) -> int:
    """
    Prints an error message if server response says action was invalid
    :param result: the server code
    :return: 0 if valid, -1 otherwise
    """
    if result == Result.OKEY:
        return 0

    print("Error: ", result.name)
    return -1


def unpack_helper(data) -> (Result, str):
    (resp_code, msg_len), data = struct.unpack("ii", data[:8]), data[8:]
    msg = data[:msg_len]
    return resp_code, msg


class GameClient:
    def __init__(self) -> None:
        self.__service = Service()
        self.__service.connect("wgforge-srv.wargaming.net", 443)

    def __del__(self) -> None:
        self.__service.disconnect()

    def login(self, name: str) -> int:
        """
        User login
        :param name: username
        :return: user_id if valid, -1 otherwise
        """
        d: dict = {
            "name": name
        }

        ret = self.__send_and_receive_dict(d, Action.LOGIN)

        print(ret)

        if ret is None:
            return -1

        return ret["idx"]

    def __send_and_receive_dict(self, d: dict, a: Action) -> dict:
        msg: bytes = bytes(json.dumps(d), 'utf-8')
        out: bytes = struct.pack('ii', a, len(msg)) + msg

        self.__service.send_data(out)
        ret = self.__service.receive_data()

        resp_code, msg = unpack_helper(ret)

        if result_handler(resp_code) < 0:
            return {}
        else:
            return json.loads(msg)


if __name__ == "__main__":
    c = GameClient()
    id = c.login("MegatronJeremy")
    print(id)
