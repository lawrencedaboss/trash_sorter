import random

health_loss = random.randint(1, 75)
levels_gained = health_loss/10

gold = 0
level=1
has_weapon=False
health=75
has_magic_ring = False
has_armor = False


print("You have no gold, or armor and you only have a shortsword, though you know how to use it well. You are level 1.")
print(" You start looking for ways to get some gold.")
print()







#purchasing things

up_lvl = input("Would you like to purchase a magic level up scroll? It increases your level by one and it " 
"costs 10 gold. Please type yes or no.")

if up_lvl == "yes":
    gold-= 10
    level += 1


buy_gear = input("Would you like to purchase some armor? It costs 20 gold per level. Teher is armor from levels 1-5, and each. Please type yes or no.")

if up_lvl == "yes":
    gold-= 20
    has_weapon = True


trip = input("Would you scearch for a magic ring? It has unique properties, but it could be dangerous." 
"Please type yes or no.")

if trip == "yes":
    health -= health_loss
    has_magic_ring = True

if health <= 0:
    print("You died attempting to find the magic ring. ")
else:
    print("You found the magic ring, and gained", levels_gained, "but you lost", health_loss, "health in the process")    

buy_pot = input("Would you like to purchase a health potion? It heals you 10 health and it " 
"costs 15 gold. Please type yes or no.")

if buy_pot == "yes":
    pots = input("How many health potions would you like to buy?")
    print("You successfully bought", pots, "health potions. You drink them and get high. You feel healed once the high ends.")
    heal= int(pots)*15
    health += heal




#entering boss area
if has_magic_ring == False:
    if level>=5:
        if health>= 50:
            if has_weapon == True or has_armor == True:
                print("Your ready for battle!")
            else:
                print("You need a better equipment to fight!")
        else:
            print("Heal up before you fight!")        
    
    else:
        print("Level up before entering this area.")
else:
    if health >= 40:
        print("The magic ring grants you access")     
    else:
            print("Heal up before you fight!")  