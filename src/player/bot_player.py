from abc import ABC
from threading import Semaphore

from src.entity.tanks.tank import Tank
from src.player.player import Player
from src.client.server_enum import Action


class BotPlayer(Player, ABC):
    def __init__(self, name: str, password: str, is_observer: bool, turn_played_sem: Semaphore,
                 current_player: list[1], player_index: int):
        super().__init__(name, password, is_observer, turn_played_sem, current_player, player_index)

    def _make_turn_plays(self) -> None:

        for tank in self._tanks:
            # print(tank.get_id(), tank.get_coord())
            # print(self._map.closest_enemy(tank).get_coord())
            # self.__move_to(tank, self._map.closest_enemy(tank).get_coord())
            closest_base_coord = self._map.closest_base(tank.get_coord())
            if closest_base_coord is not None:
                self.__move_to(tank, closest_base_coord)

    def __move_to_shoot(self, who: Tank, what: Tank):
        what_coord = what.get_coord()
        if self.is_in_range(who, what_coord):
            print('shot')
            self.__take_action(who.get_id(), what_coord, Action.SHOOT)
        else:
            print('move')
            self.__move_to(who, what_coord)

    def __move_to(self, tank: Tank, where: tuple):
        tank_speed = tank.get_speed()
        tank_id = tank.get_id()
        next_best = self._game_map.next_best(tank.get_coord(), where, tank_speed, tank_id)
        print(next_best)
        if next_best is not None:
            self.__take_action(tank_id, next_best, Action.MOVE)


    def __take_action(self, tank_id: int, action_coord: tuple, action: int) -> None:
        x, y, z = action_coord
        move_dict = {"vehicle_id": tank_id, "target": {"x": x, "y": y, "z": z}}
        self._game_client.move(move_dict)
        self._game_map.update({"actions": [{"action_type": action, "data": move_dict}]})

    def is_in_range(self, tank: Tank, target_coord: tuple) -> bool:
        return target_coord in tank.get_possible_shots()

