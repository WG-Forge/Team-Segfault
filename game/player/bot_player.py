from threading import Semaphore, Event
from typing import List

from entity.tanks.tank import Tank
from player.player import Player


class BotPlayer(Player):
    def __init__(self, name: str, password: str, is_observer: bool, turn_played_sem: Semaphore,
                 current_player: list[1], player_index: int, over: Event):
        super().__init__(name=name,
                         password=password,
                         is_observer=is_observer,
                         turn_played_sem=turn_played_sem,
                         current_player=current_player,
                         player_index=player_index,
                         over=over)

        self.__turn: int = 0

    def _make_turn_plays(self) -> None:
        try:
            # play your move if you are the current player
            if self._current_player[0] == self.idx:
                # time.sleep(2)  # comment/uncomment this for a turn delay effect
                self.__place_actions()
        finally:
            # end your turn
            self._game_client.force_turn()

    def __place_actions(self) -> None:
        # Types: spg, light_tank, heavy_tank, medium_tank, at_spg

        if self._game_actions:
            for tank in self._tanks:
                action = self._game_actions[tank.get_type()][self.__turn]
                print('action', action)
                self.__do(action, tank)
        else:
            # multiplayer game:
            for tank in self._tanks:
                if tank.get_type() == 'light_tank':
                    self.__move_to_base(tank)
                else:
                    self.__move_to_shoot_closest_enemy(tank)
        self.__turn += 1

    def __do(self, action: str, tank: Tank) -> None:
        if action == 'camp_in_base' or action == 'camp_close_to_base':
            self.__camping(tank, action)
        elif action == 'shoot_closest_enemy':
            self.__move_to_shoot_closest_enemy(tank)

    def __camping(self, tank: Tank, camping_style: str) -> None:
        tank_coord = tank.get_coord()
        enemies_in_range = self._map.enemies_in_range(tank)
        if enemies_in_range:
            self.__camp(tank, enemies_in_range)
        else:
            if camping_style == 'in_base':
                go_to = self._map.closest_free_base(tank_coord)
            else:  # camping_style == 'close_to_base':
                go_to = self._map.closest_free_base_adjacent(tank_coord)
            if go_to and tank_coord != go_to:
                self.__move_to_if_possible(tank, go_to)

    def __camp_close_to_base(self, tank: Tank) -> None:
        self.__camping(tank, 'close_to_base')

    def __camp_in_base(self, tank: Tank) -> None:
        self.__camping(tank, 'in_base')

    def __camp(self, tank: Tank, enemies_in_range: List[Tank]) -> None:
        if tank.get_type() != 'at_spg':
            self.__update_maps_with_shot(tank, enemies_in_range[0])
        else:
            # Get the enemy in the fire corridor with the largest number of enemies
            enemy = max(([enemy for enemy in enemies_in_range if enemy.get_coord() in corridor] for corridor in
                         tank.fire_corridors()), key=lambda enemies: len(enemies))[0]
            self.__update_maps_with_shot(tank, enemy, is_td=True)

    def __move_to_base(self, tank: Tank):
        closest_base_coord = self._map.closest_free_base(tank.get_coord())
        if closest_base_coord is not None:
            self.__move_to_if_possible(tank, closest_base_coord)

    def __move_to_shoot_closest_enemy(self, tank: Tank):
        for enemy in self._map.closest_enemies(tank):
            shot_moves = tank.shot_moves(enemy.get_coord())
            if tank.get_coord() in shot_moves and not (self._map.is_neutral(tank, enemy) or enemy.is_destroyed()):
                if tank.get_type() != 'at_spg':
                    self.__update_maps_with_shot(tank, enemy)
                else:
                    self.__update_maps_with_shot(tank, enemy, is_td=True)
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

    def __update_maps_with_shot(self, tank: Tank, enemy: Tank, is_td=False):
        if is_td:
            td_shooting_coord = tank.td_shooting_coord(enemy.get_coord())
            x, y, z = td_shooting_coord
            self._map.td_shoot(tank, td_shooting_coord)
        else:
            x, y, z = enemy.get_coord()
            self._map.local_shoot(tank, enemy)

        self._game_client.server_shoot({"vehicle_id": tank.get_id(), "target": {"x": x, "y": y, "z": z}})
