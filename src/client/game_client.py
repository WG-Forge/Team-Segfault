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

        ret = self.__send_and_receive_data(d, Action.LOGIN)

        if ret is None:
            return -1

        return ret["idx"]

    def logout(self) -> int:
        """
        User logout
        :param
        :return: 0 if valid, -1 otherwise
        """

        ret = self.__send_and_receive_data({}, Action.LOGOUT, True)

        if ret is None:
            return -1

        return 0

    def __send_and_receive_data(self, d: dict, a: Action, empty: bool = False) -> dict:
        msg: bytes = b''
        if not empty:
            msg = bytes(json.dumps(d), 'utf-8')
        out: bytes = struct.pack('ii', a, len(msg)) + msg

        self.__service.send_data(out)
        ret = self.__service.receive_data()

        resp_code, msg = unpack_helper(ret)

        if resp_code != Result.OKEY:
            d: dict = json.loads(msg)
            raise ConnectionError(f"Error {resp_code}: {d['error_message']}")
        elif len(msg) > 0:
            return json.loads(msg)

        return {}


if __name__ == "__main__":
    c = GameClient()
    r = c.login("MegatronJeremy")
    print(r)
    r = c.logout()
