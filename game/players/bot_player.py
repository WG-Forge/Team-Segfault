import time
from threading import Semaphore, Event

from constants import GAME_SPEED
from entities.entity_enum import Entities
from entities.tanks.tank import Tank
from players.player import Player


class BotPlayer(Player):
    def __init__(self, name: str, password: str, is_observer: bool, turn_played_sem: Semaphore,
                 current_player: list[int], player_index: int, over: Event):
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
                delay = 1.0 - GAME_SPEED[0]
                if delay > 0:
                    time.sleep(delay)  # comment/uncomment this for a turn delay effect
                self.__place_actions()
        finally:
            # end your turn
            self._game_client.force_turn()

    def _finalize(self) -> None:
        # manage your own connection
        self._game_client.logout()
        self._game_client.disconnect()

    def __place_actions(self) -> None:
        # Types: spg, light_tank, heavy_tank, medium_tank, at_spg

        if self._game_actions:
            for tank in self._tanks:
                action = self._game_actions[tank.type][self.__turn]
                self.__do(action, tank)
        else:
            # multiplayer game:
            actions = ('A', 'B', 'C', 'D', 'E')
            for action, tank in zip(actions, self._tanks):
                self.__do(action, tank)

        self.__turn += 1

    def __do(self, action: str, tank: Tank) -> None:
        if action == 'A':
            self.__shoot_else_move(tank, 'close enemy')
        elif action == 'B':
            self.__move_and_camp(tank, 'in base')
        elif action == 'C':
            self.__move_and_camp(tank, 'close to base')
        elif action == 'D':
            self.__shoot_else_move(tank, 'in base')
        elif action == 'E':
            self.__shoot_else_move(tank, 'close to base')

    def __move_and_camp(self, tank: Tank, where: str) -> None:
        if not self.__move(where, tank):
            enemies_in_range = self._map.enemies_in_range(tank)
            if enemies_in_range:
                self.__camp(tank, enemies_in_range)

    def __shoot_else_move(self, tank: Tank, where: str) -> None:
        enemies_in_range = self._map.enemies_in_range(tank)
        if enemies_in_range:
            self.__camp(tank, enemies_in_range)
        else:
            self.__move(where, tank)

    def __camp(self, tank: Tank, enemies_in_range: list[Tank]) -> None:
        if tank.type != Entities.TANK_DESTROYER:
            self.__update_maps_with_shot(tank, enemies_in_range[0])
        else:
            self.__td_camp(tank, self._map.tanks_in_range(tank))

    def __td_camp(self, td: Tank, tanks: list[Tank]) -> None:
        # Get the enemy in the fire corridor with the largest number of enemies and least friends
        tanks_by_corridor = [[tank for tank in tanks if tank.coord in c] for c in td.fire_corridors()]

        best_score: float | int = 0
        best_corridor = None
        for corridor in tanks_by_corridor:
            score = sum(
                [1 if self._map.is_enemy(td, tank) else -10 if self._map.is_neutral(td, tank) else -1.1 for tank in
                 corridor])
            if score > best_score:
                best_score = score
                best_corridor = corridor

        if best_corridor and best_score > 0:
            self.__update_maps_with_shot(td, best_corridor[0], is_td=True)

    def __move(self, where: str, who: Tank) -> bool:
        who_coord, go_to = who.coord, None
        if where == 'close to base':
            go_to = self._map.closest_free_base_adjacents(who_coord)
        elif where == 'in base':
            go_to = self._map.closest_free_bases(who_coord)
        elif where == 'close enemy':
            if self._map.closest_enemies(who):
                go_to = who.shot_moves(self._map.closest_enemies(who)[0].coord)
        if go_to:  # TODO: Solve this dirty fix, find out why 'go_to' is None in edge cases
            for coord in go_to:
                if who_coord == coord or self.__move_to_if_possible(who, coord):
                    return True
        return False

    def __move_to_if_possible(self, tank: Tank, where: tuple) -> bool:
        next_best = self._map.next_best_available_hex_in_path_to(tank, where)
        if next_best is not None:
            self.__update_maps_with_move(tank, next_best)
            return True
        return False

    def __update_maps_with_move(self, tank: Tank, action_coord: tuple) -> None:
        x, y, z = action_coord
        self._map.local_move(tank, action_coord)
        self._game_client.server_move({"vehicle_id": tank.tank_id, "target": {"x": x, "y": y, "z": z}})

    def __update_maps_with_shot(self, tank: Tank, enemy: Tank, is_td=False) -> None:
        if is_td:
            td_shooting_coord = tank.td_shooting_coord(enemy.coord)
            x, y, z = td_shooting_coord
            self._map.td_shoot(tank, td_shooting_coord)
        else:
            x, y, z = enemy.coord
            self._map.local_shoot(tank, enemy)

        self._game_client.server_shoot({"vehicle_id": tank.tank_id, "target": {"x": x, "y": y, "z": z}})
