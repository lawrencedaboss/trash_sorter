import pygame, random, threading, time, os

def main():
    BASE_DIR = os.path.dirname(__file__)
    pygame.init()
    pygame.mixer.init()

    # Audio
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
        "cardboard_box.png": "recycle",
        "pizza_box.png": "trash"
    }
    trash_item_choice = {i + 1: key for i, key in enumerate(trash_item)}

    def spawn_item():
        choice = random.randint(1, len(trash_item))
        item_name = trash_item_choice[choice]
        item_type = trash_item[item_name]
        image = pygame.image.load(os.path.join(BASE_DIR, item_name))
        width, height = image.get_size()
        image = pygame.transform.scale(image, (width // 9, height // 9))
        location_x = random.randint(0, 700 - width // 9)
        location_y = random.randint(0, 400 - height // 9)
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
    running = True
    game = False
    show_start_screen = True

    # Feedback
    feedback_start_time = 0
    feedback_duration = 600
    feedback_type = None

    # UI
    button_tra = pygame.Rect(75, 500, 120, 45)
    button_recy = pygame.Rect(500, 500, 120, 45)
    button_comp = pygame.Rect(305, 500, 120, 45)
    start_button = pygame.Rect(250, 400, 200, 60)

    def draw_button(text, rect, color):
        pygame.draw.rect(screen, color, rect)
        txt_surface = font.render(text, True, (255, 255, 255))
        screen.blit(txt_surface, txt_surface.get_rect(center=rect.center))

    def draw_start_screen():
        screen.fill((200, 225, 255))
        screen.blit(font.render("Welcome to Trash Sorter!", True, (0, 0, 0)),
                    font.render("Welcome to Trash Sorter!", True, (0, 0, 0)).get_rect(center=(350, 150)))
        screen.blit(font.render("Sort items into trash, recycle, or compost.", True, (50, 50, 50)),
                    font.render("Sort items into trash, recycle, or compost.", True, (50, 50, 50)).get_rect(center=(350, 220)))
        pygame.draw.rect(screen, (0, 100, 200), start_button)
        screen.blit(font.render("Start Game", True, (255, 255, 255)),
                    font.render("Start Game", True, (255, 255, 255)).get_rect(center=start_button.center))

    correct, incorrect, check, x = spawn_answer()
    score = 0
    start_ticks = 0
    dragged_item = None

    def item_spawner():
        while running:
            if game:
                with lock:
                    items.append(spawn_item())
                time.sleep(2)

    spawner_thread = threading.Thread(target=item_spawner)
    spawner_thread.start()

    # Game loop
    while running:
        screen.fill((255, 255, 255))

        if show_start_screen:
            draw_start_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.collidepoint(event.pos):
                        show_start_screen = False
                        game = True
                        start_ticks = pygame.time.get_ticks()

        else:
            draw_button("trash", button_tra, (0, 0, 0))
            draw_button("recycle", button_recy, (75, 125, 255))
            draw_button("compost", button_comp, (45, 235, 75))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if game:
                    if event.type == pygame.MOUSEBUTTONDOWN:
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
                        item_type = dragged_item["type"]
                        item_rect = dragged_item["rect"]
                        feedback_start_time = pygame.time.get_ticks()
                        feedback_type = None

                        if item_rect.colliderect(button_tra):
                            feedback_type = "correct" if item_type == "trash" else "incorrect"
                        elif item_rect.colliderect(button_recy):
                            feedback_type = "correct" if item_type == "recycle" else "incorrect"
                        elif item_rect.colliderect(button_comp):
                            feedback_type = "correct" if item_type == "compost" else "incorrect"

                        if feedback_type == "correct":
                            check_sound.play()
                            score += 1
                        elif feedback_type == "incorrect":
                            x_sound.play()

                        with lock:
                            if dragged_item in items:
                                items.remove(dragged_item)
                        dragged_item = None

                    elif event.type == pygame.MOUSEMOTION and dragged_item:
                        mouse_x, mouse_y = event.pos
                        dragged_item["rect"].x = mouse_x + dragged_item["offset_x"]
                        dragged_item["rect"].y = mouse_y + dragged_item["offset_y"]

            if game:
                with lock:
                    for item in items:
                        screen.blit(item["surface"], item["rect"])

                seconds = (pygame.time.get_ticks() - start_ticks) // 1000
                remaining = max(0, 60 - seconds)
                timer_text = f"{remaining // 60}:{remaining % 60:02d}"
                screen.blit(font.render(f"Time: {timer_text}", True, (0, 0, 0)), (20, 20))
                screen.blit(font.render(f"Score: {score}", True, (0, 0, 0)), (560, 20))

                current_time = pygame.time.get_ticks()
                if feedback_type == "correct" and current_time - feedback_start_time < feedback_duration:
                    screen.blit(correct, check)
                elif feedback_type == "incorrect" and current_time - feedback_start_time < feedback_duration:
                    screen.blit(incorrect, x)

                if remaining == 0:
                    game = False
            else:
                screen.fill((0, 0, 100))
                txt_surface = font.render(f"Time's up! Final score: {score}", True, (255, 255, 255))
                screen.blit(txt_surface, txt_surface.get_rect(center=(350, 300)))

        pygame.display.flip()
        clock.tick(60)
    running = False
    spawner_thread.join()
    pygame.quit()

if __name__ == "__main__":
    main()
