import pygame
from load_image import load_image


pygame.init()

platform_ = pygame.image.load("Sprites\\tile.png")
GREEN_GROUND = (0, 200, 0)



class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.blit(platform_, (0,0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Platform_Ground(Platform):
    def __init__(self, x, y, width, height, sprite_path):
        super().__init__(x, y, width, height)
        self.image = pygame.image.load(sprite_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class FinishSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(image_path, 0.2)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
