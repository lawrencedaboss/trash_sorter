import turtle as t
wn = t.Screen
t.hideturtle()
t.hideturtle()
t.ht()
t.speed(0)

t.pensize(11)




t = t.Turtle()



t.color("black")
t.circle(60, extent=60)
t.right(150)
t.circle(-60, extent=80)



cv = t.getcanvas()
cv.postscript(file="circle.ps", colormode='color')

t.done()