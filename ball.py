import pygame
import random
from pygame.locals import QUIT

pygame.init()
pygame.display.set_caption("Flappy Blud")

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

#point system
score = 0
font = pygame.font.Font(None, 36)

# Player starting position
player_x = 400
player_y = 300  

# Pipe settings
pipe_width = 50
pipe_gap = 200 # Gap between top and bottom pipes
pipe_speed = 1.7
pipe_spacing = 300  # Distance between pipe sets

# Create multiple pipe sets
class PipeSet:
    def __init__(self, x):
        self.x = x
        # Randomize gap position (keep gap away from edges)
        gap_y = random.randint(100, screen_height - pipe_gap - 100)
        
        # Top pipe (from top of screen to gap)
        self.top_rect = pygame.Rect(x, 0, pipe_width, gap_y)
        
        # Bottom pipe (from gap to bottom of screen)
        self.bottom_rect = pygame.Rect(x, gap_y + pipe_gap, pipe_width, screen_height - (gap_y + pipe_gap))
        
        # Track if player has passed this pipe set
        self.passed = False
    
    def move(self):
        self.x -= pipe_speed
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x
    
    def is_off_screen(self):
        return self.x < -pipe_width
    
    def check_collision(self, player_rect):
        return player_rect.colliderect(self.top_rect) or player_rect.colliderect(self.bottom_rect)
    
    def check_passed(self, player_x):
        if not self.passed and self.x + pipe_width < player_x:
            self.passed = True
            return True
        return False

# Create initial pipe sets
pipes = []
for i in range(3):  # Start with 3 pipe sets
    pipes.append(PipeSet(screen_width + i * pipe_spacing))

# Player velocity
velocity_y = 0
gravity = 0.76
jump_strength = -10

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        # Handle jumping - INSIDE the event loop for key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                velocity_y = jump_strength  # Apply jump force
    
    # Move all pipes
    for pipe in pipes:
        pipe.move()
    
    # Remove off-screen pipes and add new ones
    pipes = [pipe for pipe in pipes if not pipe.is_off_screen()]
    
    # Add new pipe when the last pipe is far enough
    if len(pipes) == 0 or pipes[-1].x < screen_width - pipe_spacing:
        pipes.append(PipeSet(screen_width))
    
    # Apply gravity
    velocity_y += gravity
    player_y += velocity_y
    
    # Update player rect position
    player_rect = pygame.Rect(player_x - 20, player_y - 20, 40, 40)
    
    # Boundary checks
    if player_y < 20:  # Hit ceiling
        player_y = 20
        velocity_y = 0  # Stop upward movement
        print("Hit the ceiling! Final Score:", score)
        running = False
    
    if player_y > screen_height - 20:  # Hit ground
        player_y = screen_height - 20
        velocity_y = 0  # Stop falling
        print("Hit the ground! Final Score:", score)
        running = False
    
    # Check collisions with all pipes
    collision = False
    for pipe in pipes:
        if pipe.check_collision(player_rect):
            collision = True
            break
    
    if collision:
        print("Collision detected! Final Score:", score)
        running = False
    
    # Check scoring for all pipes
    for pipe in pipes:
        if pipe.check_passed(player_x):
            score += 1
            print("Score:", score)
        
    # Clear screen
    screen.fill((0, 0, 0))
    
    # Draw player
    pygame.draw.circle(screen, (255, 150, 0), (int(player_x), int(player_y)), 20)
    
    # Draw all pipes
    for pipe in pipes:
        pygame.draw.rect(screen, (0, 150, 0), pipe.top_rect)
        pygame.draw.rect(screen, (0, 150, 0), pipe.bottom_rect)
    
    # Draw score on screen
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    
    clock.tick(60)
    pygame.display.flip()

pygame.quit() 