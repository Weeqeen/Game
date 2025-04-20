import pygame
from Small_func import quit_game
from Player import Player
from numpy.random.mtrand import randint
from Platforms import Platform, Platform_Ground, FinishSprite
from Draw_t_and_b import draw_text, draw_button


pygame.init()
WIDTH, HEIGHT = 1024, 650
bg = pygame.image.load("Sprites\\layer-1.png")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT+50 ))
font = pygame.font.SysFont(None, 48)
FONT_COLOR = (255, 255, 255)
level = 1
screen = pygame.display.set_mode((1024, 650))


def random_level():
    level = randint(1,6)
    return game_loop(level)


def end_menu():
    """Меню завершения игры после 5 уровня"""
    clock = pygame.time.Clock()  # Инициализируем clock внутри функции
    running = True
    while running:
        screen.blit(bg, (0, 0))

        draw_text('Поздравляем, вы прошли игру!', font, FONT_COLOR, screen, WIDTH // 2, HEIGHT // 4)

        # Кнопка для начала игры заново
        draw_button('Начать заново', font, screen, WIDTH // 2 - 130, HEIGHT // 2 - 50, 260, 60,
                    action=lambda: game_loop(level=1))

        # Кнопка для выхода
        draw_button('Выход', font, screen, WIDTH // 2 - 130, HEIGHT // 2 + 50, 260, 60, quit_game)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        pygame.display.flip()
        clock.tick(60)  # Обновляем экран 60 раз в секунду



def game_loop(level):
    all_sprites = pygame.sprite.Group()
    font_small = pygame.font.SysFont(None, 30)
    player = Player()
    all_sprites.add(player)

    platforms = pygame.sprite.Group()
    platform = Platform_Ground(0, HEIGHT + 40, WIDTH + 100, 100, "Sprites\\layer-2.png")
    all_sprites.add(platform)
    platforms.add(platform)

    platform_positions = {
        1: [
            (25, 570, 150, 20),
            (200, 480, 150, 20),
            (500, 480, 150, 20),
            (650, 390, 150, 20),
            (430, 280, 150, 20),
            (700, 200, 150, 20)
        ],
        2: [
            (450, 590, 150, 20),
            (250, 500, 150, 20),
            (650, 500, 150, 20),
            (830, 390, 150, 20),
            (150, 220, 150, 20),
            (300, 420, 150, 20),
            (600, 320, 150, 20)
        ],
        3: [
            (50, 600, 200, 20),
            (300, 400, 200, 20),
            (550, 300, 200, 20),
            (200, 200, 200, 20),
            (400, 450, 200, 20)
        ],
        4: [
            (100, 450, 150, 20),
            (250, 350, 150, 20),
            (400, 250, 150, 20),
            (550, 150, 150, 20),
            (200, 400, 150, 20)
        ],
        5: [
            (50, 450, 200, 20),
            (300, 350, 200, 20),
            (600, 300, 200, 20),
            (100, 200, 200, 20),
            (400, 100, 200, 20)
        ]
    }

    finish_positions = {
        1: (WIDTH - 100, HEIGHT - 0),
        2: (WIDTH - 150, HEIGHT - 0),
        3: (WIDTH - 120, HEIGHT - 0),
        4: (WIDTH - 100, HEIGHT - 0),
        5: (WIDTH - 80, HEIGHT - 0)
    }

    for x, y, width, height in platform_positions[level]:
        platform = Platform(x, y, width, height)
        all_sprites.add(platform)
        platforms.add(platform)

    finish_image_path = "C:\\Users\\Илья\\PycharmProjects\\PyGame\\.venv\\Sprites\\finish_image.jpg"
    finish_x, finish_y = finish_positions[level]
    finish_sprite = FinishSprite(finish_x, finish_y, finish_image_path)
    all_sprites.add(finish_sprite)

    running = True
    clock = pygame.time.Clock()
    waiting_for_click = False

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.jump()
                if event.key == pygame.K_LEFT:
                    player.x_speed = -5
                if event.key == pygame.K_RIGHT:
                    player.x_speed = 5
                if event.key == pygame.K_DOWN:
                    player.drop_down()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.x_speed = 0

        all_sprites.update(platforms)



        if pygame.sprite.collide_rect(player, finish_sprite):
            if level == 5:
                running = False
                end_menu()
            else:
                level += 1
                game_loop(level)

        if not waiting_for_click:
            screen.blit(bg, (0, 0))
            draw_text(f"Уровень {level}", font_small, FONT_COLOR, screen, WIDTH - 50, 10)
            all_sprites.draw(screen)
            pygame.display.flip()

    pygame.quit()
