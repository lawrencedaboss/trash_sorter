import pygame, sys, random

pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Epic RPG Adventure")
font = pygame.font.SysFont(None, 32)
clock = pygame.time.Clock()

# Background setup
background = pygame.Surface((WIDTH, HEIGHT))
background.fill((20, 15, 40))

def draw_background():
    screen.blit(background, (0, 0))

def draw(text, x, y, color=(255, 255, 255)):
    screen.blit(font.render(text, True, color), (x, y))

# Game state
MAX_PLAYERS = 4
players = []
day = 1
difficulty = "easy"

difficulty_mods = {
    "easy":   {"enemy_hp": 1.0, "enemy_dmg": 1.0, "heal": 1.5},
    "normal": {"enemy_hp": 1.3, "enemy_dmg": 1.2, "heal": 1.0},
    "hard":   {"enemy_hp": 1.6, "enemy_dmg": 1.4, "heal": 0.8},
    "extreme":{"enemy_hp": 2.0, "enemy_dmg": 1.7, "heal": 0.5}
}

CLASSES = {
    "Fighter":     {"hp":50, "ac":12, "weapon":(5,10),  "special":"Stun"},
    "Mage":        {"hp":30, "ac":6,  "weapon":(8,14),  "special":"Fireball"},
    "Rogue":       {"hp":35, "ac":10, "weapon":(4,8),   "special":"Backstab"},
    "Buffer":      {"hp":40, "ac":9,  "weapon":(2,4),   "special":"Battle Chant"},
    "Cleric":      {"hp":38, "ac":10, "weapon":(3,6),   "special":"Heal"},
    "Ranger":      {"hp":37, "ac":11, "weapon":(5,9),   "special":"Critical Shot"},
    "Necromancer": {"hp":32, "ac":8,  "weapon":(6,12),  "special":"Raise Skeletons", "skeletons":[]},
    "Mystic":      {"hp":34, "ac":9,  "weapon":(4,10),  "special":"Barrier"}
}

ELITE_SKELETONS = {
    "Bone Knight": {"hp":2, "damage":(6,10), "desc":"Armored melee unit with strong hits."},
    "Bone Archer": {"hp":1, "damage":(5,8),  "desc":"Ranged attacker that pierces armor."},
    "Bone Shaman": {"hp":1, "damage":(4,6),  "desc":"Magical skeleton that weakens enemies."}
}

def home_screen():
    global MAX_PLAYERS, difficulty
    selecting = True
    selected_players = 4
    difficulties = ["easy", "normal", "hard", "extreme"]

    while selecting:
        draw_background()
        draw("🎮 Welcome to Epic RPG Adventure", 260, 60)
        draw("Select Difficulty (1–4):", 100, 150)
        for i, lvl in enumerate(difficulties):
            prefix = ">" if difficulty == lvl else " "
            draw(f"{prefix} {i+1}. {lvl.capitalize()}", 120, 190 + i*30)

        draw("Select Number of Players (UP/DOWN):", 500, 150)
        draw(f"  {selected_players}", 550, 190)
        draw("Press ENTER to Start", 320, 500)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_KP1]:
                    difficulty = difficulties[0]
                elif event.key in [pygame.K_2, pygame.K_KP2]:
                    difficulty = difficulties[1]
                elif event.key in [pygame.K_3, pygame.K_KP3]:
                    difficulty = difficulties[2]
                elif event.key in [pygame.K_4, pygame.K_KP4]:
                    difficulty = difficulties[3]
                elif event.key == pygame.K_UP and selected_players < 4:
                    selected_players += 1
                elif event.key == pygame.K_DOWN and selected_players > 1:
                    selected_players -= 1
                elif event.key == pygame.K_RETURN:
                    MAX_PLAYERS = selected_players
                    selecting = False

        clock.tick(30)

def choose_classes():
    current = 1
    while current <= MAX_PLAYERS:
        draw_background()
        draw(f"Player {current}: Choose Class", 300, 50)
        for i, key in enumerate(CLASSES):
            draw(f"{i+1}. {key} — {CLASSES[key]['special']}", 100, 100 + i*40)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                keymap = {
                    pygame.K_1:0, pygame.K_KP1:0,
                    pygame.K_2:1, pygame.K_KP2:1,
                    pygame.K_3:2, pygame.K_KP3:2,
                    pygame.K_4:3, pygame.K_KP4:3,
                    pygame.K_5:4, pygame.K_KP5:4,
                    pygame.K_6:5, pygame.K_KP6:5,
                    pygame.K_7:6, pygame.K_KP7:6,
                    pygame.K_8:7, pygame.K_KP8:7,
                }
                if event.key in keymap:
                    idx = keymap[event.key]
                    cname = list(CLASSES.keys())[idx]
                    p = CLASSES[cname].copy()
                    p.update({
                        "name": f"Player{current}",
                        "class": cname,
                        "hp": p["hp"], "max_hp": p["hp"],
                        "level": 1,
                        "inventory": ["Health Potion"],
                        "skeletons": []
                    })
                    players.append(p)
                    current += 1

        clock.tick(30)

def choose_skeleton_type():
    while True:
        draw_background()
        draw("Choose your elite skeleton type:", 280, 50)
        for i, (name, info) in enumerate(ELITE_SKELETONS.items()):
            draw(f"{i+1}. {name} — {info['desc']}", 100, 120 + i*40)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_KP1]:
                    return "Bone Knight"
                elif event.key in [pygame.K_2, pygame.K_KP2]:
                    return "Bone Archer"
                elif event.key in [pygame.K_3, pygame.K_KP3]:
                    return "Bone Shaman"

        clock.tick(30)

