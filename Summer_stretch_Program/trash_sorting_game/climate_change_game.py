import pygame, random, threading, time, os

BASE_DIR = os.path.dirname(__file__)

# Initialize Pygame and mixer
pygame.init()
pygame.mixer.init()

# Load and play background music
pygame.mixer.music.load(os.path.join(BASE_DIR, "elevator_music.wav"))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

x_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "Incorrect_sound.wav"))
check_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "Correct_sound.wav"))

# Trash logic
trash_item = {
    "banana.png": "compost",
    "plastic_water_bottle.png": "recycle",
    "apple_core.png": "compost",
    "can.png": "recycle",
    "carboard_box.png": "recycle",
    "pizza_box.png": "trash",
}

trash_item_choice = {i + 1: key for i, key in enumerate(trash_item)}

def spawn_item():
    choice = random.randint(1, 6)
    item_name = trash_item_choice[choice]
    item_type = trash_item[item_name]
    image = pygame.image.load(os.path.join(BASE_DIR, item_name))
    width, height = image.get_size()
    image = pygame.transform.scale(image, (width // 9, height // 9))
    location_x = random.randint(1, 500)
    location_y = random.randint(1, 400)
    rect = image.get_rect(topleft=(location_x, location_y))

    return {
        "name": item_name,
        "type": item_type,
        "surface": image,
        "rect": rect,
        "dragging": False,
        "offset_x": 0,
        "offset_y": 0
    }

def spawn_answer():
    correct = pygame.image.load(os.path.join(BASE_DIR, "check.png"))
    incorrect = pygame.image.load(os.path.join(BASE_DIR, "x.png"))
    correct = pygame.transform.scale(correct, (100, 100))
    incorrect = pygame.transform.scale(incorrect, (100, 100))
    check = correct.get_rect(center=(350, 300))
    x = incorrect.get_rect(center=(350, 300))
    return correct, incorrect, check, x

# Setup
screen = pygame.display.set_mode((700, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)
pygame.display.set_caption("Trash Sorter Game")

items = []
lock = threading.Lock()

# Feedback State
feedback_start_time = 0
feedback_duration = 600  # milliseconds
feedback_type = None  # "correct" or "incorrect"

def item_spawner():
    while running:
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
correct, incorrect, check, x = spawn_answer()
score = 0
start_ticks = pygame.time.get_ticks()
dragged_item = None
running = True
spawner_thread = threading.Thread(target=item_spawner)
spawner_thread.start()

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
            with lock:
                for item in reversed(items):
                    if item["rect"].collidepoint(event.pos):
                        item["dragging"] = True
                        mouse_x, mouse_y = event.pos
                        item["offset_x"] = item["rect"].x - mouse_x
                        item["offset_y"] = item["rect"].y - mouse_y
                        dragged_item = item
                        break

        elif event.type == pygame.MOUSEBUTTONUP and dragged_item:
            dragged_item["dragging"] = False
            item_type = dragged_item["type"]
            item_rect = dragged_item["rect"]

            feedback_start_time = pygame.time.get_ticks()

            if item_rect.colliderect(button_tra):
                if item_type == "trash":
                    score += 1
                    feedback_type = "correct"
                    check_sound.play()
                else:
                    feedback_type = "incorrect"
                    x_sound.play()
                with lock:
                    items.remove(dragged_item)

            elif item_rect.colliderect(button_recy):
                if item_type == "recycle":
                    score += 1
                    feedback_type = "correct"
                    check_sound.play()
                else:
                    feedback_type = "incorrect"
                    x_sound.play()
                with lock:
                    items.remove(dragged_item)

            elif item_rect.colliderect(button_comp):
                if item_type == "compost":
                    score += 1
                    feedback_type = "correct"
                    check_sound.play()
                else:
                    feedback_type = "incorrect"
                    x_sound.play()
                with lock:
                    items.remove(dragged_item)

            dragged_item = None

        elif event.type == pygame.MOUSEMOTION and dragged_item:
            mouse_x, mouse_y = event.pos
            dragged_item["rect"].x = mouse_x + dragged_item["offset_x"]
            dragged_item["rect"].y = mouse_y + dragged_item["offset_y"]

    # Draw items
    with lock:
        for item in items:
            screen.blit(item["surface"], item["rect"])

    # Timer and score display
    seconds = (pygame.time.get_ticks() - start_ticks) // 1000
    remaining = max(0, 60 - seconds)
    timer_text = f"{remaining // 60}:{remaining % 60:02d}"
    score_text = f"Score: {score}"

    timer_surface = font.render(f"Time: {timer_text}", True, (0, 0, 0))
    score_surface = font.render(score_text, True, (0, 0, 0))
    screen.blit(timer_surface, (20, 20))
    screen.blit(score_surface, (560, 20))

    # Show feedback if within duration
    current_time = pygame.time.get_ticks()
    if feedback_type == "correct" and current_time - feedback_start_time < feedback_duration:
        screen.blit(correct, check)
    elif feedback_type == "incorrect" and current_time - feedback_start_time < feedback_duration:
        screen.blit(incorrect, x)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()