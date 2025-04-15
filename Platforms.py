import pygame
from load_image import load_image


pygame.init()

PLATFORM_COLOR = (50, 150, 50)
GREEN_GROUND = (0, 200, 0)


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(PLATFORM_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Platform_Ground(Platform):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.image.fill(GREEN_GROUND)


class FinishSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(image_path, 0.1)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y