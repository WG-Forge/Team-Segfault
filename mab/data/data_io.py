import json
from typing import Type


class DataIO:
    __results_table_path = "mab\\data\\training_data\\results_table.json"
    __num_games_path = "mab\\data\\training_data\\num_games.json"
    __client_map_path = "mab\\data\\server_data\\client_map.json"
    __game_state_path = "mab\\data\\server_data\\game_state.json"
    ResultsTable = Type[dict[int, dict[str, dict[str, list[int]]]]]
    GameActions = Type[dict[int, dict[str, str]]]

    """     SAVING      """

    @staticmethod
    def __save(what, where: str) -> None:
        with open(where, 'w') as file:
            json.dump(what, file)

    @staticmethod
    def save_client_map(client_map) -> None: DataIO.__save(client_map, DataIO.__client_map_path)

    @staticmethod
    def save_game_state(game_state) -> None: DataIO.__save(game_state, DataIO.__game_state_path)

    @staticmethod
    def save_results_table(results_table: ResultsTable) -> None: DataIO.__save(results_table, DataIO.__results_table_path)

    @staticmethod
    def save_num_games(explore_prob, max_explore_prob, decay_per_game) -> None:
        num_games = int((max_explore_prob - explore_prob) / decay_per_game)
        DataIO.__save(num_games, DataIO.__num_games_path)

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
