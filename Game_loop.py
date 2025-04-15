import pygame
from Player import Player
from Platforms import Platform, Platform_Ground, FinishSprite


pygame.init()
SKY = (135, 206, 235)
WIDTH, HEIGHT = 1024, 650
level = 1
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


def game_loop(level):
    all_sprites = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)

    platforms = pygame.sprite.Group()
    platform = Platform_Ground(0, HEIGHT + 70, WIDTH, 50)
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
            (600, 320, 150, 20),
            ],
        3: [
            (50, 500, 200, 20),
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
        1: (WIDTH - 100, HEIGHT - 600),
        2: (WIDTH - 150, HEIGHT - 400),
        3: (WIDTH - 120, HEIGHT - 300),
        4: (WIDTH - 100, HEIGHT - 200),
        5: (WIDTH - 80, HEIGHT - 100)
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
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.jump()
                if event.key == pygame.K_LEFT:
                    player.x_speed = -5
                if event.key == pygame.K_RIGHT:
                    player.x_speed = 5
                if event.key == pygame.K_DOWN:
                    if player.rect.bottom < HEIGHT - 50:
                        player.rect.y += 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.x_speed = 0

        all_sprites.update()

        collisions = pygame.sprite.spritecollide(player, platforms, False)
        if collisions:
            player.rect.bottom = collisions[0].rect.top
            player.y_speed = 0
            player.is_jumping = False

        if pygame.sprite.collide_rect(player, finish_sprite):
            if level >= 5:
                draw_text('       Победа!', font, screen, WIDTH // 2 - 100, HEIGHT // 2 - 50)
                draw_button('Начать заново?', font, screen, WIDTH // 2 - 100, HEIGHT // 2 + 20, 270, 50,
                            lambda: reset_game())
                draw_button('Выйти из игры', font, screen, WIDTH // 2 - 100, HEIGHT // 2 + 80, 270, 50, pygame.quit)
                pygame.display.flip()
                waiting_for_click = True
                continue
            else:
                level += 1
                game_loop(level)

        if not waiting_for_click:
            screen.fill(SKY)
            all_sprites.draw(screen)
            pygame.display.flip()

    pygame.quit()