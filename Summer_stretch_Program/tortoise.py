#author: Lawrence Chen
#Date: 7/1/2025

import turtle
import random


steps = 100

turtle.speed(50)
turtle.hideturtle
turtle.forward(100)
#for times in range (36):
    for c in ('blue', 'red', 'green'):
        turtle.color(c)
        turtle.forward(steps)
        turtle.backward(steps)
        turtle.right(10)
        turtle.done

         


random_number = random.randint(1,10)
print(random_number)