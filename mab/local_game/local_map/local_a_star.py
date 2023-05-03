import heapq

from local_entities.local_map_features.local_landmarks.local_obstacle import LocalObstacle
from local_entities.local_map_features.local_landmarks.local_spawn import LocalSpawn
from local_entities.local_tanks.local_tank import LocalTank
from local_map.local_hex import LocalHex


def local_a_star(game_map: dict, tank: LocalTank, finish: tuple) -> tuple | None:
    start, tank_id, speed = tank.coord, tank.tank_id, tank.speed
    passable_obstacles = []
    cnt = 0

    while cnt < 25:
        frontier: list[tuple] = []
        heapq.heappush(frontier, (0, start))
        came_from: dict[tuple, tuple | None] = {}
        cost_so_far = {start: 0}
        came_from[start] = None
        while frontier:
            current = heapq.heappop(frontier)[1]
            if current == finish:
                break
            for movement in LocalHex.moves:
                coord = LocalHex.coord_sum(current, movement)
                entities = game_map.get(coord)
                if entities and not (isinstance(entities['feature'], LocalObstacle) or coord in passable_obstacles):
                    new_cost = cost_so_far[current] + 1
                    if coord not in cost_so_far or new_cost < cost_so_far[coord]:
                        cost_so_far[coord] = new_cost
                        priority = new_cost + LocalHex.manhattan_dist(finish, coord)
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

    return None


# Protected member of module starts with underscore
def _is_others_spawn(game_map: dict, spawn_coord: tuple, tank_id: int) -> bool:
    # If the feature at spawn_coord is a spawn object and it does not belong to the tank with tank_id return True
    feature = game_map[spawn_coord]['feature']
    if isinstance(feature, LocalSpawn):
        if feature.get_belongs_id() != tank_id:
            return True
    return False
