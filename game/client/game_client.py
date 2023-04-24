import json
import struct

from client.server_enum import Action
from client.server_enum import Result
from client.service import Service


class GameClient:
    def __init__(self) -> None:
        self.__service = Service()
        self.__service.connect("wgforge-srv.wargaming.net", 443)

    def __enter__(self):
        return GameClient

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.disconnect()

    def disconnect(self) -> None:
        self.__service.disconnect()

    def login(self, name: str, password: str = None, game_name: str = None,
              num_turns: int = None, num_players: int = None,
              is_observer: bool = None) -> dict:
        """
        User login
        :param name: player username
        :param password: player password
        :param game_name: define the game name to create or join if it already exists
        :param num_turns: number of game turns (if creating a game)
        :param num_players: number of game players (if creating a game)
        :param is_observer: define if joining as an observer
        :return: user dict
        """

        d: dict = {
            "name": name,
            "password": password,
            "game": game_name,
            "num_turns": num_turns,
            "num_players": num_players,
            "is_observer": is_observer
        }

        d = {k: v for k, v in d.items() if v is not None}

        self.__send_action(Action.LOGIN, d)
        return self.__receive_response()

    def logout(self) -> None:
        """
        User logout
        :param
        """
        self.__send_action(Action.LOGOUT)
        self.__receive_response()

    def get_map(self) -> dict:
        """
        Map request, return all map data in a dict
        :param
        :return: map dict
        """
        self.__send_action(Action.MAP)
        return self.__receive_response()

    def get_game_state(self) -> dict:
        """
        Game state request, returns the current game state
        :param
        :return: game state dict
        """
        self.__send_action(Action.GAME_STATE)
        return self.__receive_response()

    def get_game_actions(self) -> dict:
        """
        Game actions request, returns the actions that happened in the previous turn.
        Represent changes between turns.
        :return: game actions dict
        """
        self.__send_action(Action.GAME_ACTIONS)
        return self.__receive_response()

    def force_turn(self) -> int:
        """
        Needed to force the next turn of the game instead of waiting for the game's time slice.
        :param
        :return: 0 if turn has happened, -1 otherwise (TIMEOUT error)
        """
        try:
            self.__send_action(Action.TURN)
            self.__receive_response()
        except TimeoutError:
            return -1
        else:
            return 0

    def chat(self, msg):
        """
        Chat, just for fun and testing
        :param msg: message sent
        """
        self.__send_action(Action.CHAT, {"message": msg})
        self.__receive_response()

    def server_move(self, move_dict: dict) -> None:
        """
        Changes vehicle position
        """
        self.__send_action(Action.MOVE, move_dict)
        self.__receive_response()

    def server_shoot(self, shoot_dict: dict) -> None:
        """
        Shoot at a hex position
        """
        self.__send_action(Action.SHOOT, shoot_dict)
        self.__receive_response()

    @staticmethod
    def __unpack_helper(data) -> (Result, str):
        (resp_code, msg_len), data = struct.unpack("ii", data[:8]), data[8:]
        msg = data[:msg_len]
        return resp_code, msg

    def __send_action(self, act: Action, dct=None) -> None:
        if dct is None:
            dct = {}

        msg: bytes = b''
        if dct:
            msg = bytes(json.dumps(dct), 'utf-8')
        out: bytes = struct.pack('ii', act, len(msg)) + msg

        if not self.__service.send_data(out):
            raise ConnectionError(f"Error: Data was not sent correctly.")

    def __receive_response(self) -> dict:
        ret = self.__service.receive_data()
        resp_code, msg = self.__unpack_helper(ret)

        if resp_code == Result.TIMEOUT:
            dct: dict = json.loads(msg)
            raise TimeoutError(f"Error {resp_code}: {dct['error_message']}")
        elif resp_code != Result.OKEY:
            dct: dict = json.loads(msg)
            raise ConnectionError(f"Error {resp_code}: {dct['error_message']}")
        elif len(msg) > 0:
            return json.loads(msg)

        return {}
