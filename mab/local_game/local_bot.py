from mab.local_game.local_player import LocalPlayer
from src.entities.entity_enum import Entities
from src.entities.tanks.tank import Tank


class LocalBot(LocalPlayer):
    __actions = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O')
    __no_repair_actions = ('A', 'B', 'C', 'D', 'E', 'F')
    __num_actions = len(__actions)
    __tank_names_can_repair = {
        'spg': False, 'light_tank': False, 'heavy_tank': True, 'medium_tank': True, 'at_spg': True
    }

    def __init__(self, player_idx: int, best_actions: dict, current_round: list[int]):
        super().__init__(player_idx=player_idx)
        self.__current_round: list[int] = current_round
        self.__best_actions: dict = best_actions

    def _make_turn_plays(self) -> None:
        self.__place_actions()

    def __place_actions(self) -> None:
        for tank in self._tanks:
            action = self.__best_actions[tank.type][self.__current_round[0]]
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

        # Shoot enemies in range, if none & has catapult bonus do action. If no bonus move to usable catapult,
        #  if none do repair action if can repair else do non repair action.
        elif action == 'F':
            if self.__tank_names_can_repair[tank.type]:
                self.__catapult_else(tank, 'K')
            else:
                self.__catapult_else(tank, 'A')
        elif action == 'G':
            if self.__tank_names_can_repair[tank.type]:
                self.__catapult_else(tank, 'L')
            else:
                self.__catapult_else(tank, 'B')
        elif action == 'H':
            if self.__tank_names_can_repair[tank.type]:
                self.__catapult_else(tank, 'M')
            else:
                self.__catapult_else(tank, 'C')
        elif action == 'I':
            if self.__tank_names_can_repair[tank.type]:
                self.__catapult_else(tank, 'N')
            else:
                self.__catapult_else(tank, 'D')
        elif action == 'J':
            if self.__tank_names_can_repair[tank.type]:
                self.__catapult_else(tank, 'O')
            else:
                self.__catapult_else(tank, 'E')

        # Do actions, if health points == 1 and closest appropriate repair is free & can repair move there
        elif action == 'K':
            self.__repair_if_low_hp_else(tank, 'A')
        elif action == 'L':
            self.__repair_if_low_hp_else(tank, 'B')
        elif action == 'M':
            self.__repair_if_low_hp_else(tank, 'C')
        elif action == 'N':
            self.__repair_if_low_hp_else(tank, 'D')
        elif action == 'O':
            self.__repair_if_low_hp_else(tank, 'E')

    def __repair_if_low_hp_else(self, tank: Tank, action: str) -> None:
        if tank.health_points == 1 and self.__tank_names_can_repair[tank.type] \
                and self.__move_return_has_moved('repair', tank):
            return
        self.__do(action, tank)

    def __catapult_else(self, tank: Tank, action: str) -> None:
        enemies_in_range = self._map.enemies_in_range(tank)
        if enemies_in_range:
            self.__camp(tank, enemies_in_range)
        else:
            if tank.catapult_bonus:
                self.__do(action, tank)
            elif not self.__move_return_has_moved('catapult', tank):
                if self._map.is_catapult_and_usable(tank.coord):
                    return
                cats = self._map.two_closest_catapults_if_usable(tank)
                if len(cats) == 0:
                    self.__do(action, tank)

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
        next_best = self._map.next_best_available_hex_in_path_to(tank, where)

        if next_best is not None:
            self.__update_maps_with_move(tank, next_best)
            return True
        return False

    def __update_maps_with_move(self, tank: Tank, action_coord: tuple) -> None:
        self._map.local_move(tank, action_coord)

    def __update_maps_with_tank_shot(self, tank: Tank, enemy: Tank) -> None:
        self._map.local_shoot_no_graphics(tank, enemy)

    def __update_maps_with_td_shot(self, tank: Tank, td_fire_corridor: list[tuple]) -> None:
        self._map.td_shoot_no_graphics(tank, td_fire_corridor)

    @staticmethod
    def __best_shooting_target(enemies_in_range: list[Tank]) -> Tank:
        """Returns the tank with the lowest health points and the most max health points in enemies_in_range"""
        target: Tank | None = None
        for tank in enemies_in_range:
            if target is None or tank.health_points < target.health_points or \
                    (tank.health_points == target.health_points and target.max_health_points < tank.max_health_points):
                target = tank
        return target

