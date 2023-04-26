import random as rnd
from typing import Dict, List

from mab.tank import Tank


class Player:
    __tank_names = ('spg', 'light_tank', 'heavy_tank', 'medium_tank', 'at_spg')

    def __init__(self, num_turns: int):
        self.__tanks = {name: Tank(num_turns) for name in Player.__tank_names}

    def register_reward(self, reward: int) -> None:
        for bandit in self.__tanks.values():
            bandit.register_reward(reward)

    def get_game_actions(self, explore_prob: float) -> Dict[str, str]:
        exploring = rnd.random() < explore_prob
        actions = {
            name: (bandit.get_explore_actions() if exploring else bandit.get_exploit_actions())
            for name, bandit in self.__tanks.items()
        }
        return actions

    def set_results_table(self, player_results_table: Dict[str, List[int]]) -> None:
        for tank_name, tank_results_table in player_results_table.items():
            self.__tanks[tank_name].set_results_table(tank_results_table)

    def get_results_table(self) -> Dict[str, List[int]]:
        return {name: tank.get_results_table() for name, tank in self.__tanks.items()}
