from abc import ABC
from threading import Semaphore

from entity.tanks.tank import Tank
from player.player import Player


class BotPlayer(Player, ABC):
    def __init__(self, name: str, password: str, is_observer: bool, turn_played_sem: Semaphore,
                 current_player: list[1], player_index: int):
        super().__init__(name, password, is_observer, turn_played_sem, current_player, player_index)

    def _make_turn_plays(self) -> None:
        # Types: spg, light_tank, heavy_tank, medium_tank, at_spg

        # multiplayer game:
        for tank in self._tanks:
            if tank.get_type() != 'at_spg':
                self.__move_to_shoot_closest_enemy(tank)
            # if tank.get_type() == 'light_tank':
            #     self.__move_to_shoot_closest_enemy(tank)
            # elif tank.get_type() == 'at_spg':
            #     # todo: handle it, below is only some kind of an example
            #     directions = [0, 2]
            #     potential_shooting_options = tank.get_possible_shots()
            #     true_shooting_options: tuple = ()
            #     for direction in directions:
            #         for i in range(3):
            #             if self._map.is_obstacle(potential_shooting_options[i * 6 + direction]):
            #                 break
            #             true_shooting_options += potential_shooting_options[i * 6 + direction]
            # else:
            #     self.__move_to_shoot_closest_enemy(tank)

        # single player:
        # for tank in self._tanks:
        #     self.__move_to_base(tank)

    def __move_to_base(self, tank: Tank):
        closest_base_coord = self._map.closest_base(tank.get_coord())
        if closest_base_coord is not None:
            self.__move_to(tank, closest_base_coord)

    def __move_to_shoot_closest_enemy(self, tank: Tank):
        # Find the closest enemy tank
        enemy: Tank = self._map.closest_enemy(tank)
        if enemy is not None:
            if tank.in_range(enemy.get_coord()) and self._map.can_shoot(self._player_index, enemy.get_player_index()):
                self.__update_shot(tank, enemy)
            else:
                self.__move_to(tank, enemy.get_coord())

    def __move_to(self, tank: Tank, where: tuple):
        next_best = self._map.next_best(tank, where)
        if next_best is not None:
            self.__update_move(tank, next_best)

    def __update_move(self, tank: Tank, action_coord: tuple) -> None:
        #print('has moved', 'id:', tank.get_id(), 'from:', tank.get_coord(), 'to:', action_coord)
        x, y, z = action_coord
        self._game_client.move({"vehicle_id": tank.get_id(), "target": {"x": x, "y": y, "z": z}})
        self._map.move(tank, action_coord)

    def __update_shot(self, tank: Tank, target: Tank):
        print(tank.get_player_index(), '->', target.get_player_index())
        x, y, z = target.get_coord()

        self._game_client.shoot({"vehicle_id": tank.get_id(), "target": {"x": x, "y": y, "z": z}})
        was_killed = self._map.shoot(tank, target)
        if was_killed:
            x, y, z = tank.get_coord()
            self._game_client.move({"vehicle_id": tank.get_id(), "target": {"x": x, "y": y, "z": z}})

