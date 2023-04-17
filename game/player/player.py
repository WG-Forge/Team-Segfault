from abc import abstractmethod
from dataclasses import dataclass
from threading import Thread, Semaphore, Event

from client.game_client import GameClient
from entity.tanks.tank import Tank
from map.map import Map


@dataclass
class Player(Thread):
    __type_order = ('spg', 'light_tank', 'heavy_tank', 'medium_tank', 'at_spg')
    __possible_colours = ((224, 206, 70), (70, 191, 224), (224, 137, 70))  # yellow, blue, orange

    def __init__(self, name: str, password: str, is_observer: bool,
                 turn_played_sem: Semaphore, current_player: list[1], player_index: int, active: Event):
        super().__init__()

        self.idx: int = -1
        self.name = name
        self.password = password
        self.is_observer: bool = is_observer

        self.next_turn_sem = Semaphore(0)
        self.__turn_played_sem = turn_played_sem
        self.__active = active
        self.__current_player = current_player

        self._game_client = None
        self._map = None

        self._damage_points = 0
        self._capture_points = 0
        self._tanks: list[Tank] = []
        self._player_index = player_index
        self.__player_colour = Player.__possible_colours[player_index]
        self.__has_shot = []  # Holds a list of enemies this player has shot last turn

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
        while self.__active.is_set():
            # wait for condition
            self.next_turn_sem.acquire()

            try:
                # check if the game ended
                if not self.__active.is_set():
                    break

                # play your move if you are the current player
                if self.__current_player[0] == self.idx:
                    # time.sleep(1)  # comment/uncomment this for a turn delay effect
                    self._make_turn_plays()

                # force next turn
                self._game_client.force_turn()
            except ConnectionError or TimeoutError as err:
                print(err)
            finally:
                # notify condition
                self.__turn_played_sem.release()

        # finalization
        self.__logout()

    def get_color(self) -> str:
        return self.__player_colour

    def get_index(self):
        return self._player_index

    def get_tanks(self):
        return self._tanks

    def has_shot(self, player_index: int) -> bool:
        return player_index in self.__has_shot

    def register_shot(self, enemy_index: int) -> None:
        self.__has_shot.append(enemy_index)

    def register_turn(self) -> None:  # Call this for every player at the beginning of every turn
        self.__has_shot = []

    @abstractmethod
    def _make_turn_plays(self) -> None:
        pass

    def __logout(self):
        self._game_client.logout()
        self._game_client.disconnect()
