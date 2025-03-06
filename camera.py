


from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from classes.object import Object


middle_position = {
    "x": 0,
    "y": 0,
}



def camera_follow(object: 'Object'):
    if middle_position['x']-5 > object.x:
        amount_to_follow =  max( ( middle_position['x'] - object.x )/40, 5)
        middle_position['x'] -= amount_to_follow
    elif middle_position['x']+5 < object.x:
        amount_to_follow =  max( ( object.x - middle_position['x'] )/40, 5)
        middle_position['x'] += amount_to_follow

    if middle_position['y']-5 > object.y:
        amount_to_follow =  max( ( middle_position['y'] - object.y )/40, 5)
        middle_position['y'] -= amount_to_follow
    elif middle_position['y']+5 < object.y:
        amount_to_follow =  max( ( object.y - middle_position['y'] )/40, 5)
        middle_position['y'] += amount_to_follow

    
