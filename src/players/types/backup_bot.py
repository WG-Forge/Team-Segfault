import time
from enum import IntEnum
from threading import Semaphore, Event

from src.constants import GAME_SPEED
from src.entities.entity_enum import Entities
from src.entities.tanks.tank import Tank
from src.players.player import Player


class Callout(IntEnum):
    CLOSE_TO_BASE = 0
    INSIDE_BASE = 1
    CLOSEST_ENEMY = 2
    CATAPULT = 3
    REPAIR = 4


class BackupBot(Player):
    """To use this class, change the import in player_factory.py to this class instead of bot_player"""

    def __init__(self, turn_played_sem: Semaphore, current_player: list[int], current_turn: list[int],
                 over: Event, game_exited: Event,
                 name: str | None = None, password: str | None = None,
                 is_observer: bool | None = None):
        super().__init__(turn_played_sem=turn_played_sem,
                         current_player=current_player, current_turn=current_turn,
                         over=over, game_exited=game_exited,
                         name=name, password=password,
                         is_observer=is_observer)
        self.__safe_hexes: dict | None = None

    def register_round(self) -> None:
        super().register_round()

    def _make_turn_plays(self) -> None:
        try:
            # play your move if you are the current player
            if self._current_player[0] == self.idx:
                delay = 1.0 - GAME_SPEED[0]
                if delay > 0:
                    time.sleep(delay)  # comment/uncomment this for a turn delay effect
                # self.__safe_hexes = self._map.get_safe_hexes(self.idx)
                self.__place_actions()
        except Exception as e:
            print(e)
        finally:
            # end your turn
            self._game_client.force_turn()

    def _logout(self) -> None:
        # manage your own connection
        self._game_client.logout()
        self._game_client.disconnect()

    def __place_actions(self) -> None:
        if self._current_turn[0] <= self._num_players:
            self._map.set_order_by_idx(self._current_turn[0], self.idx)

        for tank in self._tanks:
            location = Callout.INSIDE_BASE

            if tank.type == Entities.HEAVY_TANK and tank.health_points == 1:
                location = Callout.REPAIR
            if tank.type == Entities.LIGHT_TANK and not tank.catapult_bonus:
                location = Callout.CATAPULT

            self.__shoot_else_move(tank, location)

    def __move_return_has_moved(self, where: Callout, who: Tank) -> bool:
        """Tries to move the to the 'where' callout, returns True on success"""
        who_coord = who.coord
        go_to: list[tuple[int, int, int]] = []
        match where:
            case Callout.CLOSE_TO_BASE:
                go_to += self._map.closest_free_base_adjacents(who_coord)
            case Callout.INSIDE_BASE:
                go_to += self._map.closest_free_bases(who_coord)
            case Callout.CLOSEST_ENEMY:
                closest = self._map.closest_enemies(who)
                if closest:
                    for enemy in closest:
                        go_to.append(who.shot_moves(enemy.coord))
            case Callout.REPAIR:
                go_to += self._map.closest_usable_repair(who)
            case Callout.CATAPULT:
                go_to += self._map.two_closest_catapults_if_usable(who)

        if go_to:
            for coord in go_to:
                if who_coord == coord:
                    return False
                if self.__move_to_if_possible(who, coord):
                    return True

        return False

    def __move_else_shoot(self, tank: Tank, where: Callout) -> None:
        """Moves the tank to designated position if possible, otherwise it shoots an enemy in range (if any)"""
        if not self.__move_return_has_moved(where, tank):
            enemies_in_range = self._map.enemies_in_range(tank)
            if enemies_in_range:
                self.__shoot(tank, enemies_in_range)

    def __shoot_else_move(self, tank: Tank, where: Callout) -> None:
        enemies_in_range = self._map.enemies_in_range(tank)
        if not enemies_in_range:
            self.__move_return_has_moved(where, tank)
        else:
            self.__shoot(tank, enemies_in_range)

    def __shoot(self, tank: Tank, enemies_in_range: list[Tank]) -> None:
        if tank.type != Entities.TANK_DESTROYER:
            self.__update_maps_with_tank_shot(tank, self.__best_shooting_target(enemies_in_range))
        else:
            self.__td_camp(tank, self._map.enemies_in_range(tank))

    def __td_camp(self, td: Tank, enemy_tanks: list[Tank]) -> bool:
        # Shoot the fire corridor with the largest damage potential, if no damage potential in any get the
        # corridor with the most enemies, if no enemies return False, is has shot return True
        td_fire_corridors = td.fire_corridors()
        tanks_by_corridor = [
            [tank for tank in enemy_tanks if tank.coord in corridor]
            for corridor in td_fire_corridors]

        most_damage_index, most_damage_potential = max(
            ((i, sum(tank.max_health_points for tank in corridor if tank.health_points == 1))
             for i, corridor in enumerate(tanks_by_corridor)), key=lambda x: x[1], default=(None, 0))

        if most_damage_index:
            self.__update_maps_with_td_shot(td, td_fire_corridors[most_damage_index])
            return True

        most_enemies_index, most_enemies = max(((i, len(corridor)) for i, corridor in enumerate(tanks_by_corridor)),
                                               key=lambda x: x[1], default=(None, 0))
        if most_enemies_index:
            self.__update_maps_with_td_shot(td, td_fire_corridors[most_enemies_index])
            return True

        return False

    def __move_to_if_possible(self, tank: Tank, where: tuple) -> bool:
        """Tries to move 'tank' to given coordinate 'where', returns True on success"""
        next_best = self._map.next_best_available_hex_in_path_to(tank, where)

        if next_best is not None:  # and next_best not in self.__safe_hexes:
            self.__update_maps_with_move(tank, next_best)
            return True
        return False

    def __update_maps_with_move(self, tank: Tank, action_coord: tuple) -> None:
        x, y, z = action_coord
        self._map.local_move(tank, action_coord)
        self._game_client.server_move({"vehicle_id": tank.tank_id, "target": {"x": x, "y": y, "z": z}})

    def __update_maps_with_tank_shot(self, tank: Tank, enemy: Tank) -> None:
        self._map.local_shoot(tank, enemy)
        x, y, z = enemy.coord
        self._game_client.server_shoot({"vehicle_id": tank.tank_id, "target": {"x": x, "y": y, "z": z}})

    def __update_maps_with_td_shot(self, tank: Tank, td_fire_corridor: list[tuple]) -> None:
        x, y, z = td_fire_corridor[0]
        self._map.td_shoot(tank, td_fire_corridor)
        self._game_client.server_shoot({"vehicle_id": tank.tank_id, "target": {"x": x, "y": y, "z": z}})

    @staticmethod
    def __best_shooting_target(enemies_in_range: list[Tank]) -> Tank:
        """Returns the tank with the lowest health points and the most max health points in enemies_in_range"""
        target: Tank | None = None
        for tank in enemies_in_range:
            if target is None or tank.health_points < target.health_points or \
                    (tank.health_points == target.health_points and target.max_health_points < tank.max_health_points):
                target = tank
        return target
