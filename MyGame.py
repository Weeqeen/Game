import pygame
import sys
from load_image import load_image
from Game_loop import game_loop, random_level
from Small_func import quit_game, reset_game
from Draw_t_and_b import draw_text, draw_button


WIDTH, HEIGHT = 1024, 650
SKY = (135, 206, 235)
FONT_COLOR = (255, 255, 255)
FONT_SIZE = 40
BUTTON_FONT_SIZE = 30
clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((1024, 650), pygame.FULLSCREEN)
pygame.display.set_caption("Jump 'n' Run")
font = pygame.font.SysFont(None, 48)
button_font = pygame.font.Font(None, BUTTON_FONT_SIZE)



def Run():
    running = True
    while running:
        screen.fill(SKY)

        draw_text('Главное меню', font, FONT_COLOR, screen, WIDTH // 2, HEIGHT // 4)

        draw_button('Новая игра', button_font, screen, WIDTH // 2 - 130, HEIGHT // 2 - 50, 260, 60,
                    lambda: game_loop(level=1))

        draw_button('Рандомный уровень', button_font, screen, WIDTH // 2 - 130, HEIGHT // 2 + 50, 260, 60, random_level)

        draw_button('Выход', button_font, screen, WIDTH // 2 - 130, HEIGHT // 2 + 150, 260, 60, quit_game)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        pygame.display.flip()
        clock.tick(60)
