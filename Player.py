import pygame
from load_image import load_image


pygame.init()

WIDTH, HEIGHT = 1024, 650
scale_factor = 0.8
player_images = {
    "idle": load_image("Sprites\Стойка.png", scale_factor),
    "right": [
        load_image("Sprites\Бег1.png", scale_factor),
        load_image("Sprites\Бег2.png", scale_factor),
        load_image("Sprites\Бег3.png", scale_factor),
        load_image("Sprites\Бег4.png", scale_factor),
        load_image("Sprites\Бег5.png", scale_factor),
        load_image("Sprites\Бег6.png", scale_factor)
    ],
    "left": [
        pygame.transform.flip(load_image("Sprites\Бег1.png", scale_factor), True, False),
        pygame.transform.flip(load_image("Sprites\Бег2.png", scale_factor), True, False),
        pygame.transform.flip(load_image("Sprites\Бег3.png", scale_factor), True, False),
        pygame.transform.flip(load_image("Sprites\Бег4.png", scale_factor), True, False),
        pygame.transform.flip(load_image("Sprites\Бег5.png", scale_factor), True, False),
        pygame.transform.flip(load_image("Sprites\Бег6.png", scale_factor), True, False)
    ],
    "jump_right": load_image("Sprites\Прыжок3.png", scale_factor),
    "jump_left": pygame.transform.flip(load_image("Sprites\Прыжок3.png", scale_factor), True, False),
}

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