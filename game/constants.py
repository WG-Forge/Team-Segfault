# server info
HOST_NAME = "wgforge-srv.wargaming.net"
HOST_PORT = 443

# gui constants
FPS_MAX = 30  # max frames per second
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# this is reduced when on game start
HEX_RADIUS_X = [SCREEN_WIDTH]
HEX_RADIUS_Y = [SCREEN_HEIGHT]

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GAME_BACKGROUND = (47, 31, 128)
PLAYER1_COLOR = (224, 206, 70)  # yellow
PLAYER2_COLOR = (70, 191, 224)  # blue
PLAYER3_COLOR = (201, 26, 40)  # red
BASE_COLOR = (39, 161, 72)
EMPTY_COLOR = (87, 81, 81)
OBSTACLE_COLOR = (51, 46, 46)
DEFAULT_SPAWN_COLOR = (135, 126, 126)

# player names
PLAYER1_NAME = ['Playa']

# sound options
SOUND_VOLUME = [0.0]

# sound paths
EXPLOSION_SOUND = 'game/assets/sounds/explosion.mp3'
BULLET_SOUND = 'game/assets/sounds/shot.mp3'

# image paths
TANK_ICON_PATH = 'game/assets/tank_icon.png'
SPG_IMAGE_PATH = 'game/assets/tank_classes/spg.png'
HT_IMAGE_PATH = 'game/assets/tank_classes/ht.png'
LT_IMAGE_PATH = 'game/assets/tank_classes/lt.png'
MT_IMAGE_PATH = 'game/assets/tank_classes/mt.png'
TD_IMAGE_PATH = 'game/assets/tank_classes/td.png'

FLAG_PATH = 'game/assets/flag.png'
EXPLOSION_IMAGES = [f'game/assets/explosion/{i}.png' for i in range(7)]
BULLET_IMAGE_PATH = 'game/assets/white_bullet.png'
