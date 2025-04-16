import pygame
import sys
from load_image import load_image
from Game_loop import game_loop


WIDTH, HEIGHT = 1024, 650
SKY = (135, 206, 235)
FONT_COLOR = (255, 255, 255)
BUTTON_COLOR = (0, 102, 204)
BUTTON_HOVER_COLOR = (0, 153, 255)
FONT_SIZE = 40
BUTTON_FONT_SIZE = 30
clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((1024, 650), pygame.FULLSCREEN)
pygame.display.set_caption("Jump 'n' Run")
font = pygame.font.SysFont(None, 48)
button_font = pygame.font.Font(None, BUTTON_FONT_SIZE)


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


def draw_button(text, font, surface, x, y, width, height, action=None):
    """Рисует кнопку и обрабатывает её нажатие"""
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    button_color = BUTTON_HOVER_COLOR if x < mouse_pos[0] < x + width and y < mouse_pos[1] < y + height else BUTTON_COLOR

    pygame.draw.rect(surface, button_color, (x, y, width, height))
    draw_text(text, font, FONT_COLOR, surface, x + width // 2, y + height // 2)

    if button_color == BUTTON_HOVER_COLOR and mouse_click[0] and action:
        action()


def level_menu():
    """Меню выбора уровня"""
    running = True
    while running:
        screen.fill(SKY)

        draw_text('Выбор уровня', font, FONT_COLOR, screen, WIDTH // 2, HEIGHT // 4)

        for i in range(1, 6):
            # Создаем лямбда-функцию с явным параметром lvl=i
            draw_button(f'Уровень {i}', button_font, screen,
                       WIDTH // 2 - 130, HEIGHT // 2 - 120 + (i - 1) * 70,
                       260, 60,
                       action=lambda lvl=i: game_loop(lvl))  # Используем lvl вместо i

        draw_button('Назад', button_font, screen, WIDTH // 2 - 130, HEIGHT // 2 + 250, 260, 60, action=main_menu)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        pygame.display.flip()
        clock.tick(60)


def quit_game():
    pygame.quit()
    sys.exit()


def main_menu():
    running = True
    while running:
        screen.fill(SKY)

        draw_text('Главное меню', font, FONT_COLOR, screen, WIDTH // 2, HEIGHT // 4)

        draw_button('Новая игра', button_font, screen, WIDTH // 2 - 130, HEIGHT // 2 - 50, 260, 60,
                    lambda: game_loop(level=1))

        draw_button('Выбор уровня', button_font, screen, WIDTH // 2 - 130, HEIGHT // 2 + 50, 260, 60, level_menu)

        draw_button('Выход', button_font, screen, WIDTH // 2 - 130, HEIGHT // 2 + 150, 260, 60, quit_game)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        pygame.display.flip()
        clock.tick(60)


def reset_game():
    global level
    level = 1
    game_loop(level)

main_menu()
