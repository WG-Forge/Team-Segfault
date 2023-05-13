import random as rnd
import time
from threading import Semaphore, Event

from mab.data.data_io import DataIO
from src.constants import GAME_SPEED
from src.entities.entity_enum import Entities
from src.entities.tanks.tank import Tank
from src.players.player import Player


class BotPlayer(Player):
    __actions = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
    __no_repair_actions = ('A', 'B', 'C', 'D', 'E', 'F')
    __num_actions = len(__actions)
    __tank_names_can_repair = {
        'spg': False, 'light_tank': False, 'heavy_tank': True, 'medium_tank': True, 'at_spg': True
    }

    def __init__(self, turn_played_sem: Semaphore, current_player: list[int], current_turn: list[int],
                 over: Event, game_exited: Event,
                 name: str | None = None, password: str | None = None,
                 is_observer: bool | None = None):
        super().__init__(turn_played_sem=turn_played_sem,
                         current_player=current_player, current_turn=current_turn,
                         over=over, game_exited=game_exited,
                         name=name, password=password,
                         is_observer=is_observer)
        self.__order = None

    def register_round(self) -> None:
        # reset round actions
        self._best_actions = None

        super().register_round()

    def _make_turn_plays(self) -> None:
        try:
            # play your move if you are the current player
            if self._current_player[0] == self.idx:
                delay = 1.0 - GAME_SPEED[0]
                if delay > 0:
                    time.sleep(delay)  # comment/uncomment this for a turn delay effect
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
            self.__order = self._current_turn[0]

        # set round actions based on first turn order
        if not self._best_actions:
            self._best_actions = DataIO.load_best_actions()[str(self._current_turn[0] % self._num_players)]

        # Types: spg, light_tank, heavy_tank, medium_tank, at_spg
        if self._best_actions:
            for tank in self._tanks:
                action = self._best_actions[tank.type][self._current_turn[0]]
                self.__do(action, tank)
        else:
            # testing catapult action
            # for tank in self._tanks:
            #     if tank.catapult_bonus:
            #         self.__do('C', tank)
            #     else:
            #         self.__do('F', tank)

            # testing random actions
            for tank in self._tanks:
                action = None
                can_repair = self.__tank_names_can_repair[tank.type]
                possible_actions = self.__actions if can_repair else self.__no_repair_actions
                while action not in possible_actions:
                    action = self.__actions[rnd.randint(0, len(possible_actions) - 1)]
                self.__do(action, tank)

    def __do(self, action: str, tank: Tank) -> None:
        if action == 'A':
            # Move into the closest free base and from then on shoot enemies in range without moving
            self.__move_and_camp(tank, 'in base')
        elif action == 'B':
            # Move into the closest free hex adjacent to the base and shoot enemies in range
            self.__move_and_camp(tank, 'close to base')
        elif action == 'C':
            # If there are enemies in range shoot them, else move towards
            # a position where this tank can shoot the closest enemy
            self.__shoot_else_move(tank, 'close enemy')
        elif action == 'D':
            # If there are enemies in range shoot them, else, move towards the closest free base
            self.__shoot_else_move(tank, 'in base')
        elif action == 'E':
            # If there are enemies in range shoot them, else, move towards the closest free hex adjacent to the base
            self.__shoot_else_move(tank, 'close to base')
        elif action == 'F':
            # Shoot enemies in range if no enemies in range move towards the closest of the two catapults
            # that is usable. If on the catapult, stay.
            # Else if both catapults are occupied or none of them have shots left do action E
            self.__catapult_else_e(tank)
        elif action == 'G':
            # Do action E, if health points == 1 and closest appropriate repair hex is free move into it
            # Do action E. This action only callable for tanks that can repair (at_spg, heavy_tank, medium_tank)
            self.__repair_if_low_hp_else_e(tank)

    def __repair_if_low_hp_else_e(self, tank):
        if tank.health_points == 1 and self.__tank_names_can_repair[tank.type] \
                and self.__move_return_has_moved('repair', tank):
            return
        self.__do('E', tank)

    def __catapult_else_e(self, tank: Tank) -> None:
        enemies_in_range = self._map.enemies_in_range(tank)
        if enemies_in_range:
            self.__camp(tank, enemies_in_range)
        else:
            if not self.__move_return_has_moved('catapult', tank):
                if self._map.is_catapult_and_usable(tank.coord):
                    return
                cats = self._map.two_closest_catapults_if_usable(tank)
                if len(cats) == 0:
                    self.__do('E', tank)

    def __move_return_has_moved(self, where: str, who: Tank) -> bool:
        who_coord, go_to = who.coord, None
        if where == 'close to base':
            go_to = self._map.closest_free_base_adjacents(who_coord)
        elif where == 'in base':
            go_to = self._map.closest_free_bases(who_coord)
        elif where == 'close enemy':
            if self._map.closest_enemies(who):
                go_to = who.shot_moves(self._map.closest_enemies(who)[0].coord)
        elif where == 'repair':
            go_to = self._map.closest_usable_repair(who)
        elif where == 'catapult':
            go_to = self._map.two_closest_catapults_if_usable(who)

        if go_to:  # TODO: Find out why 'go_to' is None in edge cases
            for coord in go_to:
                if who_coord == coord:
                    return False
                if self.__move_to_if_possible(who, coord):
                    return True
        return False

    def __move_and_camp(self, tank: Tank, where: str) -> None:
        if not self.__move_return_has_moved(where, tank):
            enemies_in_range = self._map.enemies_in_range(tank)
            if enemies_in_range:
                self.__camp(tank, enemies_in_range)

    def __shoot_else_move(self, tank: Tank, where: str) -> None:
        enemies_in_range = self._map.enemies_in_range(tank)
        if not enemies_in_range:
            self.__move_return_has_moved(where, tank)
        else:
            self.__camp(tank, enemies_in_range)

    def __camp(self, tank: Tank, enemies_in_range: list[Tank]) -> None:
        if tank.type != Entities.TANK_DESTROYER:
            self.__update_maps_with_tank_shot(tank, self.__highest_damage_potential_enemy(enemies_in_range))
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
        next_best = self._map.next_best_available_hex_in_path_to(tank, where)

        if next_best is not None:
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
    def __highest_damage_potential_enemy(enemies_in_range: list[Tank]) -> Tank:
        """Out of the tanks with the lowest health return the tank with the highest max health"""
        enemies_by_health = sorted(enemies_in_range, key=lambda e: e.health_points)

        target = enemies_by_health[0]
        min_health = target.health_points
        max_damage_potential = 0

        for enemy in enemies_by_health:
            if enemy.health_points > min_health:
                break
            elif enemy.max_health_points > max_damage_potential:
                target = enemy
                max_damage_potential = enemy.max_health_points

        return target
