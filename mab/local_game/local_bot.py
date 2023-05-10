from mab.local_game.local_player import LocalPlayer
from src.entities.entity_enum import Entities
from src.entities.tanks.tank import Tank


class LocalBot(LocalPlayer):
    __actions = ('A', 'B', 'C', 'D', 'E', 'F', 'G')

    def __init__(self, player_index: int, game_actions: dict[str, str], current_turn: list[int]):
        super().__init__(player_index)
        self.__current_turn: list[int] = current_turn

        # game_actions = {tank_name: action_string}
        self.__game_actions = game_actions

    def _make_turn_plays(self) -> None:
        for tank in self._tanks:
            self.__do(self.__game_actions[tank.type][self.__current_turn[0]], tank)

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
            # Do action E, if health points != max health points and closest appropriate repair hex is free move into it
            # Do action E. This action only callable for tanks that can repair (at_spg, heavy_tank, medium_tank)
            self.__repair_if_low_hp_else_e(tank)

    def __repair_if_low_hp_else_e(self, tank):
        if tank.max_health_points != tank.health_points and self.__move_return_has_moved('repair', tank):
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
        if enemies_in_range:
            self.__camp(tank, enemies_in_range)
        else:
            self.__move_return_has_moved(where, tank)

    def __camp(self, tank: Tank, enemies_in_range: list[Tank]) -> None:
        if tank.type != Entities.TANK_DESTROYER:
            self.__update_maps_with_shot(tank, enemies_in_range[0])
        else:
            self.__td_camp(tank, self._map.tanks_in_range(tank))

    def __td_camp(self, td: Tank, tanks: list[Tank]) -> None:
        # Get the enemy in the fire corridor with the largest number of enemies and least friends
        tanks_by_corridor = [
            [tank for tank in tanks if tank.coord in c]
            for c in td.fire_corridors()
        ]

        best_score: float | int = 0
        best_corridor = None
        for corridor in tanks_by_corridor:
            score = sum(
                [1 if self._map.is_enemy(td, tank) else
                 -10 if self._map.is_neutral(td, tank) else -1.1
                 for tank in corridor]
            )
            if score > best_score:
                best_score, best_corridor = score, corridor

        if best_corridor and best_score > 0:
            self.__update_maps_with_shot(td, best_corridor[0], is_td=True)

    def __move_to_if_possible(self, tank: Tank, where: tuple) -> bool:
        next_best = self._map.next_best_available_hex_in_path_to(tank, where)

        if next_best is not None:
            self.__update_maps_with_move(tank, next_best)
            return True
        return False

    def __update_maps_with_move(self, tank: Tank, action_coord: tuple) -> None:
        self._map.local_move(tank, action_coord)

    def __update_maps_with_shot(self, tank: Tank, enemy: Tank, is_td=False) -> None:
        if is_td:
            td_shooting_coord = tank.td_shooting_coord(enemy.coord)
            self._map.td_shoot_no_graphics(tank, td_shooting_coord)
        else:
            self._map.local_shoot_no_graphics(tank, enemy)
