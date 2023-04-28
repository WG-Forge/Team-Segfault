from threading import Thread, Event
from typing import Dict

from client.game_client import GameClient
from client.server_enum import Action
from constants import HEX_RADIUS_Y, HEX_RADIUS_X
from map.map import Map
from player.bot_player1 import BotPlayer
from player.player1 import Player


class Game(Thread):
    def __init__(self, game_name: str = None, num_turns: int = None, max_players: int = 1, index: int = 0,
                 player_name: str = None, password: str = None, is_observer: bool = None) -> None:
        super().__init__()

        self.__game_map = None
        self.__game_name: str = game_name

        # create an active event
        self.over: Event = Event()

        self.__num_turns: int = num_turns
        self.__max_players: int = max_players
        self.__winner = None
        self.__started: bool = False

        self.__current_turn: [] = [-1]
        self.__current_player = None

        self.__current_player_idx: int = -1

        self.__game_client = GameClient()

        self.__player = self.__add_player(player_name, password, is_observer, index)

    def __str__(self):
        out: str = ""
        out += str.format(f'Game name: {self.__game_name}, '
                          f'number of players: {self.__max_players}, '
                          f'number of turns: {self.__num_turns}.')
        return str(self.__player)

    def __add_player(self, name: str, password: str = None, is_observer: bool = None, index: int = 0) -> Player:
        """
        Will connect the player if game has started.
        If the game is full, player will be connected as an observer.
        """

        player = BotPlayer(name=name, password=password, is_observer=is_observer, player_index=index, over=self.over)

        self.__connect_player(player)
        return player

    def __connect_player(self, player: Player) -> None:
        game_client: GameClient = GameClient()
        user_info: Dict = game_client.login(player.name, player.password,
                                            self.__game_name, self.__num_turns,
                                            self.__max_players, player.is_observer)

        player.add_to_game(user_info)

    # def start_menu(self) -> None:
    #     try:
    #         # initialize and start the pygame display manager from the main thread
    #         DisplayManager(self).run()
    #     finally:
    #         # in case the main thread is interrupted
    #         self.over.set()

    def run(self) -> None:
        self.__init_game_state()

        while not self.over.is_set():
            # start the next turn
            self.__start_next_turn()

            if self.__current_player_idx == self.__player.idx:
                # Reset current player attacks
                self.__player.register_turn()
                self.__player.make_turn_plays()
                for action_id, action_dict in self.__player.turn_actions:
                    if action_id == Action.SHOOT:
                        self.__game_client.server_shoot(action_dict)
                    else:
                        self.__game_client.server_move(action_dict)

            self.__game_client.force_turn()

        self.__end_game()

    def __wait_for_full_lobby(self) -> Dict | None:
        """ Return game state if the lobby is full, else None if the game was interrupted """
        game_state: Dict = self.__game_client.get_game_state()

        while not self.over.is_set() and game_state["num_players"] != len(game_state["players"]):
            # wait for all the players to join
            game_state = self.__game_client.get_game_state()

        return game_state

    def __init_game_state(self) -> None:
        # Add the queued local players to the game

        game_state: Dict = self.__wait_for_full_lobby()

        if not game_state:
            # the game was interrupted
            return

        client_map: Dict = self.__game_client.get_map()
        HEX_RADIUS_X[0] //= (client_map['size'] - 1) * 2 * 2
        HEX_RADIUS_Y[0] //= (client_map['size'] - 1) * 2 * 2

        # initialize the game map (now adds tanks to players & game_map too)
        self.__game_map = Map(client_map, game_state, active_players={self.__player.idx: self.__player},
                              current_turn=self.__current_turn)

        self.__num_turns = game_state["num_turns"]
        self.__max_players = game_state["num_players"]

        # pass Map reference to players
        self.__player.add_map(self.__game_map)

        # output the game info to console
        print(self)

    def __start_next_turn(self) -> None:

        # start the next turn
        game_state = self.__game_client.get_game_state()

        self.__current_turn[0] = game_state["current_turn"]
        self.__current_player_idx = game_state["current_player_idx"]

        print(f"Current turn: {self.__current_turn[0]}, "
              f"current player: {self.__current_player.name}")

        self.__game_map.update_turn(game_state)

        if game_state["winner"] or self.__current_turn[0] == self.__num_turns:
            self.__winner = game_state["winner"]
            self.over.set()

    def __end_game(self):
        if self.__winner is None:
            print('The game is a draw.')
        elif self.__winner == self.__player.name:
            print(f'Congrats {self.__player.name}, you won!')
        else:
            print(f'You lost ):. The winner is {self.__winner}')

        self.__finalize()

    def __finalize(self):
        # manage your own connection
        self.__game_client.logout()
        self.__game_client.disconnect()
