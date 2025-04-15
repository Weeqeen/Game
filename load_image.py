import pygame


pygame.init()
pygame.display.set_mode((1, 1))


def load_image(name, scale_factor):
    image = pygame.image.load(name).convert_alpha()
    return pygame.transform.scale(image,
                                  (int(image.get_width() * scale_factor), int(image.get_height() * scale_factor)))