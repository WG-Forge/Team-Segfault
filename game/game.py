from threading import Thread, Event

from game_map.map import Map
from players.player import Player
from players.player_manager import PlayerManager
from remote.game_client import GameClient


class Game(Thread):
    def __init__(self, game_name: str | None = None, num_turns: int | None = None,
                 max_players: int = 1) -> None:
        super().__init__()

        self.game_map: Map | None = None
        self.__game_name: str | None = game_name

        # create an active event
        self.over: Event = Event()

        self.__num_turns: int | None = num_turns
        self.__max_players: int = max_players
        self.__winner: int | None = None
        self.__winner_index: int | None = None
        self.__started: bool = False
        self.__game_is_draw: bool = False

        self.__connection_error: ConnectionError | None = None

        self.__current_turn: list[int] = [-1]
        self.__current_player: Player | None = None

        # Observer connection that is used for collecting data
        self.__shadow_client = GameClient()
        self.__active_players: dict[int, Player] = {}
        self.__current_player_idx: list[int] = [-1]
        self.__player_manager: PlayerManager = PlayerManager(self, self.__shadow_client)

    def __str__(self) -> str:
        out: str = ""
        out += str.format(f'Game: {self.__game_name}, '
                          f'number of players: {self.__max_players}, '
                          f'number of turns: {self.__num_turns}.')

        for player in self.__active_players.values():
            out += "\n" + str(player)

        return out

    """     GETTERS     """

    @property
    def max_players(self) -> int:
        return self.__max_players

    @property
    def current_player_idx(self) -> list[int]:
        return self.__current_player_idx

    @property
    def started(self) -> bool:
        return self.__started

    @property
    def game_name(self) -> str | None:
        return self.__game_name

    @property
    def num_turns(self) -> int | None:
        return self.__num_turns

    @property
    def active_players(self) -> dict[int, Player]:
        return self.__active_players

    @property
    def current_player(self) -> Player:
        return self.__current_player

    @property
    def connection_error(self) -> ConnectionError:
        return self.__connection_error

    @property
    def game_is_draw(self) -> bool:
        return self.__game_is_draw

    """     GAME LOGIC      """

    def run(self) -> None:
        try:
            self.__init_game_state()

            while not self.over.is_set():
                # start the next turn
                self.__start_next_turn()

                # handshake with players
                self.__player_manager.handle_player_turns()

        except ConnectionError as err:
            # a connection error happened
            self.over.set()
            self.__connection_error = err

        finally:
            self.__end_game()

    def add_local_player(self, name: str, password: str | None = None, is_observer: bool | None = None) -> None:
        self.__player_manager.add_local_player(name, password, is_observer)

    def get_winner_index(self) -> int | None:
        # wait for game end event
        self.over.wait()
        return self.__winner_index

    def __wait_for_full_lobby(self) -> dict | None:
        """ Return game state if the lobby is full, else None if the game was interrupted """
        game_state: dict = self.__shadow_client.get_game_state()

        while not self.over.is_set() and game_state["num_players"] != len(game_state["players"]):
            # wait for all the players to join
            game_state = self.__shadow_client.get_game_state()

        if self.over.is_set():
            return None

        return game_state

    def __init_game_state(self) -> None:
        self.__started = True

        # Login to the shadow client
        self.__player_manager.login()

        # Add the queued local players to the game
        self.__player_manager.connect_queued_players()

        game_state: dict | None = self.__wait_for_full_lobby()

        if not game_state:
            # the game was interrupted
            return

        self.__num_turns = game_state["num_turns"]
        self.__max_players = game_state["num_players"]

        # add all remote players and observers
        self.__player_manager.add_remote_players(game_state["players"])
        self.__player_manager.add_remote_players(game_state["observers"])

        # start all player instances
        self.__player_manager.start_players()

        client_map: dict = self.__shadow_client.get_map()

        # initialize the game map (now adds tanks to players & game_map too)
        self.game_map = Map(client_map, game_state, self.__active_players, self.__current_turn)

        # pass Map reference to players
        for player in self.__active_players.values():
            player.add_map(self.game_map)

        # output the game info to console
        print(self)

    def __start_next_turn(self) -> None:
        # start the next turn
        game_state = self.__shadow_client.get_game_state()

        self.__current_turn[0] = game_state["current_turn"]
        self.__current_player_idx[0] = game_state["current_player_idx"]
        self.__current_player = self.__active_players[self.__current_player_idx[0]]

        # Reset current player attacks
        self.__current_player.register_turn()

        print()
        print(f"Current turn: {self.__current_turn[0]}, "
              f"current player: {self.__current_player.player_name}")

        if self.game_map:
            self.game_map.update_turn(game_state)

        if game_state["finished"]:
            self.__winner = game_state["winner"]
            if self.__winner is None:
                self.__game_is_draw = True
            self.over.set()

    def __end_game(self) -> None:
        # Notify all players the game has ended
        self.__player_manager.notify_all_players()

        if self.__connection_error:
            # TODO just print it in the console for now
            print(self.__connection_error)
        elif self.__winner or self.__game_is_draw:
            if self.__game_is_draw:
                # TODO just print it in the console for now
                print('The game is a draw')
            else:
                winner = self.__active_players[self.__winner]
                self.__winner_index = winner.index
                print(f'The winner is: {winner.player_name}.')
        else:
            print("The game was interrupted")

        self.__player_manager.logout()
