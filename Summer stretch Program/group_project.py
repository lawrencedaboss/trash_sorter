user_name = input("Your name is:")
player_stats = {
    "Name":user_name,
    "Health": 100,
    "Energy": 75,
    "Hydration": 100,
    "Day": 1
}

def eat():
    print ("You feel hungry, do you want to eat?")
    action = input("yes or no ")
    if (action == "yes"):
        player_stats ["Energy"] += 10
        player_stats ["Health"] += 5
        print (player_stats)
        rand_action()
    else:
        player_stats ["Energy"] -= 10
        player_stats ["Health"] -= 5
        print ("You skipped a meal... - 10 energy -5 health")
        rand_action()
def hydration():
    print ("You feel thirsty, do you want to drink? ")
    action_hydration = input("yes or no ")
    if (action_hydration == "yes"):
        player_stats ["Hydration"] += 10
        player_stats ["Health"] += 2
        print (player_stats)
        rand_action()
    else:
        player_stats ["Hydration"] -= 10
        player_stats ["Health"] -= 2
        print ("You didn't drink water... -10 Hydration. -2 Health")
        rand_action()
def health():
    print ("Do you want to sleep")
    action_health = input("yes or no ")
    if (action_health == "yes"):
        player_stats ["Energy"] += 15
        player_stats ["Health"] += 10
        print (player_stats)
        player_stats ["Day"] += 1
        print (f"You've moved on to day {player_stats['Day']}")
        rand_action()
    else:
        print ("You die")
        quit()
   
def rand_action():
    import random
    activity = random.randint (1,3)
    if (activity == 1):
         health()
    elif (activity == 2):
         hydration()
    else:
         eat()
rand_action()
file = open("./gamesave.txt", "w")
file.write(player_stats)
file.close()