import pygame
from settings import CUBE_WIDTH, CUBE_HEIGHT


scaled_coin_image = pygame.transform.scale( pygame.image.load("images/coin.png"), (CUBE_WIDTH, CUBE_HEIGHT) )
scaled_brick_image = pygame.transform.scale( pygame.image.load("images/brick.png"), (CUBE_WIDTH, CUBE_HEIGHT) )
scaled_campfire_image = pygame.transform.scale( pygame.image.load("images/campfire.png"), (CUBE_WIDTH, CUBE_HEIGHT) )
ladder_image = pygame.transform.scale( pygame.image.load("images/ladder.png"), (CUBE_WIDTH, CUBE_HEIGHT) )

