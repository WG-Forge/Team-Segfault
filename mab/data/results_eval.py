from typing import Type

from mab.data.data_io import DataIO

# ResultsTable = player_index: tank_name: action_string: rewards

# ResultsTable = {player_index: {tank_name: {action_combo: rewards}}}
ResultsTable = Type[dict[int, dict[str, dict[str, list[int]]]]]


def results_eval():
    actions = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O')
    no_repair_actions = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J')

    tank_names_can_repair = {
        'spg': False, 'light_tank': False, 'heavy_tank': True, 'medium_tank': True, 'at_spg': True
    }

    actions_by_reward_sum_and_num = {
        'A': [0, 0], 'B': [0, 0], 'C': [0, 0], 'D': [0, 0], 'E': [0, 0], 'F': [0, 0], 'G': [0, 0], 'H': [0, 0],
        'I': [0, 0], 'J': [0, 0], 'K': [0, 0], 'L': [0, 0], 'M': [0, 0], 'N': [0, 0], 'O': [0, 0]
    }

    action_sum_num = {action: [0, 0] for action in no_repair_actions}
    repair_action_sum_num = {action: [0, 0] for action in actions}

    tank_by_sum = {tank_name: repair_action_sum_num if tank_names_can_repair[tank_name] else action_sum_num
                   for tank_name in tank_names_can_repair}

    results_sums = {player_index: tank_by_sum for player_index in range(3)}

    results_table: ResultsTable = DataIO.load_results_table('many_actions')

    for player_index, player_dict in results_table.items():
        for tank_name, tank_dict in player_dict.items():
            for actions, rewards in tank_dict.items():
                if len(actions) < 1:
                    continue

                action = actions[0]
                reward_sum = sum(rewards)

                results_sums[int(player_index)][tank_name][action][0] += reward_sum
                results_sums[int(player_index)][tank_name][action][1] += len(rewards)

                actions_by_reward_sum_and_num[action][0] += reward_sum
                actions_by_reward_sum_and_num[action][1] += len(rewards)

    print('Overall averages:')
    for action, reward_and_sum in actions_by_reward_sum_and_num.items():
        try:
            average_reward = round(((reward_and_sum[0] / reward_and_sum[1]) * 100), 0)
            print(action, average_reward)
        except Exception as e:
            print(e)

    print('Specific Averages')
    for player_index, player_dict in results_sums.items():
        print('Player:', player_index)
        for tank_name, tank_dict in player_dict.items():
            print(tank_name, end='')
            for action, sum_num in tank_dict.items():
                try:
                    average_reward = int((sum_num[0] / sum_num[1]) * 100)
                    print(action, average_reward, end=', ')
                except Exception as e:
                    print(e)
            print()
        print()

