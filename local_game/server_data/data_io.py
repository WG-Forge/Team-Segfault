import json


dir_path = 'local_game\\server_data\\'

def load_server_map() -> dict:
    with open(dir_path + 'server_map.json', 'r') as f:
        server_map = json.load(f)
    return server_map


def load_game_state() -> dict:
    with open(dir_path + 'game_state.json', 'r') as f:
        game_state = json.load(f)
    return game_state


def save_server_map(server_map: dict):
    with open(dir_path + 'server_map.json', 'w') as f:
        json.dump(server_map, f)


def save_game_state(game_state: dict):
    with open(dir_path + 'game_state.json', 'w') as f:
        json.dump(game_state, f)
