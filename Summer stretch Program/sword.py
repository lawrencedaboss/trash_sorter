#import
import turtle
import turtle as t
import turtle as f

# Set up "e"
e = turtle.Turtle()
e.pencolor("white")
e.right(90)
e.forward(150)
e.left(90)

# Set the fill color
e.fillcolor("aqua")
e.pencolor("black")
# Start filling
e.begin_fill()

# Draw a custom shape (triangle)
e.left(87.5)
e.forward(400)
e.right(175)
e.forward(400)
e.right(2.5)

#end "e"
e.end_fill()
e.hideturtle

#set up "t"
t.pencolor("white")
t.right(90)
t.forward(150)
t.left(90)
t.forward(34.89551)
t.fillcolor("gold")
t.pencolor("black")
t.begin_fill()

#draw arc1
t.circle(30, extent=60)
t.right(150)
t.circle(-30, extent=80)

#repostion and draw handle
t.left(80)
t.forward(75)
t.right(90)
t.forward(34.89551)
t.right(90)
t.forward(75)
t.left(80)

#draw arc2
t.circle(-30, extent=80)
t.right(150)
t.circle(30, extent=60)


# Finish and end filling
t.forward(34.89551)
t.end_fill()
t.hideturtle


#postition lightning
f.pencolor("white")
f.penup()
f.forward(17.447755)
f.right(90)
f.forward(30)
f.left(90)
f.pendown

#draw lightning
f.right(20)
f.forward(10)
f.left(15)
f.forward(20)
f.right(20)
f.forward(20)

#end drawing
f.hideturtle()


# Keep the window open
turtle.done()