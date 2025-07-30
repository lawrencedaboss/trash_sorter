import pygame, threading, time, openai

pygame.init()
screen = pygame.display.set_mode((850, 675))
clock = pygame.time.Clock()
TILE_SIZE = 25
openai.api_key = "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"  # Replace with your actual OpenAI API key

# Function to query GPT for ghost movement
def get_gpt_direction(ghost_pos, pac_pos):
    prompt = (
        f"The ghost is at position {ghost_pos}. Pac-Man is at {pac_pos}. "
        "Which direction should the ghost move to best intercept Pac-Man while avoiding walls? "
        "Respond with one word: up, down, left, or right."
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        direction = response.choices[0].message.content.strip().lower()
        return direction
    except Exception as e:
        print("OpenAI error:", e)
        return "right"  # fallback


def dir_to_vector(d):
    if d == "up": return (0, -TILE_SIZE)
    if d == "down": return (0, TILE_SIZE)
    if d == "left": return (-TILE_SIZE, 0)
    if d == "right": return (TILE_SIZE, 0)
    return (0, 0)

# Pac-Man setup
def pacman():
    image = pygame.image.load("pacman.png")
    image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
    rect = image.get_rect(topleft=(400, 350))
    return image, rect

image, rect = pacman()
x, y = rect.topleft
score = 0
moving = False
direction = None
target_pos = rect.topleft
move_delay = 150
last_move_time = pygame.time.get_ticks()
font = pygame.font.SysFont(None, 36)

# Ghost class with OpenAI logic
class Ghost:
    def __init__(self, image_path, start_pos):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=start_pos)

    def move(self, wall_rects, pac_pos):
        direction_str = get_gpt_direction(self.rect.topleft, pac_pos)
        dx, dy = dir_to_vector(direction_str)
        new_pos = self.rect.move(dx, dy)
        if not any(new_pos.colliderect(w) for w in wall_rects):
            self.rect = new_pos

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Maze setup
grid = [
    "##################################",
    "#................................#",
    "#.#######.##.########.##.#######.#",
    "#.#######.##.########.##.#######.#",
    "#.........##....##....##.........#",
    "#.####.##.####..##..####.##.####.#",
    "#.###..##.####..##..####.##..###.#",
    "#.##..###.##..........##.###..##.#",
    "#.##.##...##.###--###.##...##.##.#",
    "#.##.##.#....#      #....#.##.##.#",
    "#.##.##.#.##.########.##.#.##....#",
    "#.##.##.#.##..........##.#....##.#",
    "#.####.##.##..........##.##.####.#",
    "#.####.##.##..........##.##.####.#",
    "#......##.##.... .....##.##......#",
    "#.#######.##.########.##.#######.#",
    "#.#######.##.########.##.#######.#",
    "#...............##...............#",
    "#.##*####.#####.##.#####.####*##.#",
    "#.##...##................##...##.#",
    "#.####.##.##.########.##.##.####.#",
    "#.##......##....##....##......##.#",
    "#.##.##.#######.##.#######.##.##.#",
    "#.##.#........#.##.#........#.##.#",
    "#.##.#.######.#.##.#.######.#.##.#",
    "#................................#",
    "##################################"
]

wall_rects, pellet_rects, power_pellets = [], [], []

def build_map():
    for row_index, row in enumerate(grid):
        for col_index, tile in enumerate(row):
            px, py = col_index * TILE_SIZE, row_index * TILE_SIZE
            if tile == '#':
                wall_rects.append(pygame.Rect(px, py, TILE_SIZE, TILE_SIZE))
            elif tile == '.':
                pellet_rects.append(pygame.Rect(px+12.5, py+12.5, 4, 4))
            elif tile == '*':
                power_pellets.append(pygame.Rect(px+7.5, py+7.5, 12.5, 12.5))

def draw_map():
    for wall in wall_rects:
        pygame.draw.rect(screen, (0, 0, 255), wall)
    for pellet in pellet_rects:
        pygame.draw.rect(screen, (255, 255, 0), pellet)
    for power in power_pellets:
        pygame.draw.rect(screen, (255, 0, 255), power)

build_map()

ghost = Ghost("red_ghost.png", (375, 175))
clock = pygame.time.Clock()
running = True

while running:
    screen.fill((0, 0, 0))
    draw_map()
    keys = pygame.key.get_pressed()
    now = pygame.time.get_ticks()

    # Movement
    if not moving:
        if keys[pygame.K_LEFT]: direction = (-TILE_SIZE, 0)
        elif keys[pygame.K_RIGHT]: direction = (TILE_SIZE, 0)
        elif keys[pygame.K_UP]: direction = (0, -TILE_SIZE)
        elif keys[pygame.K_DOWN]: direction = (0, TILE_SIZE)

        if direction:
            new_x, new_y = x + direction[0], y + direction[1]
            future = rect.copy()
            future.topleft = (new_x, new_y)
            if not any(future.colliderect(w) for w in wall_rects):
                target_pos = (new_x, new_y)
                moving = True
                last_move_time = now
                direction = None
    elif now - last_move_time >= move_delay:
        x, y = target_pos
        rect.topleft = target_pos
        moving = False

    # Eat pellets
    for p in pellet_rects:
        if rect.colliderect(p):
            pellet_rects.remove(p)
            score += 10
            break

    for p in power_pellets:
        if rect.colliderect(p):
            power_pellets.remove(p)
            score += 50
            break

    screen.blit(image, rect)
    ghost.move(wall_rects, rect.topleft)
    ghost.draw(screen)
    score_surf = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_surf, (5, 5))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()