from pygame import Surface

from constants import HEX_RADIUS_X, HEX_RADIUS_Y, SCREEN_HEIGHT, SCREEN_WIDTH
from entities.map_features.bonuses.catapult import Catapult
from entities.map_features.feature_factory import FeatureFactory
from entities.map_features.landmarks.empty import Empty
from entities.map_features.landmarks.obstacle import Obstacle
from entities.tanks.tank import Tank
from entities.tanks.tank_factory import TankFactory
from game_map import _a_star
from game_map.hex import Hex
from gui.map_utils.map_drawer import MapDrawer


class Map:

    def __init__(self, client_map: dict, game_state: dict, active_players: dict, current_turn: list[int]):
        HEX_RADIUS_X[0] = SCREEN_WIDTH // ((client_map['size'] - 1) * 2 * 2)
        HEX_RADIUS_Y[0] = SCREEN_HEIGHT // ((client_map['size'] - 1) * 2 * 2)

        self.__players: dict = self.__add_players(active_players)
        self.__tanks: dict[int, Tank] = {}
        self.__destroyed: list[Tank] = []
        self.__base_coords: tuple = ()
        self.__base_adjacent_coords: tuple = ()
        self.__spawn_coords: tuple = ()
        self.__catapult_coords: tuple = ()
        self.__light_repair_coords: tuple = ()
        self.__hard_repair_coords: tuple = ()

        self.__map: dict = {}
        self.__map_size = client_map['size']
        self.__make_map(client_map, game_state, active_players)

        self.__path_finding_algorithm: callable = _a_star.a_star
        self.__map_drawer: MapDrawer = MapDrawer(client_map["size"], self.__players, self.__map, current_turn)

    """     MAP MAKING      """

    def __make_map(self, client_map: dict, game_state: dict, active_players: dict) -> None:
        # Make empty map
        rings = [Hex.make_ring(ring_num) for ring_num in range(client_map["size"])]
        self.__map = {coord: {'feature': Empty(coord), 'tank': None} for ring in rings for coord in ring}

        # Uncomment to save new maps to run in the local version
        # save_server_map(client_map)
        # save_game_state(game_state)

        # Make features, put them in map
        feature_factory = FeatureFactory(client_map["content"], self.__map)
        self.__base_coords = feature_factory.base_coords
        self.__base_adjacent_coords = feature_factory.base_adjacents
        self.__catapult_coords = feature_factory.catapult_coords
        self.__light_repair_coords = feature_factory.light_repair_coords
        self.__hard_repair_coords = feature_factory.hard_repair_coords

        # Make tanks & spawns, put them in map
        tank_factory = TankFactory(game_state["vehicles"], active_players, self.__map, self.__catapult_coords)
        self.__tanks = tank_factory.tanks

        del feature_factory, tank_factory

    @staticmethod
    def __add_players(active_players: dict) -> dict:
        return {player.index: player for player in active_players.values() if not player.is_observer}

    """     DRAWING     """

    def draw(self, screen: Surface) -> None:
        self.__map_drawer.draw(screen)

    """     SYNCHRONIZE SERVER AND LOCAL MAPS        """

    def update_turn(self, game_state: dict) -> None:
        # At the beginning of each turn move the tanks that have been destroyed in the previous turn to their spawn
        self.__respawn_destroyed_tanks()

        for vehicle_id, vehicle_info in game_state["vehicles"].items():
            server_coord = (vehicle_info["position"]["x"], vehicle_info["position"]["y"], vehicle_info["position"]["z"])
            server_hp, server_cp = vehicle_info['health'], vehicle_info["capture_points"]

            tank = self.__tanks[int(vehicle_id)]
            self.local_move(tank, server_coord) if server_coord != tank.coord else None
            tank.health_points = server_hp if server_hp != tank.health_points else tank.health_points
            tank.capture_points = server_cp if server_cp != tank.capture_points else tank.capture_points

    def __respawn_destroyed_tanks(self) -> None:
        while self.__destroyed:
            tank = self.__destroyed.pop()
            self.local_move(tank, tank.spawn_coord)
            tank.respawn()

    """     MOVE & FIRE CONTROL        """

    def local_move(self, tank: Tank, new_coord: tuple) -> None:
        self.__map[new_coord]['tank'] = tank  # New pos now has tank
        self.__map[tank.coord]['tank'] = None  # Old pos is now empty
        tank.coord = new_coord  # tank has new position

    def local_shoot(self, tank: Tank, target: Tank) -> None:
        destroyed = target.register_hit_return_destroyed()
        self.__map_drawer.add_shot(Hex.make_center(tank.coord), Hex.make_center(target.coord),
                                   tank.color)
        if destroyed:
            # update player damage points
            self.__players[tank.player_index].register_destroyed_vehicle(target)

            # add explosion
            self.__map_drawer.add_explosion(tank, target)

            # add to destroyed tanks
            self.__destroyed.append(target)
        else:
            self.__map_drawer.add_hitreg(Hex.make_center(target.coord), target.image_path, target.color)
        self.__players[tank.player_index].register_shot(target.player_index)

    def local_shoot_tuple(self, tank: Tank, coord: tuple) -> None:
        entities = self.__map.get(coord)
        if entities and not isinstance(entities['feature'], Obstacle):
            enemy = self.__map[coord]['tank']
            if self.is_enemy(tank, enemy):
                self.local_shoot(tank, enemy)

    def td_shoot(self, td: Tank, target: tuple) -> None:
        danger_zone = Hex.danger_zone(td.coord, target)
        for coord in danger_zone:
            entities = self.__map.get(coord)
            if entities and not isinstance(entities['feature'], Obstacle):
                target_tank = self.__map[coord]['tank']
                # Target tank can be an ally or an enemy
                if target_tank:
                    self.local_shoot(td, target_tank)
            else:
                break

    def is_neutral(self, player_tank: Tank, enemy_tank: Tank) -> bool:
        # Neutrality rule logic implemented here, return True if neutral, False if not neutral
        player_index, enemy_index = player_tank.player_index, enemy_tank.player_index
        other_index = next(iter({0, 1, 2} - {player_index, enemy_index}))
        other_player, enemy_player = self.__players[other_index], self.__players[enemy_index]
        return not enemy_player.has_shot(player_index) and other_player.has_shot(enemy_index)

    def is_enemy(self, friend: Tank, enemy: Tank) -> bool:
        return enemy and not (friend.player_index == enemy.player_index or
                              self.is_neutral(friend, enemy) or enemy.is_destroyed)

    """     NAVIGATION    """

    def __is_usable(self, bonus_coord: tuple, tank_type: str) -> bool:
        coord_dict = self.__map[bonus_coord]
        bonus, tank = coord_dict['feature'], coord_dict['tank']
        return not tank and bonus.is_usable(tank_type)

    @staticmethod
    def __features_by_dist(tank: Tank, feature_coords: tuple[tuple[int, int, int], ...]) -> list[tuple[int, int, int]]:
        return sorted(feature_coords, key=lambda coord: Hex.manhattan_dist(coord, tank.coord))

    def closest_usable_repair(self, tank: Tank) -> list[tuple[int, int, int]] | None:
        feature_coords = self.__hard_repair_coords
        if tank.type == 'medium_tank':
            feature_coords = self.__light_repair_coords
        closest_repair = self.__features_by_dist(tank, feature_coords)[0]
        if self.__is_usable(closest_repair, tank.type):
            return [closest_repair]

    def two_closest_catapults_if_usable(self, tank: Tank) -> list[tuple[int, int, int]]:
        two_closest = [coord for coord in self.__features_by_dist(tank, self.__catapult_coords)][:2]
        return [coord for coord in two_closest if self.__is_usable(coord, tank.type)]

    def tanks_in_range(self, tank: Tank) -> list[Tank]:
        is_on_catapult = isinstance(self.__map[tank.coord]['feature'], Catapult)
        return [
            tank for coord in tank.coords_in_range(is_on_catapult)
            if (tank := self.__map.get(coord, {}).get('tank')) is not None and not tank.is_destroyed
        ]

    def enemies_in_range(self, tank: Tank) -> list[Tank]:
        return [
            enemy for enemy in self.tanks_in_range(tank)
            if self.is_enemy(tank, enemy)
        ]

    def closest_free_bases(self, to: tuple) -> list[tuple] | None:
        free_base_coords = tuple(c for c in self.__base_coords if self.__map[c]['tank'] is None or c == to)
        if free_base_coords:
            return sorted(free_base_coords, key=lambda coord: Hex.manhattan_dist(to, coord))

        return None

    def closest_free_base_adjacents(self, to: tuple) -> list[tuple] | None:
        free_base_adjacents = [c for c in self.__base_adjacent_coords if self.__map[c]['tank'] is None or c == to]
        if free_base_adjacents:
            return sorted(free_base_adjacents, key=lambda coord: Hex.manhattan_dist(to, coord))

        return None

    def closest_enemies(self, tank: Tank) -> list[Tank]:
        # Returns a sorted list by distance of enemy tanks
        tank_idx, tank_coord = tank.player_index, tank.coord
        enemies = [self.__players[player] for player in self.__players if player != tank_idx]
        return sorted((enemy_tank for enemy in enemies for enemy_tank in enemy.tanks),
                      key=lambda enemy_tank: Hex.manhattan_dist(enemy_tank.coord, tank_coord))

    def next_best_available_hex_in_path_to(self, tank: Tank, finish: tuple) -> tuple | None:
        return self.__path_finding_algorithm(self.__map, tank, finish)
