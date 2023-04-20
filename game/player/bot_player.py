from threading import Semaphore, Event

from entity.tanks.tank import Tank
from map.hex import Hex
from player.player import Player


class BotPlayer(Player):
    def __init__(self, name: str, password: str, is_observer: bool, turn_played_sem: Semaphore,
                 current_player: list[1], player_index: int, active: Event):
        super().__init__(name, password, is_observer, turn_played_sem, current_player, player_index, active)

    def _make_turn_plays(self) -> None:
        # Types: spg, light_tank, heavy_tank, medium_tank, at_spg

        # multiplayer game:
        for tank in self._tanks:
            if tank.get_type() == 'light_tank':
                self.__move_to_base(tank)
            else:
                self.__move_to_shoot_closest_enemy(tank)

    def __move_to_base(self, tank: Tank):
        closest_base_coord = self._map.closest_base(tank.get_coord())
        if closest_base_coord is not None:
            self.__move_to_if_possible(tank, closest_base_coord)

    def __move_to_shoot_closest_enemy(self, tank: Tank):
        for enemy in self._map.closest_enemies(tank):
            shot_moves = tank.shot_moves(enemy.get_coord())
            if tank.get_coord() in shot_moves and not (self._map.is_neutral(tank, enemy) or enemy.is_destroyed()):
                if tank.get_type() != 'at_spg':
                    self.__update_maps_with_shot(tank, enemy)
                else:
                    td_shooting_coord = Hex.td_shooting_coord(tank.get_coord(), enemy.get_coord())
                    self.__update_maps_with_shot(tank, enemy, td_shooting_coord=td_shooting_coord)
            else:
                for coord in shot_moves:
                    if self.__move_to_if_possible(tank, coord):
                        break
            break

    def __move_to_if_possible(self, tank: Tank, where: tuple) -> bool:
        next_best = self._map.next_best_available_hex_in_path_to(tank, where)
        if next_best is not None:
            self.__update_maps_with_move(tank, next_best)
            return True
        return False

    def __update_maps_with_move(self, tank: Tank, action_coord: tuple) -> None:
        x, y, z = action_coord
        self._map.local_move(tank, action_coord)
        self._game_client.server_move({"vehicle_id": tank.get_id(), "target": {"x": x, "y": y, "z": z}})

    def __update_maps_with_shot(self, tank: Tank, target: Tank, td_shooting_coord=None):
        if td_shooting_coord is None:
            x, y, z = target.get_coord()
            self._map.local_shoot(tank, target)
        else:
            x, y, z = td_shooting_coord
            self._map.td_shoot(tank, td_shooting_coord)

        self._game_client.server_shoot({"vehicle_id": tank.get_id(), "target": {"x": x, "y": y, "z": z}})
