# display consts
FPS_MAX = 30  # max frames per second
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PLAYER1_COLOR = (224, 206, 70)  # yellow
PLAYER2_COLOR = (70, 191, 224)  # blue
PLAYER3_COLOR = (201, 26, 40)  # red
BASE_COLOR = (39, 161, 72)
EMPTY_COLOR = (87, 81, 81)
OBSTACLE_COLOR = (51, 46, 46)
DEFAULT_SPAWN_COLOR = (135, 126, 126)

# sound options
SOUND_MUTED = False
SOUND_VOLUME = 0.1

# sound paths
EXPLOSION_SOUND = 'game/assets/sounds/explosion.mp3'
BULLET_SOUND = 'game/assets/sounds/shot.mp3'

# menu constants
MENU_FONT = 'game/assets/menu/8-BIT WONDER.TTF'

# image paths
SPG_IMAGE_PATH = 'game/assets/tank_classes/spg.png'
HT_IMAGE_PATH = 'game/assets/tank_classes/ht.png'
LT_IMAGE_PATH = 'game/assets/tank_classes/lt.png'
MT_IMAGE_PATH = 'game/assets/tank_classes/mt.png'
TD_IMAGE_PATH = 'game/assets/tank_classes/td.png'
EXPLOSION_IMAGES = [f'game/assets/explosion/{i}.png' for i in range(7)]
BULLET_IMAGE = 'game/assets/white_bullet.png'
