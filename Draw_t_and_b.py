import pygame


pygame.init()
FONT_COLOR = (255, 255, 255)
BUTTON_COLOR = (0, 102, 204)
BUTTON_HOVER_COLOR = (0, 153, 255)


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


def draw_button(text, font, surface, x, y, width, height, action=None):
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    button_color = BUTTON_HOVER_COLOR if x < mouse_pos[0] < x + width and y < mouse_pos[1] < y + height else BUTTON_COLOR

    pygame.draw.rect(surface, button_color, (x, y, width, height))
    draw_text(text, font, FONT_COLOR, surface, x + width // 2, y + height // 2)

    if button_color == BUTTON_HOVER_COLOR and mouse_click[0] and action:
        action()