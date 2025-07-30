
import random 
import time


gold = 50
level=1
has_weapon=False
health=40+8*(level-1)
max_health = 40+8*(level-1)
has_magic_ring = False
has_armor = False
armor_class = 6 + level
if has_armor == True:
    armor_class += 2




#sleep
def sleep(health, max_health):
    max_health=40+8*(level-1)
    night = random.randint(-10,10)
    if night >0:
        print("You get a good night's sleep and heal", night, "health.")
    else:
        if night<0:
            print("You try to get some rest but stay awake all night. You lost", night, "health.")
    health += int(night)
    return health, max_health





#death mechanic
def death():
    print()
    print()
    print()
    print("You have died! please reload to play again.")
    quit(0)
    





#combat mechanics
def combat(level, difficulty, damage_potential, enemy_health, enemy, armor_class, health):
    initiative = random.randint(1, 20)+level-1
    enemy_initiative = random.randint(1,20)+difficulty-1
        
    if enemy_initiative >= initiative:
         print("The", enemy, "reacts faster then you and goes first.")
         enemy_attack_roll = random.randint(1,20)+difficulty
         if enemy_attack_roll >= armor_class:
            enemy_damage = random.randint(difficulty, damage_potential)
            health -= enemy_damage
            print("The", enemy, "hits you and deals", enemy_damage, "damage. You have", health, "health left")
         else:
            print("The", enemy, "attempts to attack you but misses.")       
         print()
         time.sleep(3)
         while enemy_health>0 and health > 0:
                attack_roll = random.randint(1, 20)+int(level)
                if attack_roll >= 12+difficulty:
                    damage = random.randint(1, 10)+2*int(level)
                    enemy_health -=damage
                    print("You attack the", enemy, "and deal", damage, "damage. It has", enemy_health, "health left")
                    
                else:
                    print("You miss the", enemy)  
                      
                time.sleep(3)
                print()
                if enemy_health>0:
                    enemy_attack_roll = random.randint(1,20)+difficulty
                    if enemy_attack_roll >= armor_class:
                        enemy_damage = random.randint(difficulty, damage_potential)
                        health -= enemy_damage
                        print("The", enemy, "hits you and deals", enemy_damage, "damage. You have", health, "health left")
                    else:
                        print("The", enemy, "attempts to attack you but misses.")       
                    time.sleep(3)
                    print()
         if health >0:
            return health
         else:  
             death()     

    else:
        print("You manage to react first.")
        attack_roll = random.randint(1, 20)+level
        if attack_roll >= 12+difficulty:
            damage = random.randint(1, 12)+2*level
            enemy_health -= damage
            print("You attack the", enemy, "and deal", damage, "damage. It has", enemy_health, "health left")
        else:
            print("You miss the", enemy)   
        time.sleep(3)
        print()
        while enemy_health>0 and health > 0:
            enemy_attack_roll = random.randint(1,20)+difficulty
            if enemy_attack_roll >= armor_class:
                enemy_damage = random.randint(difficulty, damage_potential)
                health -= enemy_damage
                print("The", enemy, "hits you and deals", enemy_damage, "damage. You have", health, "health left")
            else:
                print("The", enemy, "attempts to attack you but misses.")       
            time.sleep(3)  
            print()      
            if health>0:
                attack_roll = random.randint(1, 20)+level
                if attack_roll >= 12+difficulty:
                    damage = random.randint(1, 12)+2*level
                    enemy_health -=damage
                    print("You attack the", enemy, "and deal", damage, "damage. It has", enemy_health, "health left")
                else:
                    print("You miss the", enemy)   
                time.sleep(3)
                print()
    
            else:
                death()
        if health >0:
            return health
        else:  
             death()                  




def goblins(health, gold, level, armor_class):
    #goblins
    goblins = input("Do you want to fight, or try to talk it into leaving? Answer in the format: talk or fight.")
    print()
    if goblins == "fight":
        print("The goblin charges you. You draw your sword and get ready")
        time.sleep(3)
        combat(int(level), 1, 12, 30, "goblin", armor_class, health)
        level += 2
        gold+=30
        return gold, level, health



            
    else:
        if goblins == "talk":
            print("You attempt to bribe the goblins to depart in peace.")
            print()
            gold_lost = random.randint(-gold, gold)

            if gold_lost > 0:
                print("You manage to bribe the goblins with", gold_lost,"gold.")
                time.sleep(2)
                gold -=gold_lost
                return gold

            else:
                print("You fail to bribe the goblins")
                time.sleep(2)
                combat(int(level), 1, 12, 30, "goblin", armor_class, health)
                level+=2
                gold+=30
                return health, gold, level







#day2 bugbear 
def bugbear(health, gold, level, armor_class):
    print("Despite the ecounter on the first day, everything is quiet on the second day.")
    time.sleep(4)
    print("But, just as you let down your guard a bugbear comes from behind and stabs you")
    time.sleep(4)
    health -= 15
    print("You take 15 damage and have", health, "left")
    time.sleep(4)
    print("You draw your sword and attack")
    combat(int(level), 3, 15, 50, "bugbear", armor_class, health)
    if health>0:
        print("The bugbear falls with a crash.")
        print()
        print("Well done!")
        print("You find 50 gold on its body")
        gold+=50
        level+=2
        return health, gold, level
    else:
        death()    





#buying things at the market
def market():
    print("On the third day, you find a market filled with people, most of them adventurers, due to the reclsive location of the market.")
    print("The market is selling food, clothes, adventuring gear, or even just a place to stay, and rest.")
    print("2 types of items catch your eye: armor, and health potions")
    







#beginning storyline
def intro():
    print("You have 75 health, have no gold, or armor and you only have a shortsword, though you know how to use it well. You are level 1.")
    time.sleep(3)
    print()
    print(" You start looking for ways to get some gold.")
    time.sleep(3)
    print()


    print("You ask around for anywhere jobs, but you can't seem to find anything.")
    print()
    time.sleep(4)
    print("Eventually, you learn that about bartender named Thorinton who gives out unusually dangerous jobs, and pays well.")
    print()
    time.sleep(5)
    

    print("After deciding to head to his tavern, you arrive to see a bustling tavern with battered sign that reads: The Bloodied Mug.")
    time.sleep(6)
    print()
    print("You ask Thorinton if there are any jobs available and he says: Only one, but it will be dangerous, so it's not for the faint of heart.")
    time.sleep(6)
    print()
    print("But you insist, so he sighs and gets up. He says: Alright then, I have a package I have to send to Waterdeep and I need someone to guard it. It's only a week on horseback but the road is filled with monsters.")
    print()
    time.sleep(8)
    print("One day later, you set off. On the first day you encounter a goblin. It asks for your valuables as it draws a dagger.")
    print()
    time.sleep(4)







#actual storyline
intro()
    
    

print()
health, gold, level = goblins(health, gold, int(level), armor_class)
time.sleep(3)
health, max_health = sleep(health, max_health)
health, gold, level = bugbear(health, gold, int(level), armor_class)