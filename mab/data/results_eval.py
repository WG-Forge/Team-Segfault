from typing import Type

from mab.data.data_io import DataIO

# ResultsTable = player_index: tank_name: action_string: rewards

# ResultsTable = {player_index: {tank_name: {action_combo: rewards}}}
ResultsTable = Type[dict[int, dict[str, list[int]]]]


def results_eval():
    results_table: ResultsTable = DataIO.load_results_table('rnd')

    print(len(results_table[str(0)]))

