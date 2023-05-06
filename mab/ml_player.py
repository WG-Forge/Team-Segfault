import random as rnd

from mab.ml_tank import MLTank


class MLPlayer:
    __tank_names_can_repair = {
        'spg': False, 'light_tank': False, 'heavy_tank': True, 'medium_tank': True, 'at_spg': True
    }

    def __init__(self, num_turns: int, group_size: int):
        self.__tanks: dict[str, MLTank] = self.make_tanks(num_turns, group_size)

    def make_tanks(self, num_turns: int, group_size: int) -> dict[str, MLTank]:
        return {
            name: MLTank(num_turns, group_size, can_repair)
            for name, can_repair in self.__tank_names_can_repair.items()
        }

    def register_reward(self, reward: int) -> None:
        for bandit in self.__tanks.values():
            bandit.register_reward(reward)

    def get_game_actions(self, explore_prob: float) -> dict[str, str]:
        exploring = rnd.random() < explore_prob
        actions = {
            name: (bandit.get_explore_actions() if exploring else bandit.get_exploit_actions())
            for name, bandit in self.__tanks.items()
        }
        return actions

    def set_results_table(self, player_results_table: dict[str, dict[str, list[int]]]) -> None:
        for tank_name, tank_results_table in player_results_table.items():
            self.__tanks[tank_name].set_results_table(tank_results_table)

    def get_results_table(self) -> dict[str, list[int]]:
        return {
            name: tank.get_results_table()
            for name, tank in self.__tanks.items()
        }
