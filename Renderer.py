import pygame
import config
import sys
import time

# Pygame setup
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Red Ball Simulation")

# Clock and delta time setup
clock = pygame.time.Clock()

# Colors
SKY_BLUE = (173, 216, 230)
GRASS_GREEN = (0, 128, 0)
RED = (255, 0, 0)

# Ground level
GROUND_Y = HEIGHT - 100

# Ball setup
BALL_RADIUS = 30

# Scaling: total height of monitor represents 10 meters
PIXELS_PER_METER = HEIGHT / 10.0

# Initial position and velocity from config
x = 0  # starting horizontal position (meters)
y = config.InitialHeight  # starting vertical position (meters)
vx = config.initialVelocityX  # horizontal velocity (m/s)
vy = config.initialVelocityY  # vertical velocity (m/s)

# Convert initial position to pixel coordinates
ball_bottom_x = x * PIXELS_PER_METER
ball_bottom_y = GROUND_Y - (y * PIXELS_PER_METER)  # Subtract because pygame y increases downward

def draw(ball_bottom_x, ball_bottom_y):
    screen.fill(SKY_BLUE)
    
    # Draw ground
    pygame.draw.rect(screen, GRASS_GREEN, pygame.Rect(0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y))
    
    # Compute center of ball based on bottom point
    ball_center = (int(ball_bottom_x), int(ball_bottom_y - BALL_RADIUS))
    
    # Draw ball
    pygame.draw.circle(screen, RED, ball_center, BALL_RADIUS)

start_time = time.time()

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Delta time
    delta_time = clock.tick(60) / 1000.0  # Seconds per frame
    
    # Update physics while ball has velocity or is above ground
    if ball_bottom_y < GROUND_Y or (vx != 0 or vy != 0):
        # Update velocities (gravity affects vertical velocity)
        vy += config.Gravity * delta_time  # Gravity is negative, so this decreases vy
        
        # Update positions
        ball_bottom_x += vx * delta_time * PIXELS_PER_METER
        ball_bottom_y -= vy * delta_time * PIXELS_PER_METER  # Subtract because pygame y increases downward
        
        # Check if ball hits ground
        if ball_bottom_y >= GROUND_Y:
            ball_bottom_y = GROUND_Y
            # Stop the ball (no bounce)
            vx = 0
            vy = 0
    
    # Draw everything
    draw(ball_bottom_x, ball_bottom_y)
    
    # Flip display
    pygame.display.flip()

# Cleanup
pygame.quit()
sys.exit()