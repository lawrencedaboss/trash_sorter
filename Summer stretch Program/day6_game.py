

import pygame
import sys


# Initialize pygame
pygame.init()

# Set the dimensions of the game window
width, height = 600, 400
screen = pygame.display.set_mode((width, height))  # Create the game window
pygame.display.set_caption("Move the Player")      # Set the window title

# Define RGB colors
WHITE = (255, 255, 255)  # Background color
BLUE = (0, 0, 255)       # Player color

# Set the player properties
player_size = 50     # Width and height of the player square
x = 100              # Starting horizontal position
y = 100              # Starting vertical position
speed = 5            # Number of pixels the player moves per frame

# Game loop: runs until the user closes the window
running = True
while running:
    screen.fill(WHITE)  # Clear the screen with a white background
    
    # Event handling loop (checks for user input like quitting)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key press detection
    keys = pygame.key.get_pressed()  # Get the state of all keyboard keys
    if keys[pygame.K_LEFT]:    # If LEFT arrow is pressed
        x -= speed
    if keys[pygame.K_RIGHT]:   # If RIGHT arrow is pressed
        x += speed
    if keys[pygame.K_UP]:      # If UP arrow is pressed
        y -= speed
    if keys[pygame.K_DOWN]:    # If DOWN arrow is pressed
        y += speed

    # Draw the player rectangle at the updated position
    pygame.draw.rect(screen, BLUE, (x, y, player_size, player_size))

    # Refresh the screen to show the new frame
    pygame.display.flip()

    # Limit the frame rate to 60 frames per second
    pygame.time.Clock().tick(60)

# Exit the game and close the window cleanly
pygame.quit()
sys.exit()