import turtle

def draw_square(turtle):
	i = 0
	while i < 4:	
		turtle.forward(100)
		turtle.right(90)
		i = i + 1

def draw_circle_square(turtle, turnAngle):
	base_angle = 360
	j = base_angle / turnAngle
	while j > 0:
		draw_square(turtle)
		turtle.right(turnAngle)
		j = j - 1

def draw():
	window = turtle.Screen()
	window.bgcolor('red')

	brad = turtle.Turtle()
	brad.color('green')
	brad.shape('classic')
	brad.speed(2)
	draw_circle_square(brad, 10)
	
	angie = turtle.Turtle()
	angie.circle(100)
	angie.shape('classic')	

	window.exitonclick()
draw()