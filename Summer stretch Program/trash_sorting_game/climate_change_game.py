import pygame, random, threading, time

# Initialize Pygame and mixer
pygame.init()
pygame.mixer.init()

# Load and play background music
pygame.mixer.music.load("elevator_music.wav")  # Update path if needed
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  # Loop indefinitely
pygame.mixer.Sound("Incorrect_sound.wav")
pygame.mixer.Sound("Cocorrect_sound.wav")

# Trash logic
trash_item = {
    "banana.png": "trash",
    "plastic_water_bottle.png": "recycle",
    "apple_core.png": "compost",
    "can.png": "recycle",
    "carboard_box.png": "recycle",
    "pizza_box.png": "trash",
}

trash_item_choice = {
    1: "banana.png",
    2: "plastic_water_bottle.png",
    3: "apple_core.png",
    4: "can.png",
    5: "carboard_box.png",
    6: "pizza_box.png",
}

def spawn_item():
    choice = random.randint(1, 6)
    item = trash_item_choice[choice]
    image = pygame.image.load(item)
    width, height = image.get_size()
    image = pygame.transform.scale(image, (width // 9, height // 9))
    location_x = random.randint(1, 500)
    location_y = random.randint(1, 400)
    rect = image.get_rect(topleft=(location_x, location_y))
    return item, image, rect
def spawn_answer():
    correct = pygame.image.load("check.png")
    incorrect = pygame.image.load("x.png")
    check = image.get_rect(topleft=(250, 250))
    x = image.get_rect(topleft=(250, 250))
    return correct, incorrect, check, x

# Setup
screen = pygame.display.set_mode((700, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)
pygame.display.set_caption("Trash Sorter Game")


items = []  # Shared list of items

lock = threading.Lock()

def item_spawner():
    while running:  # Will need to be global
        with lock:
            new_item = spawn_item()
            items.append(new_item)
        time.sleep(2)

# Buttons
button_tra = pygame.Rect(75, 500, 120, 45)
button_recy = pygame.Rect(500, 500, 120, 45)
button_comp = pygame.Rect(305, 500, 120, 45)

def draw_button(text, rect, color):
    pygame.draw.rect(screen, color, rect)
    txt_surface = font.render(text, True, (255, 255, 255))
    txt_rect = txt_surface.get_rect(center=rect.center)
    screen.blit(txt_surface, txt_rect)

# Game State
item_spawned, image, image_rect = spawn_item()
correct, incorrect, check, x = spawn_answer()

score = 0
start_ticks = pygame.time.get_ticks()
dragging = False
offset_x = 0
offset_y = 0
running = True
show_x = False
show_y = False

# Game Loop
while running:
    screen.fill((255, 255, 255))
    draw_button("trash", button_tra, (0, 0, 0))
    draw_button("recycle", button_recy, (75, 125, 255))
    draw_button("compost", button_comp, (45, 235, 75))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if image_rect.collidepoint(event.pos):
                dragging = True
                mouse_x, mouse_y = event.pos
                offset_x = image_rect.x - mouse_x
                offset_y = image_rect.y - mouse_y

        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False

            # Check drop zones on button release
            if image_rect.colliderect(button_tra):
                if trash_item[item_spawned] == "trash":
                    score += 1
                item_spawned, image, image_rect = spawn_item()
            elif image_rect.colliderect(button_recy):
                if trash_item[item_spawned] == "recycle":
                    score += 1
                item_spawned, image, image_rect = spawn_item()
            elif image_rect.colliderect(button_comp):
                if trash_item[item_spawned] == "compost":
                    score += 1
                item_spawned, image, image_rect = spawn_item()

        elif event.type == pygame.MOUSEMOTION and dragging:
            mouse_x, mouse_y = event.pos
            image_rect.x = mouse_x + offset_x
            image_rect.y = mouse_y + offset_y

    # Draw trash item
    screen.blit(image, image_rect)

    # Timer and score display
    seconds = (pygame.time.get_ticks() - start_ticks) // 1000
    remaining = max(0, 120 - seconds)
    mins = remaining // 60
    secs = remaining % 60
    timer_text = f"{mins}:{secs:02d}"
    score_text = f"Score: {score}"

    timer_surface = font.render(f"Time: {timer_text}", True, (0, 0, 0))
    score_surface = font.render(score_text, True, (0, 0, 0))
    screen.blit(timer_surface, (20, 20))
    screen.blit(score_surface, (560, 20))
    if show_x == True:
        screen.blit()
        pygame.mixer.Sound.play()


    pygame.display.flip()
    clock.tick(60)

pygame.quit()