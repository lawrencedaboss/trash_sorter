import random

class Pet:
    def __init__(self, hunger, happiness, energy, name, cleanliness):
        self.cleanliness = cleanliness
        self.hunger = hunger
        self.energy = energy
        self.happiness = happiness
        print(f"Your kitten's name is {name}.")

    def status(self):
        print(f"happiness is: {self.happiness}. hunger is: {self.hunger}. energy is: {self.energy}. cleanliness is: {self.cleanliness}")
        self.hunger -= 15
        self.happiness -= 15
        self.energy -= 15
        self.cleanliness -= 15

    def sleep(self):
        energy_increase = random.randint(20, 51)
        self.energy += energy_increase
        print(f"Your energy increased by {energy_increase}. Your new energy is {self.energy}.")

    def feed(self):
        hunger_increase = random.randint(20, 51)
        self.hunger += hunger_increase
        print(f"Your hunger increased by {hunger_increase}. Your new hunger is {self.hunger}.")

    def play(self):
        happiness_increase = random.randint(20, 51)
        self.happiness += happiness_increase
        print(f"Your happiness increased by {happiness_increase}. Your new happiness is {self.happiness}.")

class Cat(Pet):
    def __init__(self, hunger, happiness, energy, name, cleanliness):
        super().__init__(hunger, happiness, energy, name, cleanliness)
        print(f"cleanliness is: {self.cleanliness}")

    def groom(self):
        cleanliness_increase = random.randint(25, 51)
        self.cleanliness += cleanliness_increase
        print(f"Your cleanliness increased by {cleanliness_increase}. New cleanliness is {self.cleanliness}")
        if self.cleanliness <= 0:
            self.happiness -= 25
            self.energy -= 25
            print(f"Your cat isn't clean enough, so Energy and happiness dropped. New energy is {self.energy}, New happiness is {self.happiness}")

name_choice = input("Choose a name for your kitten: ")

cat = Cat(75, 75, 75, name_choice, 50)

while cat.happiness >0 and cat.hunger >0 and cat.energy >0:
    cat.status()
    action = input("What would you like to do with your cat? play, groom, feed, or sleep: ").strip().lower()
    if action == "sleep":
        cat.sleep()
    elif action == "play":
        cat.play()
    elif action == "groom":
        cat.groom()
    elif action == "feed":
        cat.feed()
print(f"happiness is: {Pet.happiness}. hunger is: {Pet.hunger}. energy is: {Pet.energy}. cleanliness is: {Pet.cleanliness}")
print("Your cat died because you didn't take care of it.")
