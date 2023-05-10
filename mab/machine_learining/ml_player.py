import random as rnd

from mab.machine_learining.ml_tank import MLTank


class MLPlayer:
    __tank_names_can_repair = {
        'spg': False, 'light_tank': False, 'heavy_tank': True, 'medium_tank': True, 'at_spg': True
    }

    __max_explore_prob = 1.0  # Maximum exploration probability -> 100 %
    __min_explore_prob = 0.03  # Minimum exploration probability -> 3 %
    __decay_per_game = 0.00001  # Minimum exploration ratio reached after about 100 000 games

    def __init__(self, num_turns: int, group_size: int):
        self.__tanks: dict[str, MLTank] = self.__make_tanks(num_turns, group_size)
        self.__explore_prob: float = self.__max_explore_prob

    def update_exploring(self) -> None:
        if self.__explore_prob > self.__min_explore_prob:
            self.__explore_prob -= self.__decay_per_game

    def __make_tanks(self, num_turns: int, group_size: int) -> dict[str, MLTank]:
        return {
            name: MLTank(num_turns, group_size, can_repair)
            for name, can_repair in self.__tank_names_can_repair.items()
        }

    def register_reward(self, reward: int) -> None:
        for bandit in self.__tanks.values():
            bandit.register_reward(reward)

    def get_exploit_actions(self) -> dict[str, str]:
        return {
            name: tank.get_exploit_actions()
            for name, tank in self.__tanks.items()
        }

    def get_explore_actions(self) -> dict[str, str]:
        return {
            name: tank.get_explore_actions()
            for name, tank in self.__tanks.items()
        }

    def get_game_actions(self) -> dict[str, str]:
        return self.get_explore_actions() if rnd.random() < self.__explore_prob else self.get_exploit_actions()

    def get_results_table(self) -> dict[str, list[int]]:
        return {
            name: tank.get_results_table()
            for name, tank in self.__tanks.items()
        }

    def set_results_table(self, player_results_table: dict[str, dict[str, list[int]]]) -> None:
        for tank_name, tank_results_table in player_results_table.items():
            self.__tanks[tank_name].set_results_table(tank_results_table)

    def set_explore_prob(self, num_games: int) -> None:
        self.__explore_prob = self.__calc_explore_prob(num_games)

    @staticmethod
    def __calc_explore_prob(num_games: int) -> float:
        total_decay = MLPlayer.__decay_per_game * num_games
        return float(1 - total_decay)
