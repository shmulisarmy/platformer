import pygame


from settings import screen


def draw_border(rect: pygame.Rect, color: tuple[int, int, int], radius: int, border_size: int):
    pygame.draw.rect(screen, color, (rect.left-border_size, rect.top-border_size, rect.width+border_size*2, rect.height+border_size*2), border_radius=radius)
