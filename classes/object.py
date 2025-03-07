from dataclasses import dataclass, field
from typing import override

import pygame
from constants import BLUE
from custom_event_loop import scheduled_events, scheduled_event
from settings import HEIGHT, WIDTH, screen
from camera import middle_position as camera_middle
from ui.utils import draw_border


@dataclass
class Pos:
    y: int
    x: int


@dataclass
class Object:
    y: int 
    x: int 
    size_y: int 
    size_x: int 
    color: tuple[int, int, int] = field(default_factory=lambda: BLUE)
    followers: dict['Object', Pos] = field(default_factory=dict)
    image: pygame.Surface | None = field(default_factory=lambda: None)
    styles: dict = field(default_factory=dict)

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

    def draw_children(self):
        for child, pos in self.followers.items():
            child.y = self.y + pos.y
            child.x = self.x + pos.x
            child.draw(camera_middle)
    def draw(self, camera_middle):
        if self.image:
            scaled_image = pygame.transform.scale(self.image, (self.size_x, self.size_y))
            screen.blit(scaled_image, (self.x - (camera_middle['x']-WIDTH//2), self.y - (camera_middle['y']-HEIGHT//2)))
        else:
            pygame.draw.rect(screen, self.color, (self.x - (camera_middle['x']-WIDTH//2), self.y - (camera_middle['y']-HEIGHT//2), self.size_x, self.size_y))
        self.draw_children()

    def draw_with_styles(self):
        padding_x = self.styles.get('padding-x', self.styles.get('padding', 0))
        padding_y = self.styles.get('padding-y', self.styles.get('padding', 0))
        border_size = self.styles.get('border-size', 0)
        radius = self.styles.get('radius', 0)
        border_color = self.styles.get("border-color", self.styles.get("color"))
        background = self.styles.get("background", self.styles.get("color"))
        
        draw_border(pygame.Rect(self.x-padding_x, self.y-padding_y, self.size_x+padding_x*2, self.size_y+padding_y*2), border_color, radius, border_size)
        pygame.draw.rect(screen, background, (self.x-padding_x, self.y-padding_y, self.size_x+padding_x*2, self.size_y+padding_y*2), border_radius=radius)



    def attempt_to_move_by(self, x, y):
        new_x = self.x+x
        new_y = self.y+y
        print(f'{new_y = }')
        
        from game_state import games_state
        if not games_state['current_level'].colliding_with_board(Object(new_y, new_x, self.size_x, self.size_y)):
            self.x = new_x
            self.y = new_y
            return True
        return False


    @override
    def __hash__(self) -> int:
        return hash((self.size_x, self.size_y))