def summon_skeletons(caster):
    caster["skeletons"] = []
    count = caster["level"] // 3
    for _ in range(count):
        if caster["level"] >= 15:
            choice = choose_skeleton_type()
            skel = ELITE_SKELETONS[choice].copy()
            skel["type"] = choice
        else:
            skel = {"type":"Skeleton", "hp":1, "damage":(3, 6 + caster["level"]//2)}
        caster["skeletons"].append(skel)

def combat(enemy_name, hp, ac, dmg):
    draw_background()
    draw(f"A {enemy_name} appears!", 300, 100)
    pygame.display.flip()
    pygame.time.delay(1500)

    for p in players:
        if p["class"] == "Necromancer":
            summon_skeletons(p)

    while hp > 0 and any(p["hp"] > 0 for p in players):
        # Player attacks
        for p in players:
            if p["hp"] <= 0:
                continue
            roll = random.randint(1, 20) + p["level"]
            if roll >= ac:
                d = random.randint(*p["weapon"])
                hp -= d
                draw_background()
                draw(f"{p['name']} hits for {d}!", 300, 150)
                pygame.display.flip()
                pygame.time.delay(500)

        # Skeleton attacks
        for p in players:
            if p["class"] == "Necromancer":
                for s in p["skeletons"]:
                    if s["hp"] > 0 and random.randint(1, 20) >= ac:
                        sd = random.randint(*s["damage"])
                        hp -= sd
                        draw_background()
                        draw(f"{s['type']} hits for {sd}!", 300, 200)
                        pygame.display.flip()
                        pygame.time.delay(500)

        # Enemy attacks
        for p in players:
            if hp <= 0:
                break
            if p["hp"] <= 0:
                continue
            if random.randint(1, 20) >= p["ac"]:
                ed = int(random.randint(*dmg) * difficulty_mods[difficulty]["enemy_dmg"])
                p["hp"] -= ed
                draw_background()
                draw(f"{enemy_name} hits {p['name']} for {ed}!", 300, 250)
                pygame.display.flip()
                pygame.time.delay(500)

    # Post-combat results
    if hp <= 0:
        for p in players:
            if p["hp"] > 0:
                p["level"] += 1
                p["hp"] = min(p["max_hp"],
                              int(p["hp"] + 10 * difficulty_mods[difficulty]["heal"]))
        draw_background()
        draw("Victory! You leveled up!", 300, 300)
        pygame.display.flip()
        pygame.time.delay(1500)
    else:
        draw_background()
        draw("You were defeated...", 300, 300)
        pygame.display.flip()
        pygame.time.delay(1500)

def run_day():
    global day
    draw_background()
    draw(f"🌄 Day {day}", 380, 50)

    story_lines = {
        1: "You begin your journey toward the fallen kingdom...",
        2: "A forked path leads into the wild...",
        3: "You stumble upon a ruined watchtower...",
        4: "A merchant offers gear in exchange for help...",
        5: "Bandits ambush your camp at night!",
        6: "A dark fog surrounds the valley...",
        7: "You meet a wounded ranger who warns of danger ahead.",
        8: "An ancient tablet glows as you pass...",
        9: "You feel watched — something lurks nearby.",
        10: "🔥 A dragon descends from the sky!",
        11: "Smoke rises from a distant battlefield...",
        12: "You traverse cursed ruins with magical traps.",
        13: "A necromancer beckons in a whispering crypt.",
        14: "A massive storm cuts off your advance.",
        15: "You rescue villagers from spectral attackers.",
        16: "An old friend joins your fight for justice.",
        17: "You sneak into the warlord's stronghold...",
        18: "Dark clouds swirl overhead — the final battle nears.",
        19: "You find the sword of prophecy buried beneath stone.",
        20: "👑 The Final Boss awaits at the throne of ruin!"
    }

    draw(story_lines.get(day, "The journey continues..."), 150, 120)
    pygame.display.flip()
    pygame.time.delay(2000)

    enemy_types = {
        10: ("Dragon", 180, 20, (12,20)),
        20: ("Warlord King", 250, 24, (18,30))
    }
    default_enemy = ("Shadow Beast", 100 + day*5, 12 + day//2, (6, 12 + day//3))
    enemy_info = enemy_types.get(day, default_enemy)
    enemy_name, base_hp, base_ac, base_dmg = enemy_info
    scaled_hp = int(base_hp * difficulty_mods[difficulty]["enemy_hp"])

    combat(enemy_name, scaled_hp, base_ac, base_dmg)
    day += 1

def final_victory():
    draw_background()
    draw("🎉 The Warlord has fallen! Peace returns to the realm.", 180, 150)
    draw("Congratulations to the heroes:", 320, 200)
    for i, p in enumerate(players):
        y = 250 + i*80
        draw(f"{p['name']} the {p['class']} — Level {p['level']}", 280, y)
        draw(f"HP: {p['hp']}/{p['max_hp']}", 280, y+20)
        if p['class'] == "Necromancer":
            draw(f"Skeletons: {len(p['skeletons'])}", 280, y+40)
    draw("Thanks for playing Epic RPG Adventure!", 260, y+80)
    pygame.display.flip()
    pygame.time.delay(7000)

def main():
    home_screen()
    choose_classes()
    while day <= 20:
        run_day()
    final_victory()
    pygame.quit()

if __name__ == "__main__":
    main()
