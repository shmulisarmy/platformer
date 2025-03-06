from dataclasses import dataclass
from custom_event_loop import scheduled_events, scheduled_event

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

