import pygame

from consts import SOUND_MUTED, SOUND_VOLUME


class Explosion(pygame.sprite.Sprite):
    def __init__(self, coord: (int, int), scale_x, scale_y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for i in range(7):
            img = pygame.image.load(f'assets/explosion/{i}.png')
            img = pygame.transform.scale(img, (scale_x, scale_y))
            self.images.append(img)

        # image index
        self.index = 0
        # animation counter
        self.counter = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [coord[0], coord[1]]
        # used for delaying explosion if the bullet is too slow; should not be delayed when turns are fast
        # self.delay = explosion_delay

        self.__sound = pygame.mixer.Sound('assets/sounds/explosion.mp3')
        self.__sound.set_volume(SOUND_VOLUME)
        self.__sound_played = SOUND_MUTED

    def update(self):
        # if self.delay >= 0:
        #     self.delay -= 1
        #     return

        if self.__sound_played is False:
            self.__sound.play()
            self.__sound_played = True

        explosion_speed = 3
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()
