import statistics
from typing import Dict, List

import random as rnd


class Bandit:
    # Shorthand for arms to save on dict size:
    #   S = move to shoot closest enemy, I = camp in base, C = camp close to base
    __arm_shorts = ('S', 'I', 'C')
    __arm_longs = ('shoot_closest_enemy', 'camp_in_base', 'camp_close_to_base')
    __arm_short_long_names = {short: long for short, long in zip(__arm_shorts, __arm_longs)}
    __arm_long_short_names = {long: short for short, long in zip(__arm_shorts, __arm_longs)}
    __arm_num = len(__arm_shorts)

    def __init__(self, name: str, num_turns: int):
        self.__bandit_name = name
        self.__game_arms: List[str] = []
        self.__bandit_Q: Dict[str, List[int]] = {}  # {arm combo name: [list of rewards]}
        self.__num_turns = num_turns

    def get_explore_arms(self) -> tuple:
        return tuple([Bandit.__arm_longs[rnd.randint(0, Bandit.__arm_num-1)] for _ in range(self.__num_turns)])

    def get_exploit_arms(self) -> tuple:
        averages = {arm_combo: statistics.mean(rewards) if rewards else 0 for arm_combo, rewards in
                    self.__bandit_Q.items()}
        best_arm_combo = max(averages, key=averages.get)
        return tuple([Bandit.__arm_short_long_names[arm_short] for arm_short in best_arm_combo])

    def set_bandit_Q(self, bandit_Q: Dict[str, List[int]]) -> None:
        self.__bandit_Q = bandit_Q

    def get_bandit_Q(self) -> Dict[str, List[int]]:
        return self.__bandit_Q

    def register_reward(self, reward: int, game_actions: tuple) -> None:
        arm_combo_name = ''.join([Bandit.__arm_long_short_names[action] for action in game_actions])
        self.__bandit_Q.setdefault(arm_combo_name, []).append(reward)

    def register_turn(self, arm: str) -> None:
        self.__game_arms.append(arm)

# end
