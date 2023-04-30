import pygame

from constants import BULLET_IMAGE_PATH, BULLET_SOUND, SOUND_VOLUME, HEX_RADIUS_X, HEX_RADIUS_Y


class Projectile(pygame.sprite.Sprite):
    __bullet_travel_time = 5
    __IMAGE = pygame.image.load(BULLET_IMAGE_PATH)

    def __init__(self, start_pos: tuple[int, int], end_pos: tuple[int, int], color: tuple[int, int, int] | str):
        super().__init__()

        self.shot_vector = (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])
        self.start_pos = start_pos

        self.image = Projectile.__IMAGE
        # rotate bullet so it is pointing to end_pos
        angle = pygame.Vector2(1, 0).angle_to(pygame.Vector2(self.shot_vector))
        angle = -angle
        self.image = pygame.transform.rotate(self.image, angle)
        self.image = pygame.transform.scale(self.image, (HEX_RADIUS_X[0] / 2, HEX_RADIUS_Y[0] / 2))
        # color the bullet
        color_image = pygame.Surface(self.image.get_size())
        color_image.fill(color)
        self.image.blit(color_image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        self.rect = self.image.get_rect()
        self.rect.center = start_pos

        # animation variables
        self.counter = 0
        self.step = 1 / Projectile.__bullet_travel_time

        # sound
        self.__sound = pygame.mixer.Sound(BULLET_SOUND)
        self.__sound.set_volume(SOUND_VOLUME[0])
        self.__sound_played = False

    def update(self) -> None:
        if self.__sound_played is False:
            self.__sound.play()
            self.__sound_played = True
        self.counter += int(self.step)

        if self.counter >= 1:
            self.kill()

        x, y = self.start_pos
        self.rect.center = (x + self.counter * self.shot_vector[0], y + self.counter * self.shot_vector[1])

    @staticmethod
    def get_travel_time():
        return Projectile.__bullet_travel_time
