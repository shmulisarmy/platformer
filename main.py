from collections import defaultdict
from dataclasses import dataclass
import pygame
from classes.object import Object, Pos
from custom_event_loop import scheduled_events, scheduled_event, frames_passed

from camera import camera_follow, middle_position as camera_middle
from classes.player import Player
from levels import levels
from settings import CUBE_HEIGHT, CUBE_WIDTH, HEIGHT, WIDTH
from constants import BLACK, BLUE, DARK_BLUE, GREY, LIGHT_BLUE, LIGHT_GREEN, LIGHT_RED, RED, WHITE

from settings import CUBE_HEIGHT, CUBE_WIDTH
from game_state import games_state
import custom_event_loop


from loaded_assets import *




pygame.init()

c = 2

























player = Player()


player.followers[Object(0, 0, 10, 60, color=GREY)] = Pos(-10, -5)
player.followers[Object(0, 0, 8, 58, color=BLACK)] = Pos(-9, -4)
player.followers[Object(0, 0, 6, 56, color=LIGHT_RED)] = Pos(-8, -3)



def button_rendered(button: list[Object, 'text']):
    textPos = button[1].get_rect()
    textPos.y = button[0].y - (camera_middle['y']-HEIGHT//2)
    textPos.x = button[0].x - (camera_middle['x']-WIDTH//2)
    actual_button: Object = button[0]
    print(f'{actual_button = }')
    
    # actuall_button.draw(camera_middle)
    padding_x = 8
    padding_y = 4
    border_size = 2
    radius = 6
    def draw_border(rect: pygame.Rect, color: tuple[int, int, int], radius: int, border_size: int):
        pygame.draw.rect(screen, color, (rect.left-border_size, rect.top-border_size, rect.width+border_size*2, rect.height+border_size*2), border_radius=radius)

    draw_border(pygame.Rect(actual_button.x-padding_x, actual_button.y-padding_y, actual_button.size_x+padding_x*2, actual_button.size_y+padding_y*2), DARK_BLUE, radius, border_size)
    pygame.draw.rect(screen, actual_button.color, (actual_button.x-padding_x, actual_button.y-padding_y, actual_button.size_x+padding_x*2, actual_button.size_y+padding_y*2), border_radius=radius)
    screen.blit(button[1], (actual_button.x, actual_button.y))


buttons = []

def create_button(y, x, text, callback: callable = None) -> tuple['y', 'x']:
    font = pygame.font.Font(None, 28)
    text = font.render(text, True, BLACK)
    textpos = text.get_rect()


    el = Object(y, x, textpos.height, textpos.width, color=LIGHT_GREEN)
    buttons.append((el, text))

    return y+textpos.height, x+textpos.width


def buttons_flexer(texts, start_x = 20, start_y = 20, gap = 30):
    last_button_end = start_x + gap
    for text in texts:
        last_button_end = create_button(start_y, last_button_end+gap, text)[1]


# create_button(30, 30, "use power up")
# create_button(80, 30, "use liver chopper")
# create_button(130, 30, "use power sword")


buttons_flexer([
    "use power up",
    "use liver sword",
    "use liver sword",
], start_y=HEIGHT-30, gap=40)

def handle_keyboard_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_DOWN, pygame.K_s):
                player.pressed_keys["down"] = True
            elif event.key in (pygame.K_UP, pygame.K_w):
                player.pressed_keys["up"] = True
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                player.pressed_keys["left"] = True
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                player.pressed_keys["right"] = True
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_DOWN, pygame.K_s):
                player.pressed_keys["down"] = False
            elif event.key in (pygame.K_UP, pygame.K_w):
                player.pressed_keys["up"] = False
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                player.pressed_keys["left"] = False
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                player.pressed_keys["right"] = False
            

            if event.key - 48 in levels:
                games_state["current_level"] = levels[event.key - 48]



animate_letter_index = 0

def render_text(pos_y, pos_x, text, color=WHITE, animate_letter_index=None):
    font = pygame.font.Font(None, 36)
    if animate_letter_index:
        text = font.render(f'{text[:int(animate_letter_index%len(text)+1)]}', True, color)
    else:
        text = font.render(f'{text}', True, color)

    textpos = text.get_rect()
    textpos.centerx = screen.get_rect().centerx
    screen.blit(text, textpos)


def render_progress_bar(pos_y, pos_x, percent, color=WHITE):
    font = pygame.font.Font(None, 36)
    text = font.render(f'{percent}%', True, color)

    textpos = text.get_rect()
    textpos.y = pos_y - (camera_middle['y']-HEIGHT//2)
    textpos.x = pos_x - (camera_middle['x']-WIDTH//2)
    screen.blit(text, textpos)





from settings import screen


pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
while True:
    handle_keyboard_events()
    clock.tick(60)
    

    

    player.handle_movement_ques()
    player.loop_logic()
    screen.fill(BLACK)
    games_state['current_level'].draw_board(camera_middle)
    player.draw(camera_middle)



    render_text(WIDTH//2, 0, f"coins: {player.coins_collected}", animate_letter_index=animate_letter_index)
    animate_letter_index+=.05



    for button in buttons:
        button_rendered(button)

    pygame.display.update()

    custom_event_loop.frames_passed+=1


    





    camera_follow(player)


    if custom_event_loop.frames_passed in scheduled_events:
        for event in scheduled_events[custom_event_loop.frames_passed]:
            event()
        del scheduled_events[custom_event_loop.frames_passed] 


    if custom_event_loop.frames_passed%20 == 0:
        player.health-=1
    print(f'{player.health = }')
    

    







# Todo

# add buttons
# add sand
# green door next level, orange door last level
# make coins appear piratically
# paralax stars