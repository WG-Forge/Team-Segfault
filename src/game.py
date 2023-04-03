from src.client.game_client import GameClient
from src.entity.tank import Tank
from src.map.game_map import GameMap
from src.player.bot_player import BotPlayer
from src.player.human_player import HumanPlayer
from src.player.player import Player


class Game:
    def __init__(self, game_name: str = None, num_turns: int = None, num_players: int = 1) -> None:
        super().__init__()
        self.__game_map: GameMap
        self.__game_name: str = game_name

        self.__active: bool = False
        self.__num_turns: int = num_turns
        self.__max_players: int = num_players
        self.__num_players: int = 0
        self.__winner = None

        self.__players_queue: [Player] = []
        self.__current_turn = None
        self.__current_player = None
        self.__current_client = None

        self.__game_clients: dict[Player, GameClient] = {}
        self.__active_players: dict[int, Player] = {}
        self.__observers: dict[int, Player] = {}

    def __str__(self):
        out: str = ""
        out += str.format(f'Game name: {self.__game_name}, '
                          f'number of players: {self.__max_players}, '
                          f'number of turns: {self.__num_turns}.')

        for player in self.__active_players.values():
            out += "\n" + str(player)

        for player in self.__observers.values():
            out += "\n" + str(player)

        return out

    def add_player(self, name: str, password: str = None, is_bot: bool = False, is_observer: bool = False) -> None:
        """
        Will connect as a player if the game has started and the game is not full,
        or as an observer if the game is full, and allows observers.
        """
        player: Player
        if is_bot:
            player = self.__create_bot_player(name, password, is_observer)
        else:
            player = self.__create_human_player(name, password, is_observer)

        if self.__active:
            self.__connect_player(player)
        else:
            self.__players_queue.append(player)

    def start_game(self) -> None:
        if not self.__players_queue:
            raise RuntimeError("Can't start game with no players!")

        # Add the queued players to the game or as an observer
        for player in self.__players_queue:
            self.__connect_player(player)

        self.__active = True

        self.run()

    def run(self) -> None:
        self.__init_game_state()

        while self.__active:
            self.__game_map.draw_map()

            if self.__current_player.idx in self.__active_players:
                move_list, shoot_list = self.__current_player.play_move()

                for move in move_list:
                    self.__current_client.move(move)
                for shoot in shoot_list:
                    self.__current_client.shoot(shoot)

            self.__current_client.force_turn()
            self.__start_next_turn()

        self.__end_game()

    def __connect_player(self, player: Player) -> None:
        self.__game_clients[player] = GameClient()
        user_info: dict = self.__game_clients[player].login(player.name, player.password,
                                                            self.__game_name, self.__num_turns,
                                                            self.__max_players, player.is_observer)

        player.add_to_game(user_info)

        if not player.is_observer:
            self.__active_players[player.idx] = player

            # first active player added is the current client-server connection
            if not self.__current_client:
                self.__current_client = self.__game_clients[player]
        else:
            self.__observers[player.idx] = player

    def __init_game_state(self) -> None:
        game_map: dict = self.__current_client.get_map()
        game_state: dict = self.__current_client.get_game_state()

        # initialize the game map
        self.__game_map = GameMap(game_map)
        self.__num_turns = game_state["num_turns"]
        self.__max_players = game_state["num_players"]

        # add tanks to players
        for vehicle_id, vehicle_info in game_state["vehicles"].items():
            tank = Tank(int(vehicle_id), vehicle_info)
            self.__active_players[vehicle_info["player_id"]].add_tank(tank)

        # pass GameMap reference to players
        for player in self.__active_players.values():
            player.add_map(self.__game_map)

        # output the game info to console
        print(self)

        self.__start_next_turn(game_state)

    def __start_next_turn(self, game_state: dict = None) -> None:
        # start the next turn
        if not game_state:
            game_state = self.__current_client.get_game_state()

        self.__current_turn = game_state["current_turn"]
        current_player_idx: int = game_state["current_player_idx"]
        self.__current_player = self.__active_players[current_player_idx]
        self.__current_client = self.__game_clients[self.__current_player]

        print(f"Current turn: {self.__current_turn}, "
              f"current player: {self.__current_player.name}")

        self.__game_map.update(game_state)

        if game_state["winner"] or self.__current_turn == self.__num_turns:
            self.__winner = game_state["winner"]
            self.__active = False
            return

    def __end_game(self):
        if self.__winner:
            winner_name = self.__active_players[self.__winner].name
            print(f'The winner is: {winner_name}.')
        else:
            print('The game is a draw.')

        for client in self.__game_clients.values():
            client.logout()

    @staticmethod
    def __create_human_player(name: str, password: str = None, is_observer: bool = None) -> Player:
        return HumanPlayer(name, password, is_observer)

    @staticmethod
    def __create_bot_player(name: str, password: str = None, is_observer: bool = None) -> Player:
        return BotPlayer(name, password, is_observer)
