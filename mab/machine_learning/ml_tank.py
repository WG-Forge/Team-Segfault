import random as rnd
import statistics


class MLTank:
    # Shorthand for arms to save on dict size:
    __actions = ('A', 'B', 'C', 'D', 'E', 'F')
    __action_num = len(__actions)

    def __init__(self, num_rounds: int, group_size: int):
        self.__num_rounds = num_rounds
        self.__group_size: int = group_size
        self.__num_groups: int = num_rounds // group_size
        if self.__num_groups * group_size < num_rounds:
            self.__num_groups += 1

    def get_explore_actions(self) -> str:
        # Returns a random set of actions to explore the different probabilities of each
        action_combo = [
            self.__actions[rnd.randint(0, self.__action_num-1)] * self.__group_size
            for _ in range(self.__num_groups)
        ]
        return ''.join(action_combo)

