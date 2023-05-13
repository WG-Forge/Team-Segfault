import random as rnd
import statistics


class MLTank:
    # Shorthand for arms to save on dict size:
    __actions = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O')
    __action_num = len(__actions)

    def __init__(self, num_rounds: int, group_size: int, can_repair: bool):
        self.__tank_results_table: dict[str, list[int]] = {}  # {arm combo player_name: [list of rewards]}
        self.__game_action_combo: str = ''  # String representing actions taken in this turn
        self.__num_rounds = num_rounds
        self.__group_size: int = group_size
        self.__num_groups: int = num_rounds // group_size
        if self.__num_groups * group_size < num_rounds:
            self.__num_groups += 1

        ''' CHANGE IF MORE REPAIR ACTIONS ADDED, ALWAYS ADD REPAIR ACTIONS TO THE END   '''
        repair_action_num = 5

        if can_repair:
            self.__max_action_index: int = self.__action_num - 1
        else:
            self.__max_action_index: int = self.__action_num - 1 - repair_action_num

    def register_reward(self, reward: int) -> None:
        # If the combination of arms used in this turn has never been used create a new entry in
        # bandit_Q with a string that represents the combination of arms as the key and a list of
        # the rewards associated with this combo. Append this reward to this list.
        action_rewards = self.__tank_results_table.setdefault(self.__game_action_combo, [])
        action_rewards.append(reward)

        # If the list of rewards associated with this arm has more than 20 items, remove the first item
        # such that results when the enemies have not been trained are not taken into account
        if len(action_rewards) > 50:
            action_rewards.pop(0)

    def get_explore_actions(self) -> str:
        # Returns a random set of actions to explore the different probabilities of each
        action_combo = [
            self.__actions[rnd.randint(0, self.__max_action_index)] * self.__group_size
            for _ in range(self.__num_groups)
        ]
        self.__game_action_combo = ''.join(action_combo)
        return self.__game_action_combo

    def get_exploit_actions(self) -> str:
        # Returns a string representing the combination of arms with the highest average reward so far
        averages = {
            arm_combo: statistics.mean(rewards) if rewards else 0
            for arm_combo, rewards in self.__tank_results_table.items()
        }
        return max(averages, key=averages.get)

    def set_results_table(self, results_table: dict[str, list[int]]) -> None:
        self.__tank_results_table = results_table

    def get_results_table(self) -> dict[str, list[int]]: return self.__tank_results_table
