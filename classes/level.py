from dataclasses import dataclass

from classes.object import Object
from settings import CUBE_HEIGHT, CUBE_WIDTH, HEIGHT, WIDTH, screen
from loaded_assets import *



@dataclass
class Level:
    board: list[list[int]]

    def draw_board(self, middle_position):
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                color_index = self.board[y][x]
                draw_x = x * CUBE_WIDTH - (middle_position['x']-WIDTH//2)
                draw_y = y * CUBE_HEIGHT - (middle_position['y']-HEIGHT//2)
                
                if color_index == 3:
                    screen.blit(scaled_campfire_image, (draw_x, draw_y))
                elif color_index == 2:
                    screen.blit(scaled_coin_image, (draw_x, draw_y))
                elif color_index == 1:
                    screen.blit(scaled_brick_image, (draw_x, draw_y))
                elif color_index == 4:
                    screen.blit(ladder_image, (draw_x, draw_y))

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


