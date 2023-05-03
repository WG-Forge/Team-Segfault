from enum import StrEnum


class LocalEntities(StrEnum):
    # local_tanks
    LIGHT_TANK = 'light_tank'
    MEDIUM_TANK = 'medium_tank'
    HEAVY_TANK = 'heavy_tank'
    TANK_DESTROYER = 'at_spg'
    ARTILLERY = 'spg'

    # features
    EMPTY = 'empty'
    OBSTACLE = 'obstacle'
    BASE = 'base'
    SPAWN = 'spawn_points'
    LIGHT_REPAIR = 'light_repair'
    HARD_REPAIR = 'hard_repair'
    CATAPULT = 'catapult'
