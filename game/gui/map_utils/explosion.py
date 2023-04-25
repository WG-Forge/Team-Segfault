import pygame

from constants import SOUND_VOLUME, EXPLOSION_IMAGES, EXPLOSION_SOUND


class Explosion(pygame.sprite.Sprite):
    __images = [pygame.image.load(path) for path in EXPLOSION_IMAGES]
    __fist_call = True

    def __init__(self, coord: tuple[int, int], scale_x: float, scale_y: float):
        pygame.sprite.Sprite.__init__(self)

        # scale images if this is a first call (scaling cannot be done before pygame is initialized
        if Explosion.__fist_call:
            for i in range(len(Explosion.__images)):
                Explosion.__images[i] = pygame.transform.scale(Explosion.__images[i], (scale_x, scale_y))
            Explosion.__fist_call = False

        # image index
        self.index = 0
        # animation counter
        self.counter = 0
        self.image = Explosion.__images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [coord[0], coord[1]]
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

        if self.counter >= explosion_speed and self.index < len(Explosion.__images) - 1:
            self.counter = 0
            self.index += 1
            self.image = Explosion.__images[self.index]

        if self.index >= len(Explosion.__images) - 1 and self.counter >= explosion_speed:
            self.kill()
