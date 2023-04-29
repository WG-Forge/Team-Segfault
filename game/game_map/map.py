from typing import List, Union, Callable, Dict

from pygame import Surface

from constants import HEX_RADIUS_X, HEX_RADIUS_Y, SCREEN_HEIGHT, SCREEN_WIDTH
from entities.map_features.base import Base
from entities.map_features.empty import Empty
from entities.map_features.obstacle import Obstacle
from entities.tanks.tank import Tank
from entities.tanks.tank_factory import TankFactory
from game_map import _a_star
from game_map.hex import Hex
from gui.map_utils.map_drawer import MapDrawer


class Map:
    def __init__(self, client_map: Dict, game_state: Dict, active_players: Dict, current_turn: list[1]):
        HEX_RADIUS_X[0] = SCREEN_WIDTH // ((client_map['size'] - 1) * 2 * 2)
        HEX_RADIUS_Y[0] = SCREEN_HEIGHT // ((client_map['size'] - 1) * 2 * 2)

        self.__players: Dict = Map.__add_players(active_players)
        self.__tanks: Dict[int, Tank] = {}

        self.__map: Dict = {}
        self.__map_size = client_map['size']
        self.__base_coords: tuple = ()
        self.__base_adjacent_coords: tuple = ()
        self.__spawn_coords: tuple = ()
        self.__make_map(client_map, game_state, active_players)
        self.__destroyed: List[Tank] = []

        self.__path_finding_algorithm: Callable = _a_star.a_star

        self.__map_drawer: MapDrawer = MapDrawer(client_map["size"], self.__players, self.__map, current_turn)

    """     MAP MAKING      """

    def __make_map(self, client_map: Dict, game_state: Dict, active_players: Dict) -> None:
        # Make empty map
        rings = [Hex.make_ring(ring_num) for ring_num in range(client_map["size"])]
        self.__map = {coord: {'feature': Empty(coord), 'tank': None} for ring in rings for coord in ring}

        # Uncomment to save new maps to run in the local version
        # save_server_map(client_map)
        # save_game_state(game_state)

        # put tanks in tanks & map & put spawns in map
        for vehicle_id, vehicle_info in game_state["vehicles"].items():
            player = active_players[vehicle_info["player_id"]]
            tank, spawn = TankFactory.create_tank_and_spawn(int(vehicle_id), vehicle_info, player.color,
                                                            player.index)
            tank_coord = tank.coord
            self.__map[tank_coord]['tank'] = tank
            self.__map[tank.spawn_coord]['feature'] = spawn
            self.__tanks[int(vehicle_id)] = tank
            player.add_tank(tank)

        # Put entities in map
        for entity, info in client_map["content"].items():
            if entity == "base":
                self.__make_bases(info)
            elif entity == 'obstacle':
                self.__make_obstacles(info)
            else:
                print(f"Support for {entity} needed")

    @staticmethod
    def __add_players(active_players: Dict) -> Dict:
        players = {}
        for player_id, player in active_players.items():
            if not player.is_observer:
                players[player.index] = player
        return players

    def __make_bases(self, coords: Dict) -> None:
        self.__base_coords = tuple([tuple(coord.values()) for coord in coords])
        for coord in self.__base_coords:
            self.__map[coord]['feature'] = Base(coord)
        self.__make_base_adjacents()

    def __make_base_adjacents(self):
        adjacent_deltas = Hex.make_ring(1)
        self.__base_adjacent_coords = list({Hex.coord_sum(delta, base_coord) for base_coord in self.__base_coords
                                            for delta in adjacent_deltas} - set(self.__base_coords))

    def __make_obstacles(self, obstacles: []) -> None:
        for d in obstacles:
            coord = (d['x'], d['y'], d['z'])
            self.__map[coord]['feature'] = Obstacle(coord)

    """     DRAWING     """

    def draw(self, screen: Surface):
        self.__map_drawer.draw(screen)

    """     SYNCHRONIZE SERVER AND LOCAL MAPS        """

    def update_turn(self, game_state: Dict) -> None:
        # At the beginning of each turn move the tanks that have been destroyed in the previous turn to their spawn
        self.__respawn_destroyed_tanks()

        for vehicle_id, vehicle_info in game_state["vehicles"].items():
            server_coord = (vehicle_info["position"]["x"], vehicle_info["position"]["y"], vehicle_info["position"]["z"])
            server_hp, server_cp = vehicle_info['health'], vehicle_info["capture_points"]

            tank = self.__tanks[int(vehicle_id)]
            self.local_move(tank, server_coord) if server_coord != tank.coord else None
            tank.hp = server_hp if server_hp != tank.hp else tank.hp
            tank.cp = server_cp if server_cp != tank.cp else tank.cp

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

        self.__players[tank.player_index].register_shot(target.player_index)

    def local_shoot_tuple(self, tank: Tank, coord: tuple):
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

    def tanks_in_range(self, tank: Tank) -> List[Tank]:
        return [tank for coord in tank.coords_in_range() if
                (tank := self.__map.get(coord, {}).get('tank')) is not None and not tank.is_destroyed]

    def enemies_in_range(self, tank: Tank) -> List[Tank]:
        return [enemy for enemy in self.tanks_in_range(tank) if self.is_enemy(tank, enemy)]

    def closest_free_bases(self, to: tuple) -> Union[List[tuple], None]:
        free_base_coords = tuple(c for c in self.__base_coords if self.__map[c]['tank'] is None or c == to)
        if free_base_coords:
            return sorted(free_base_coords, key=lambda coord: Hex.manhattan_dist(to, coord))

    def closest_free_base_adjacents(self, to: tuple) -> Union[List[tuple], None]:
        free_base_adjacents = [c for c in self.__base_adjacent_coords if self.__map[c]['tank'] is None or c == to]
        if free_base_adjacents:
            return sorted(free_base_adjacents, key=lambda coord: Hex.manhattan_dist(to, coord))

    def closest_enemies(self, tank: Tank) -> List[Tank]:
        # Returns a sorted list by distance of enemy tanks
        tank_idx, tank_coord = tank.player_index, tank.coord
        enemies = [self.__players[player] for player in self.__players if player != tank_idx]
        return sorted((enemy_tank for enemy in enemies for enemy_tank in enemy.tanks),
                      key=lambda enemy_tank: Hex.manhattan_dist(enemy_tank.coord, tank_coord))

    def next_best_available_hex_in_path_to(self, tank: Tank, finish: tuple) -> Union[tuple, None]:
        return self.__path_finding_algorithm(self.__map, tank, finish)