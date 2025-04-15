import pygame
import random
from load_image import load_image
from Game_loop import game_loop


WIDTH, HEIGHT = 1024, 650
SKY = (135, 206, 235)
FONT_COLOR = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Jump 'n' Run")
font = pygame.font.SysFont(None, 48)


def draw_text(text, font, surface, x, y):
    textobj = font.render(text, True, FONT_COLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def draw_button(text, font, surface, x, y, width, height, action=None):
    pygame.draw.rect(surface, (0, 100, 0), (x, y, width, height))
    draw_text(text, font, surface, x + 10, y + 10)

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        if click[0] == 1 and action is not None:
            action()

def main_menu():
    while True:
        screen.fill(SKY)
        draw_text('  Главное меню', font, screen, WIDTH // 2 - 100, HEIGHT // 4)

        draw_button('   Новая игра', font, screen, WIDTH // 2 - 100, HEIGHT // 2, 257, 50, lambda: game_loop(level=1))

        draw_button('Покинуть игру', font, screen, WIDTH // 2 - 100, HEIGHT // 2 + 60, 257, 50, pygame.quit)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.flip()


def reset_game():
    global level
    level = 1
    game_loop(level)

main_menu()