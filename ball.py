import pygame
from pygame.locals import QUIT

pygame.init()
pygame.display.set_caption("Flappy Blud")

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Iplayer starting position
player_x = 400
player_y = 0

#velocity for sprite
velocity_y = 0.4

gravity = 0.76
jump_strength = -12


running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    # Handle jumping - INSIDE the event loop for key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                velocity_y = jump_strength  # Apply jump force
    
    # Move this outside the event loop
    velocity_y += gravity
    player_y += velocity_y
    
    if player_y < 20:  # Hit ceiling
        player_y = 20
        velocity_y = 0  # Stop upward movement
    
    if player_y > screen_height - 20:  # Hit ground
        player_y = screen_height - 20
        velocity_y = 0  # Stop falling
    
    screen.fill((0, 0, 0))
    
    pygame.draw.circle(screen, (255, 150, 0), (player_x, player_y), 20)
    
    clock.tick(60)
    
    pygame.display.flip()
    

pygame.quit()  