from collections import defaultdict
from dataclasses import dataclass
import math
import random
import pygame





WIDTH = 1200
HEIGHT = 1200

CUBE_WIDTH = 40
CUBE_HEIGHT = 40

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

pygame.init()

c = 2


@dataclass
class Object:
    y: int 
    x: int 
    size_y: int 
    size_x: int 

    def short_grow(self, y_amount: int, x_amount: int):
        self.size_y+=y_amount
        self.size_x+=x_amount


        # to accommodate visually
        self.y-=y_amount
        self.x-=x_amount

        def shrink_back_down():
            self.size_y-=y_amount
            self.size_x-=x_amount
            
            self.y+=y_amount
            self.x+=x_amount

        scheduled_event(shrink_back_down, 50)



@dataclass
class Level:
    board: list[list[int]]

    def draw_board(self):
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                color_index = self.board[y][x]
                draw_x = x * CUBE_WIDTH - camera_offset['x']
                draw_y = y * CUBE_HEIGHT - camera_offset['y']
                
                if color_index == 3:
                    screen.blit(scaled_campfire_image, (draw_x, draw_y))
                elif color_index == 2:
                    screen.blit(scaled_coin_image, (draw_x, draw_y))
                elif color_index == 1:
                    screen.blit(scaled_brick_image, (draw_x, draw_y))

    def collect_coins(self, object: Object) -> int:
        """returns coins_collected"""
        start_y = int(object.y//CUBE_HEIGHT)
        start_x = int(object.x//CUBE_WIDTH)

        end_y =    int((object.y + object.size_y)//CUBE_HEIGHT)
        end_x = int((object.x + object.size_x)//CUBE_WIDTH )

        
        coins_collected = 0

        for y in range(start_y, end_y + 1):
            for x in range(start_x, end_x + 1):
                if self.board[y][x] == 2:
                    self.board[y][x] = 0
                    coins_collected+=1

        return coins_collected

    def close_to_ground(self, object: Object):
        start_x = int(object.x//CUBE_WIDTH)
        end_x = int((object.x + object.size_x)//CUBE_WIDTH )
        end_y = int((object.y+10 + object.size_y)//CUBE_HEIGHT)
        return any(self.board[end_y][x] != 0 for x in range(start_x, end_x + 1))

    def colliding_with_board(self, object: Object):
        start_y = int(object.y//CUBE_HEIGHT)
        start_x = int(object.x//CUBE_WIDTH)

        end_y =    int((object.y + object.size_y)//CUBE_HEIGHT)
        end_x = int((object.x + object.size_x)//CUBE_WIDTH )

        

        return any(self.board[y][x] == 1 for x in range(start_x, end_x + 1) for y in range(start_y, end_y + 1))








levels: list[Level] = {
    1: Level([
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, c, 0, c, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, c, 0, 2, 0, 3, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, c, 0, c, 0, c, 0, c, 0, 1, 0, 0, 3, 0, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ])
}

games_state = {"current_level": levels[1]}



camera_offset = {
    "x": 0,
    "y": 100,
}










scaled_coin_image = pygame.transform.scale( pygame.image.load("images/coin.png"), (CUBE_WIDTH, CUBE_HEIGHT) )
scaled_brick_image = pygame.transform.scale( pygame.image.load("images/brick.png"), (CUBE_WIDTH, CUBE_HEIGHT) )
scaled_campfire_image = pygame.transform.scale( pygame.image.load("images/campfire.png"), (CUBE_WIDTH, CUBE_HEIGHT) )





class Player(Object):
    def __init__(self) -> None:
        super().__init__(400, 400, 50, 50)
        self.speed_x = 5
        self.speed_y = 5
        self.color = RED
        self.Base_Gravity_Amount = 4
        self.gravity_amount = 4
        self.Base_Jump_Jump_Velocity = 6
        self.Jump_Velocity = 0
        self.jump_amount = 0
        self.coins_collected = 0

        self.sprite = None
        # [
        #     pygame.transform.scale( pygame.image.load('images/duck-1.png')  , (self.size_x, self.size_y)),
        #     pygame.transform.scale( pygame.image.load('images/duck-2.png')  , (self.size_x, self.size_y)), 
        #     pygame.transform.scale( pygame.image.load('images/duck-3.png')  , (self.size_x, self.size_y)), 
        # ]
        self.sprite_index = 0
        self.image =  pygame.image.load('images/duck.png')  

        self.pressed_keys = {
            "up": False,
            "down": False,
            "left": False,
            "right": False
        }
    def fall(self):
        self.attempt_to_move_to(self.x, self.y + self.gravity_amount)
        self.gravity_amount += .1
        
    def is_jumping(self): return self.jump_amount > 0 

    def draw(self):
        if self.image:
            scaled_image = pygame.transform.scale(self.image, (self.size_x, self.size_y))
            screen.blit(scaled_image, (self.x - camera_offset['x'], self.y - camera_offset['y']))
        else:
            pygame.draw.rect(screen, self.color, (self.x - camera_offset['x'], self.y - camera_offset['y'], self.size_x, self.size_y))

    def attempt_to_move_to(self, new_x, new_y):
        if not games_state['current_level'].colliding_with_board(Object(new_y, new_x, self.size_x, self.size_y)):
            handle_main_player_movement(self.x-new_x, self.y-new_y)
            self.x = new_x
            self.y = new_y
            return True
        return False

    def on_ground(self):
        return not games_state['current_level'].colliding_with_board(Object(self.y + self.size_y, self.x, self.size_y, self.size_x))


    def handle_movement_ques(self):
        if self.pressed_keys['up'] and games_state['current_level'].close_to_ground(self):
            self.jump_amount = 100
        if self.pressed_keys['down']:
            self.attempt_to_move_to(self.x, self.y + self.speed_y)
        if self.pressed_keys['left']:
            self.attempt_to_move_to(self.x - self.speed_x, self.y)
        if self.pressed_keys['right']:
            self.attempt_to_move_to(self.x + self.speed_x, self.y)


    def jump(self):
        if self.attempt_to_move_to(self.x, self.y - self.Jump_Velocity):
            self.jump_amount -= self.Jump_Velocity
            self.Jump_Velocity+=.4
        else:
            self.jump_amount = 0





    def loop_logic(self):
        if self.is_jumping():
            self.jump()
        else:
            self.Jump_Velocity = self.Base_Jump_Jump_Velocity
        if not games_state['current_level'].colliding_with_board(self) and not self.is_jumping():
            self.fall()
        else:
            self.gravity_amount = self.Base_Gravity_Amount


        coins_collected_this_frame=games_state['current_level'].collect_coins(self)
        self.coins_collected += coins_collected_this_frame

        if coins_collected_this_frame:
            self.short_grow(10, 10)
            



def handle_main_player_movement(movement_x: int, movement_y: int):
    camera_offset_left_to_move['x'] -= movement_x
    camera_offset_left_to_move['y'] -= movement_y


player = Player()


camera_offset_left_to_move = {
    "x": 0,
    "y": 0,
}


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


scheduled_events = defaultdict(list)

def reconcile_camera_movement():
    if camera_offset_left_to_move['x'] > 4:
        camera_offset['x'] += 4
        camera_offset_left_to_move['x'] -= 4
    elif camera_offset_left_to_move['x'] < -4:
        camera_offset['x'] -= 4
        camera_offset_left_to_move['x'] += 4

    if camera_offset_left_to_move['y'] > 4:
        camera_offset['y'] += 4
        camera_offset_left_to_move['y'] -= 4
    elif camera_offset_left_to_move['y'] < -4:
        camera_offset['y'] -= 4
        camera_offset_left_to_move['y'] += 4


def scheduled_event(func: callable, delay: int):
    scheduled_events[frames_passed+delay].append(func)




frames_passed = 0
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
while True:
    handle_keyboard_events()
    clock.tick(60)
    

    

    player.handle_movement_ques()
    player.loop_logic()
    screen.fill(BLACK)
    games_state['current_level'].draw_board()
    player.draw()



    render_text(WIDTH//2, 0, f"coins: {player.coins_collected}", animate_letter_index=animate_letter_index)
    animate_letter_index+=.05
    pygame.display.update()


    frames_passed+=1


    



    
    reconcile_camera_movement()


    if frames_passed in scheduled_events:
        for event in scheduled_events[frames_passed]:
            event()
        del scheduled_events[frames_passed] 







# Todo

# add buttons
# add sand
# green door next level, orange door last level
# make coins appear piratically
# paralax stars