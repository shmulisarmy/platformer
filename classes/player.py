import pygame

from .object import Object
from constants import RED
from settings import HEIGHT, WIDTH, screen

from game_state import games_state

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

    def draw(self, camera_middle):
        if self.image:
            scaled_image = pygame.transform.scale(self.image, (self.size_x, self.size_y))
            screen.blit(scaled_image, (self.x - (camera_middle['x']-WIDTH//2), self.y - (camera_middle['y']-HEIGHT//2)))
        else:
            pygame.draw.rect(screen, self.color, (self.x - camera_middle['x'], self.y - camera_middle['y'], self.size_x, self.size_y))

    def attempt_to_move_to(self, new_x, new_y):
        if not games_state['current_level'].colliding_with_board(Object(new_y, new_x, self.size_x, self.size_y)):
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
            
