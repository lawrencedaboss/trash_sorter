
import turtle as t
import turtle as tu
import random

x=100


myrtle = t.Turtle()
tur = tu.Turtle()
t.colormode(255)


def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    color = (r, g, b)
    return color

def draw_spirograph(size_of_gap):
    for _ in range(int(360 / size_of_gap)):
        myrtle.circle(60)
        myrtle.setheading(myrtle.heading() + 10)

def draw_spiro(size_of_gap):
    for _ in range(int(360 / size_of_gap)):
        tur.circle(70)
    
        tur.setheading(tur.heading() + 10)




t.speed(150)
draw_spirograph(5)
draw_spiro(5)
