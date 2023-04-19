import pygame


class Explosion(pygame.sprite.Sprite):
    def __init__(self, coord: (int, int), scale_x, scale_y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for i in range(7):
            img = pygame.image.load(f'game/assets/explosion/{i}.png')
            img = pygame.transform.scale(img, (scale_x, scale_y))
            self.images.append(img)

        self.index = 0
        self.counter = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.topleft = [coord[0], coord[1]]

    def update(self):
        explosion_speed = 10
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()
