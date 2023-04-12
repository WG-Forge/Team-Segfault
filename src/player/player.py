from abc import abstractmethod
from dataclasses import dataclass
from threading import Thread, Semaphore

from map.map import Map
from src.client.game_client import GameClient
from src.entity.tanks.tank import Tank


@dataclass
class Player(Thread):
    __type_order = ('spg', 'light_tank', 'heavy_tank', 'medium_tank', 'at_spg')
    __possible_colours = ('blue', 'black', 'green')

    def __init__(self, name: str, password: str, is_observer: bool,
                 turn_played_sem: Semaphore, current_player: list[1], player_index: int):
        super().__init__(daemon=True)
        self.idx: int = -1
        self.name = name
        self.password = password
        self.is_observer: bool = is_observer
        self.next_turn_sem = Semaphore(0)
        self._damage_points = 0
        self._capture_points = 0
        self._tanks: list[Tank] = []
        self._map = None
        self._game_client = None
        self.__turn_played_sem = turn_played_sem
        self.__current_player = current_player
        self.__player_colour = Player.__possible_colours[player_index]
        self._player_index = player_index
        self.__attackers = [[], []]  # Holds two lists of attacker indexes -> [[prev turns'], [this turns']]

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        out = str.format(f'Player {self.idx}: {self.name}')
        if self.is_observer:
            out += ', observer'

        return out

    def add_to_game(self, player_info: dict, game_client: GameClient):
        self.idx: int = player_info["idx"]
        self.is_observer: bool = player_info["is_observer"]
        self._damage_points: int = 0
        self._capture_points: int = 0
        self._game_client: GameClient = game_client

    def add_tank(self, new_tank: Tank) -> None:
        # Adds the tank in order of who gets priority movement
        new_tank_priority = Player.__type_order.index(new_tank.get_type())
        for i, old_tank in enumerate(self._tanks):
            old_tank_priority = Player.__type_order.index(old_tank.get_type())
            if new_tank_priority <= old_tank_priority:
                self._tanks.insert(i, new_tank)
                return
        self._tanks.append(new_tank)

    def add_map(self, game_map: Map):
        self._map = game_map

    def run(self) -> None:
        while True:
            # wait for condition
            self.next_turn_sem.acquire()

            try:
                # play your move if you are the current player
                if self.__current_player[0] == self.idx:
                    self._make_turn_plays()

                # force next turn
                self._game_client.force_turn()
            except ConnectionError or TimeoutError as err:
                print(err)
            finally:
                # notify condition
                self.__turn_played_sem.release()

    @abstractmethod
    def _make_turn_plays(self) -> None:
        pass

    def get_color(self) -> str:
        return self.__player_colour

    def get_index(self):
        return self._player_index

    def get_tanks(self):
        return self._tanks

    def was_attacked_by(self, attacker_index: int) -> bool:
        # True if this player was attacked by 'attacker_index' in the previous turn
        return attacker_index in self.__attackers[0]

    def register_attacker(self, attacker_index: int) -> None:
        # Appends attacker to this turns' attackers which will become last turns' attackers next turn
        if attacker_index not in self.__attackers[1]:
            self.__attackers[1].append(attacker_index)

    def register_new_turn(self) -> None:  # Call this for every player at the beginning of every turn
        self.__attackers.pop(0)  # Delete list of attackers of two turns ago
        self.__attackers.append([])  # Append a new empty list to register this turns' attackers
