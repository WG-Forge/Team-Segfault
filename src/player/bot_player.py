from abc import ABC
from threading import Semaphore

from src.entity.tanks.tank import Tank
from src.player.player import Player


class BotPlayer(Player, ABC):
    def __init__(self, name: str, password: str, is_observer: bool, turn_played_sem: Semaphore,
                 current_player: list[1], player_index: int):
        super().__init__(name, password, is_observer, turn_played_sem, current_player, player_index)

    def _make_turn_plays(self) -> None:
        # Types: spg, light_tank, heavy_tank, medium_tank, at_spg

        # multiplayer game:
        for tank in self._tanks:
            if tank.get_type() == 'light_tank':
                self.__move_to_base(tank)
            elif tank.get_type() == 'at_spg':
                # todo: handle it, below is only some kind of an example
                directions = [0, 2]
                potential_shooting_options = tank.get_possible_shots()
                true_shooting_options: tuple = ()
                for direction in directions:
                    for i in range(3):
                        if self._map.is_obstacle(potential_shooting_options[i * 6 + direction]):
                            break
                        true_shooting_options += potential_shooting_options[i * 6 + direction]
            else:
                self.__move_to_shoot_closest_enemy(tank)

        # single player:
        # for tank in self._tanks:
        #     self.__move_to_base(tank)

    def can_shoot(self, enemy: Tank) -> bool:
        # Implements logic of the neutrality rule
        player_index = self._player_index
        enemy_index = enemy.get_player_index()
        other_index = next(iter({0, 1, 2} - {player_index, enemy_index}))
        enemy_player = self._map.get_player(enemy_index)

        enemy_has_attacked_player = self.was_attacked_by(enemy_index)
        enemy_was_attacked_by_other = enemy_player.was_attacked_by(other_index)

        return enemy_has_attacked_player or not enemy_was_attacked_by_other

    def __move_to_base(self, tank: Tank):
        closest_base_coord = self._map.closest_base(tank.get_coord())
        if closest_base_coord == tank.get_coord():
            return
        if closest_base_coord is not None:
            self.__move_to(tank, closest_base_coord)

    def __move_to_shoot_closest_enemy(self, tank: Tank):
        # Find the closest enemy
        enemy: Tank = self._map.closest_enemy(tank)
        if enemy is not None and self.can_shoot(enemy):
            if tank.in_range(enemy.get_coord()):
                self.__update_shot(tank, enemy)
            else:
                self.__move_to(tank, enemy.get_coord())

    def __move_to(self, tank: Tank, where: tuple):
        next_best = self._map.next_best(tank, where)
        if next_best is not None:
            self.__update_move(tank, next_best)

    def __update_move(self, tank: Tank, action_coord: tuple) -> None:
        print('has moved', 'id:', tank.get_id(), 'from:', tank.get_coord(), 'to:', action_coord)
        x, y, z = action_coord
        self._game_client.move({"vehicle_id": tank.get_id(), "target": {"x": x, "y": y, "z": z}})
        self._map.move(tank, action_coord)

    def __update_shot(self, tank: Tank, target: Tank):
        print('has shot', 'id:', tank.get_id(), 'from:', tank.get_coord(), 'who:', target.get_id(), target.get_coord())
        x, y, z = target.get_coord()

        # Register that self has attacked target player
        attacker_index = tank.get_player_index()
        target_player = self._map.get_player(target.get_player_index())
        target_player.register_attacker(attacker_index)

        self._game_client.shoot({"vehicle_id": tank.get_id(), "target": {"x": x, "y": y, "z": z}})
        self._map.shoot(tank, target)
