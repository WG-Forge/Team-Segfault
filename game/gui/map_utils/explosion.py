import pygame

from constants import SOUND_VOLUME, EXPLOSION_IMAGES, EXPLOSION_SOUND, HEX_RADIUS_X, HEX_RADIUS_Y


class Explosion(pygame.sprite.Sprite):
    __IMAGES = [pygame.image.load(path) for path in EXPLOSION_IMAGES]

    def __init__(self, coord: tuple[int, int]):
        super().__init__()

        # image index
        self.index = 0
        # animation counter
        self.counter = 0
        self.image = Explosion.__IMAGES[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (coord[0], coord[1])

        # used for delaying explosion if the bullet is too slow; should not be delayed when turns are fast
        # self.delay = explosion_delay

        self.__sound = pygame.mixer.Sound(EXPLOSION_SOUND)
        self.__sound.set_volume(SOUND_VOLUME[0])
        self.__sound_played = False

    def update(self):
        # if self.delay >= 0:
        #     self.delay -= 1
        #     return

        if self.__sound_played is False:
            self.__sound.play()
            self.__sound_played = True

        explosion_speed = 3
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(Explosion.__IMAGES) - 1:
            self.counter = 0
            self.index += 1
            self.image = Explosion.__IMAGES[self.index]

        if self.index >= len(Explosion.__IMAGES) - 1 and self.counter >= explosion_speed:
            self.kill()

    @staticmethod
    def set_image_scale():
        for i in range(len(Explosion.__IMAGES)):
            Explosion.__IMAGES[i] = pygame.transform.scale(Explosion.__IMAGES[i],
                                                           (HEX_RADIUS_X[0] * 2, HEX_RADIUS_Y[0] * 2))
