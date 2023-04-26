import statistics
from typing import Dict, List, Tuple

import random as rnd


class Bandit:
    # Shorthand for arms to save on dict size:
    __arms = ('A', 'B', 'C', 'D', 'E')
    __arm_num = len(__arms)

    def __init__(self, num_turns: int):
        self.__bandit_Q: Dict[str, List[int]] = {}  # {arm combo name: [list of rewards]}
        self.__game_arms: str = ''  # String representing arms used in this turn
        self.__num_turns = num_turns

    def register_reward(self, reward: int) -> None:
        # If the combination of arms used in this turn has never been used create a new entry in
        # bandit_Q with a string that represents the combination of arms as the key and a list of
        # the rewards associated with this combo. Append this reward to this list.
        arm_rewards = self.__bandit_Q.setdefault(self.__game_arms, [])
        arm_rewards.append(reward)

        # If the list of rewards associated with this arm has more than 20 items, remove the first item
        # such that results when the enemies have not been trained are not taken into account
        if len(arm_rewards) > 20:
            arm_rewards.pop(0)

    def get_explore_arms(self) -> str:
        # Returns a random set of arms to explore the different probabilities of each arm
        arm_combo = [Bandit.__arms[rnd.randint(0, Bandit.__arm_num - 1)] for _ in range(self.__num_turns)]
        self.__game_arms = ''.join(arm_combo)
        return self.__game_arms

    def get_exploit_arms(self) -> tuple:
        # Returns a string representing the combination of arms with the highest average reward so far
        averages = {arm_combo: statistics.mean(rewards) if rewards else 0 for arm_combo, rewards in
                    self.__bandit_Q.items()}
        return max(averages, key=averages.get)

    def set_bandit_Q(self, bandit_Q: Dict[str, List[int]]) -> None: self.__bandit_Q = bandit_Q

    def get_bandit_Q(self) -> Dict[str, List[int]]: return self.__bandit_Q
