from typing import Type

from mab.data.data_io import DataIO

# ResultsTable = player_index: tank_name: action_string: rewards

# ResultsTable = {player_index: {tank_name: {action_combo: rewards}}}
ResultsTable = Type[dict[int, dict[str, list[int]]]]


def results_eval():
    actions = ('A', 'B', 'C', 'D', 'E', 'F', 'G')

    actions_by_reward_sum_and_num = {
        'A': [0, 0], 'B': [0, 0], 'C': [0, 0], 'D': [0, 0], 'E': [0, 0], 'F': [0, 0], 'G': [0, 0]
    }

    results_table: ResultsTable = DataIO.load_results_table('rnd')

    print(len(results_table[str(0)]))
