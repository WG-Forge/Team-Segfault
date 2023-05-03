from constants import BASE_COLOR
from entities.entity_enum import Entities
from entities.map_features.feature import Feature


class Base(Feature):
    __rounds_to_cap = 1

    def __init__(self, coord: tuple):
        super().__init__(Entities.BASE, coord, BASE_COLOR)
        self.__rounds_in_base_by_player_index = [0 for _ in range(3)]

    def player_in_base_return_capture_points(self, player_index: int) -> int:
        self.__rounds_in_base_by_player_index[player_index] += 1
        if self.__rounds_in_base_by_player_index[player_index] > self.__rounds_to_cap:
            self.__reset_other_players_cap(self.__rounds_in_base_by_player_index[player_index], player_index)
            return 1
        return 0

    def __reset_other_players_cap(self, rounds: int, index: int) -> None:
        self.__rounds_in_base_by_player_index = [0 for _ in range(3)]
        self.__rounds_in_base_by_player_index[index] = rounds

