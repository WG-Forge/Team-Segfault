import pygame

from map.hex import Hex


class TankDrawer(pygame.sprite.Sprite):
    def __init__(self, tank):
        pygame.sprite.Sprite.__init__(self)
        self.__tank = tank
        # load image
        self.image = pygame.image.load(tank.get_image_path())
        self.image = pygame.transform.scale(self.image, (Hex.radius_x * 1.5, Hex.radius_y * 1.5))
        # color sprite image
        color_image = pygame.Surface(self.image.get_size())
        color_image.fill(tank.get_color())
        self.image.blit(color_image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        self.rect = self.image.get_rect()
        self.rect.center = Hex.make_center(tank.get_coord())

    def update(self, screen) -> None:
        self.rect.center = Hex.make_center(self.__tank.get_coord())
        if self.__tank.get_hp() == 0:
            return
        font_size = round(min(Hex.radius_y, Hex.radius_x))
        font = pygame.font.SysFont('arial', font_size, bold=True)
        text = font.render(str(self.__tank.get_hp()), True, 'white')
        text_rect = text.get_rect(bottomleft=(Hex.make_center(self.__tank.get_coord())[0] + Hex.radius_x / 2,
                                              Hex.make_center(self.__tank.get_coord())[1] + Hex.radius_y / 2))
        screen.blit(text, text_rect)
