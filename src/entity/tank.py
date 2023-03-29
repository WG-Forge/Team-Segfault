from src.entity.entity import Entity
from src.map.hex import Hex


class Tank(Entity):
    def __init__(self, tank_id: int, tank_info: dict):
        # tank_info = json.loads(tank_info)
        self.__tank_id = tank_id
        self.__hp: int = tank_info["health"]
        # change this when they give us info for other vehicle types
        self.__sp: int = 2
        self.__tank_type: str = tank_info["vehicle_type"]
        self.__spawn_coordinate: Hex = Hex([tank_info["position"]["x"],
                                            tank_info["position"]["y"],
                                            tank_info["position"]["z"]])
        self.__capture_points = tank_info["capture_points"]
        super().__init__(self.__tank_type)

    def reset(self) -> None:
        self.__hp = 2

    def update(self, hp: int, capture_pts: int):
        self.__hp = hp
        self.__capture_points = capture_pts
