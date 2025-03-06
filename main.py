from collections import defaultdict
from dataclasses import dataclass
import pygame
from classes.object import Object
from custom_event_loop import scheduled_events, scheduled_event, frames_passed

from camera import camera_follow, middle_position as camera_middle
from classes.player import Player
from levels import levels
from settings import CUBE_HEIGHT, CUBE_WIDTH, HEIGHT, WIDTH
from constants import BLACK, WHITE

from settings import CUBE_HEIGHT, CUBE_WIDTH
from game_state import games_state
import custom_event_loop


from loaded_assets import *




pygame.init()

c = 2

























player = Player()








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
            
            elif event.key in (pygame.K_2, pygame.K_KP2):
                games_state['current_level'] = levels[2]


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
    pygame.display.update()

    custom_event_loop.frames_passed+=1


    



    
    camera_follow(player)


    if custom_event_loop.frames_passed in scheduled_events:
        for event in scheduled_events[custom_event_loop.frames_passed]:
            event()
        del scheduled_events[custom_event_loop.frames_passed] 

    print(f'{custom_event_loop.frames_passed = }')
    







# Todo

# add buttons
# add sand
# green door next level, orange door last level
# make coins appear piratically
# paralax stars