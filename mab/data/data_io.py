import json
from typing import Type


class DataIO:
    __results_table_path = "mab\\data\\training_data\\results_table.json"
    __num_games_path = "mab\\data\\training_data\\num_games.json"
    __best_actions_path = "mab\\data\\training_data\\best_actions.json"
    __client_map_path = "mab\\data\\server_data\\client_map.json"
    __game_state_path = "mab\\data\\server_data\\game_state.json"

    ResultsTable = Type[dict[int, dict[str, dict[str, list[int]]]]]
    GameActions = Type[dict[int, dict[str, str]]]

    """     FORMATTING      """

    @staticmethod
    def __format_game_state(game_state: dict) -> dict:
        idx_by_index: dict[int, int] = {}
        index: int = 0
        for player_dict in game_state['players']:
            idx = player_dict.get('idx')
            if idx not in idx_by_index:
                idx_by_index[idx] = index
                index += 1
            player_dict[idx] = index

        for vehicle_dict in game_state['vehicles'].values():
            vehicle_dict['player_id'] = idx_by_index[vehicle_dict['player_id']]

        return game_state

    """     SAVING      """

    @staticmethod
    def __save(what, where: str) -> None:
        with open(where, 'w') as file:
            json.dump(what, file)

    @staticmethod
    def save_best_actions(best_actions: GameActions) -> None: DataIO.__save(best_actions, DataIO.__best_actions_path)

    @staticmethod
    def save_client_map(client_map: dict) -> None: DataIO.__save(client_map, DataIO.__client_map_path)

    @staticmethod
    def save_game_state(game_state: dict) -> None:
        game_state = DataIO.__format_game_state(game_state)
        DataIO.__save(game_state, DataIO.__game_state_path)

    @staticmethod
    def save_results_table(results_table: ResultsTable) -> None: DataIO.__save(results_table, DataIO.__results_table_path)

    @staticmethod
    def save_num_games(num_games: int) -> None: DataIO.__save(num_games, DataIO.__num_games_path)

    """     LOADING     """

    @staticmethod
    def __load(from_where: str):
        with open(from_where, 'r') as file:
            what = json.load(file)
        return what

    @staticmethod
    def load_client_map() -> dict: return DataIO.__load(DataIO.__client_map_path)

    @staticmethod
    def load_game_state() -> dict: return DataIO.__load(DataIO.__game_state_path)

    @staticmethod
    def load_results_table() -> ResultsTable: return DataIO.__load(DataIO.__results_table_path)

    @staticmethod
    def load_num_games() -> int: return DataIO.__load(DataIO.__num_games_path)

    @staticmethod
    def load_best_actions() -> dict[str, dict[str, str]]: return DataIO.__load(DataIO.__best_actions_path)
