import heapq
from typing import Union

from entities.map_features.Landmarks.obstacle import Obstacle
from entities.map_features.Landmarks.spawn import Spawn
from entities.tanks.tank import Tank
from game_map.hex import Hex


def a_star(game_map: dict, tank: Tank, finish: tuple) -> Union[tuple, None]:
    start, tank_id, speed = tank.coord, tank.tank_id, tank.speed
    passable_obstacles = []
    cnt = 0

    while cnt < 25:
        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {}
        cost_so_far = {start: 0}
        came_from[start] = None
        while frontier:
            current = heapq.heappop(frontier)[1]
            if current == finish:
                break
            for movement in Hex.moves:
                coord = Hex.coord_sum(current, movement)
                entities = game_map.get(coord)
                if entities and not (isinstance(entities['feature'], Obstacle) or coord in passable_obstacles):
                    new_cost = cost_so_far[current] + 1
                    if coord not in cost_so_far or new_cost < cost_so_far[coord]:
                        cost_so_far[coord] = new_cost
                        priority = new_cost + Hex.manhattan_dist(finish, coord)
                        heapq.heappush(frontier, (priority, coord))
                        came_from[coord] = current
        path = []
        current = finish
        while current != start:
            path.append(current)
            if current not in came_from:
                return None
            current = came_from[current]
        path.append(start)
        path.reverse()
        next_best = path[min(speed, len(path) - 1)]

        # If next_best is a tank or base, append to passable_obstacles and try again
        if _is_others_spawn(game_map, next_best, tank_id) or game_map[next_best]['tank']:
            passable_obstacles.append(next_best)
            cnt += 1
            continue
        else:
            return next_best


# Protected member of module starts with underscore
def _is_others_spawn(game_map: dict, spawn_coord: tuple, tank_id: int) -> bool:
    # If the feature at spawn_coord is a spawn object and it does not belong to the tank with tank_id return True
    feature = game_map[spawn_coord]['feature']
    if isinstance(feature, Spawn):
        if feature.get_belongs_id() != tank_id:
            return True
    return False
