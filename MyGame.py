import pygame
import random

PLATFORM_COLOR = (50, 150, 50)
WIDTH, HEIGHT = 1024, 650
SKY = (135, 206, 235)
GREEN_GROUND = (0, 200, 0)
FONT_COLOR = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Jump 'n' Run")
font = pygame.font.SysFont(None, 48)

level = 1

def load_image(name, scale_factor):
    image = pygame.image.load(name).convert_alpha()
    return pygame.transform.scale(image,
                                  (int(image.get_width() * scale_factor), int(image.get_height() * scale_factor)))

scale_factor = 0.8
player_images = {
    "idle": load_image("Стойка.png", scale_factor),
    "right": [
        load_image("Бег1.png", scale_factor),
        load_image("Бег2.png", scale_factor),
        load_image("Бег3.png", scale_factor),
        load_image("Бег4.png", scale_factor),
        load_image("Бег5.png", scale_factor),
        load_image("Бег6.png", scale_factor)
    ],
    "left": [
        pygame.transform.flip(load_image("Бег1.png", scale_factor), True, False),
        pygame.transform.flip(load_image("Бег2.png", scale_factor), True, False),
        pygame.transform.flip(load_image("Бег3.png", scale_factor), True, False),
        pygame.transform.flip(load_image("Бег4.png", scale_factor), True, False),
        pygame.transform.flip(load_image("Бег5.png", scale_factor), True, False),
        pygame.transform.flip(load_image("Бег6.png", scale_factor), True, False)
    ],
    "jump_right": load_image("Прыжок3.png", scale_factor),
    "jump_left": pygame.transform.flip(load_image("Прыжок3.png", scale_factor), True, False),

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = player_images
        self.image = self.images["idle"]
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2
        self.rect.bottom = HEIGHT + 300
        self.y_speed = 0
        self.x_speed = 0
        self.gravity = 1
        self.is_jumping = False
        self.direction = "right"
        self.animation_frame = 0
        self.animation_speed = 0.1

    def update(self):
        self.rect.x += self.x_speed
        self.y_speed += self.gravity
        self.rect.y += self.y_speed

        if self.rect.bottom > HEIGHT + 70:
            self.rect.bottom = HEIGHT + 70
            self.y_speed = 0
            self.is_jumping = False

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        self.animate()

    def jump(self):
        if not self.is_jumping:
            self.y_speed = -15
            self.is_jumping = True

    def animate(self):
        if self.is_jumping:
            self.image = self.images["jump_right"] if self.direction == "right" else self.images["jump_left"]
        elif self.x_speed > 0:
            self.direction = "right"
            animation_list = self.images["right"]
            self.animation_frame = (self.animation_frame + self.animation_speed) % len(animation_list)
            self.image = animation_list[int(self.animation_frame)]
        elif self.x_speed < 0:
            self.direction = "left"
            animation_list = self.images["left"]
            self.animation_frame = (self.animation_frame + self.animation_speed) % len(animation_list)
            self.image = animation_list[int(self.animation_frame)]
        else:
            self.image = self.images["idle"]

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

    finish_image_path = "finish_image.jpg"
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

def reset_game():
    global level
    level = 1
    game_loop(level)

main_menu()
