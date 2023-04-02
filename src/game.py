from threading import Thread

from src.client.game_client import GameClient
from src.client.server_enum import Action
from src.entity.tank import Tank
from src.map.game_map import GameMap
from src.player.bot_player import BotPlayer
from src.player.human_player import HumanPlayer
from src.player.player import Player


class Game(Thread):
    def __init__(self, game_name: str = None) -> None:
        super().__init__()
        self.__current_turn = None
        self.__game_map: GameMap
        self.__game_name: str = game_name
        self.__active: bool = False
        self.__game_client: GameClient = GameClient()
        self.__players_queue: [Player] = []
        self.__active_players: dict[int, Player] = {}
        self.__num_turns: int = 0
        self.__current_player: int = -1

    def add_player(self, name: str, password: str = None, is_bot: bool = False,
                   is_observer: bool = None) -> None:
        """
        Will connect player if game has started
        :param name:
        :param password:
        :param is_bot:
        :param is_observer:
        :return:
        """
        player: Player
        if is_bot:
            player = self.__create_bot_player(name, password, is_observer)
        else:
            player = self.__create_human_player(name, password, is_observer)
        self.__players_queue.append(player)

        if self.__active:
            self.__connect_player(player)

    def start_game(self, num_turns: int = None, num_players: int = None) -> None:
        if not self.__players_queue:
            raise RuntimeError("Can't start game with no players!")

        player_one: Player = self.__players_queue.pop(0)
        player_one_info: dict = self.__game_client.login(player_one.name, player_one.password,
                                                         self.__game_name, num_turns, num_players)
        player_one.add_to_game(player_one_info)
        self.__active_players[player_one.id] = player_one
        self.__active = True

        players_in_queue = len(self.__players_queue)
        for i in range(min(players_in_queue, 2)):
            next_player = self.__players_queue.pop(0)
            self.__connect_player(next_player)
            self.__active_players[next_player.id] = next_player

        self.start()

    def action_no_response(self, action: Action) -> None:
        pass

    def action_response(self, msg: dict) -> dict:
        pass

    def end_game(self) -> None:
        self.__game_client.logout()

    def run(self) -> None:
        self.__init_game_state()

        while self.__active:
            self.__game_map.draw_map()

            if self.__current_player in self.__active_players:
                move_dict, shoot_dict = self.__active_players[self.__current_player].play_move()
                if move_dict:
                    self.__game_client.move(move_dict)
                if shoot_dict:
                    self.__game_client.shoot(shoot_dict)

            self.__game_client.force_turn()
            self.__start_next_turn()

    def __connect_player(self, player: Player) -> None:
        if not self.__active:
            raise RuntimeError("Can't join game that has not started!")

        user_info: dict = self.__game_client.login(player.name, player.password, self.__game_name)
        player.add_to_game(user_info)

    def __init_game_state(self) -> None:
        game_map: dict = self.__game_client.get_map()
        game_state: dict = self.__game_client.get_game_state()

        self.__num_turns = game_state["num_turns"]
        self.__game_map = GameMap(game_map)
        self.__game_map.update(game_state)

        # add tanks to players
        for vehicle_id, vehicle_info in game_state["vehicles"].items():
            tank = Tank(int(vehicle_id), vehicle_info)
            self.__active_players[vehicle_info["player_id"]].add_tank(tank)

        # pass GameMap reference to players
        for _, player in self.__active_players.items():
            player.add_map(self.__game_map)

    def __start_next_turn(self) -> None:
        game_state: dict = self.__game_client.get_game_state()
        current_turn: int = game_state["current_turn"]
        print(f"Current turn: {current_turn}")

        self.__current_player = game_state["current_player_idx"]
        self.__game_map.update(game_state)
        if current_turn == self.__num_turns:
            self.__active = False

    @staticmethod
    def __create_human_player(name: str, password: str = None, is_observer: bool = None) -> Player:
        return HumanPlayer(name, password, is_observer)

    @staticmethod
    def __create_bot_player(name: str, password: str = None, is_observer: bool = None) -> Player:
        return BotPlayer(name, password, is_observer)
