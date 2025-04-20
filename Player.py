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
        self.ignore_platforms = False
        self.drop_timer = 0
        self.spread = False

    def update(self, platforms):
        self.rect.x += self.x_speed
        self.y_speed += self.gravity
        self.rect.y += self.y_speed

        # если отключены проверки (игнорируем платформы)
        if self.ignore_platforms:
            # проверяем, достиг ли он пола или платформы
            if self.rect.bottom >= HEIGHT + 70:
                # достиг пола
                self.rect.bottom = HEIGHT + 70
                self.y_speed = 0
                self.ignore_platforms = False
            else:
                # проверяем коллизию с платформами
                collisions = pygame.sprite.spritecollide(self, platforms, False)
                if collisions:
                    # достиг платформы — остановиться
                    self.rect.bottom = collisions[0].rect.top
                    self.y_speed = 0
                    self.ignore_platforms = False

        else:
            # обычная проверка коллизий
            if not self.ignore_platforms:
                collisions = pygame.sprite.spritecollide(self, platforms, False)
                if collisions:
                    if self.y_speed > 0:
                        self.rect.bottom = collisions[0].rect.top
                        self.y_speed = 0
                        self.is_jumping = False

        # границы
        if self.rect.bottom > HEIGHT + 70:
            self.rect.bottom = HEIGHT + 70
            self.y_speed = 0
            self.is_jumping = False

        # границы по горизонтали
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        self.animate()

    def jump(self):
        if not self.is_jumping:
            self.y_speed = -15
            self.is_jumping = True

    def drop_down(self):
        # мгновенно отключить проверку коллизий и начать падение
        self.ignore_platforms = True
        self.y_speed = 10  # или больше, чтобы быстро упасть

    def animate(self):
        # Сохраняем текущую позицию нижней части и координату x персонажа
        bottom = self.rect.bottom
        x = self.rect.x

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

        # Обновляем rect для нового изображения
        self.rect = self.image.get_rect()

        # Восстанавливаем позицию нижней части и координату x персонажа
        self.rect.bottom = bottom
        self.rect.x = x
