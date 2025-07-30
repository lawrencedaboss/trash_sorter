import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fighting Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Fighter class
class Fighter:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.health = 100

def draw(self):
    pygame.draw.rect(screen, self.color, (self.x, self.y, 50, 50))

def attack(self, opponent):
    damage = random.randint(5, 20)
    opponent.health -= damage

# Create fighters
fighter1 = Fighter(100, HEIGHT - 100, RED)
fighter2 = Fighter(WIDTH - 150, HEIGHT - 100, BLUE)

# Main game loop
running = True
while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Draw fighters
fighter1.draw()
fighter2.draw()

# Check for attacks (for simplicity using random attacks)
if random.randint(0, 50) == 1:
    fighter1.attack(fighter2)
if random.randint(0, 50) == 1:
    fighter2.attack(fighter1)

# Display health
font = pygame.font.Font(None, 36)
health_text1 = font.render(f"Fighter1 Health: {fighter1.health}", True, RED)
health_text2 = font.render(f"Fighter2 Health: {fighter2.health}", True, BLUE)
screen.blit(health_text1, (10, 10))
screen.blit(health_text2, (WIDTH - 250, 10))

pygame.display.flip()
pygame.time.delay(100)

pygame.quit()