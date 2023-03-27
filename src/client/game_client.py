import json
import struct

from server_enum import Action
from server_enum import Result
from service import Service


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

    def login(self, name: str) -> dict:
        """
        User login
        :param name: username
        :return: user dict
        """

        return self.__send_and_receive_data({"name": name}, Action.LOGIN)

    def logout(self) -> None:
        """
        User logout
        :param
        """
        self.__send_and_receive_data({}, Action.LOGOUT)

    def get_map(self) -> dict:
        """
        Map request, return all map data in a dict
        :param
        :return: map dict
        """
        return self.__send_and_receive_data({}, Action.MAP)

    def get_game_state(self) -> dict:
        """
        Game state request, returns the current game state
        :param
        :return: game state dict
        """
        return self.__send_and_receive_data({}, Action.GAME_STATE)

    def get_game_actions(self) -> dict:
        """
        Game actions request, returns the actions that happened in the previous turn.
        Represents changes between turns.
        :param
        :return: game actions dict
        """
        return self.__send_and_receive_data({}, Action.GAME_ACTIONS)

    def force_turn(self) -> int:
        """
        Needed to force the next turn of the game instead of waiting for the game's time slice.
        :param
        :return: 0 if turn has happened, -1 otherwise (TIMEOUT error)
        """
        try:
            self.__send_and_receive_data({}, Action.TURN)
        except TimeoutError:
            return -1
        else:
            return 0

    def chat(self, msg):
        """
        Chat, just for fun and testing
        :param msg: message sent
        """
        self.__send_and_receive_data({"message": msg}, Action.CHAT)

    def move(self, vehicle_id: int, x: int, y: int, z: int) -> None:
        """
        Changes vehicle position
        :param vehicle_id: id of vehicle
        :param x: coordinate x
        :param y: coordinate y
        :param z: coordinate z
        """
        dct: dict = {
            "vehicle_id": vehicle_id,
            "target": {
                "x": x,
                "y": y,
                "z": z
            }
        }
        self.__send_and_receive_data(dct, Action.MOVE)

    def shoot(self, vehicle_id: int, x: int, y: int, z: int) -> None:
        """
        Shoot to target position
        :param vehicle_id: id of vehicle
        :param x: coordinate x
        :param y: coordinate y
        :param z: coordinate z
        """
        dct: dict = {
            "vehicle_id": vehicle_id,
            "target": {
                "x": x,
                "y": y,
                "z": z
            }
        }
        self.__send_and_receive_data(dct, Action.SHOOT)

    def __send_and_receive_data(self, dct: dict, act: Action) -> dict:
        msg: bytes = b''
        if dct:
            msg = bytes(json.dumps(dct), 'utf-8')
        out: bytes = struct.pack('ii', act, len(msg)) + msg

        self.__service.send_data(out)
        ret = self.__service.receive_data()

        resp_code, msg = unpack_helper(ret)

        if resp_code == Result.TIMEOUT:
            dct: dict = json.loads(msg)
            raise TimeoutError(f"Error {resp_code}: {dct['error_message']}")
        elif resp_code != Result.OKEY:
            dct: dict = json.loads(msg)
            raise ConnectionError(f"Error {resp_code}: {dct['error_message']}")
        elif len(msg) > 0:
            return json.loads(msg)

        return {}


if __name__ == "__main__":
    c = GameClient()
    r = c.login("MegatronJeremy")
    idx: int = r["idx"]
    print(c.get_map())
    print(c.get_game_actions())
    print(c.get_game_state())
    c.move(1, -8, -2, 10)
    c.force_turn()
    print(c.get_game_actions())
    c.logout()
