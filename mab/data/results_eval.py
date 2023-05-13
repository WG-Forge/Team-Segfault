from mab.data.data_io import DataIO

# ResultsTable = player_index: tank_name: action_string: rewards

def results_eval():
    results_table = DataIO.load_results_table('one_action')
    actions_by_reward_sum_and_num = {
        'A': [0, 0], 'B': [0, 0], 'C': [0, 0], 'D': [0, 0], 'E': [0, 0], 'F': [0, 0], 'G': [0, 0]
    }

    for player_dict in results_table.values():
        for name, tank_dict in player_dict.items():
            print(name, end=': ')
            for actions, rewards in tank_dict.items():
                if len(actions) < 1:
                    continue
                action = actions[0]
                reward_sum = sum(rewards)
                actions_by_reward_sum_and_num[action][0] += reward_sum
                actions_by_reward_sum_and_num[action][1] += len(rewards)

                print(action, round((reward_sum/len(rewards))*100, 0), end=', ')
            print()
        print()

    print('Overall averages:')
    for action, reward_and_sum in actions_by_reward_sum_and_num.items():
        average_reward = round(((reward_and_sum[0] / reward_and_sum[1]) * 100), 0)
        print(action, average_reward)
