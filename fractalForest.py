import turtle as tt
from random import randint

# Setup the screen
screen = tt.Screen()
screen.bgcolor("#D4E4C9")  # Light greenish background for a glowing effect

# Draw the glowing background (simplified)
def draw_background():
    bg = tt.Turtle()
    bg.hideturtle()
    bg.speed(0)
    bg.penup()
    bg.goto(0, 200)
    bg.pendown()
    bg.pencolor("#FFFF99")  # Light yellow for glow
    bg.fillcolor("#FFFF99")
    bg.begin_fill()
    bg.circle(100)  # Sunlight glow effect
    bg.end_fill()

# Draw grass with flowers
def draw_grass_and_flowers():
    grass = tt.Turtle()
    grass.hideturtle()
    grass.speed(0)
    grass.pensize(2)
    
    # Draw grass
    for x in range(-400, 400, 5):
        grass.penup()
        grass.goto(x, -300)
        grass.pendown()
        grass.pencolor("#228B22")  # Forest green
        grass.setheading(randint(70, 110))
        grass.forward(randint(30, 60))
    
    # Draw flowers
    for x in range(-400, 400, 20):
        grass.penup()
        grass.goto(x + randint(-5, 5), -300 + randint(0, 20))
        grass.pendown()
        grass.pencolor("#FF4040")  # Red flowers
        grass.dot(5)

# Draw a single tree using L-system (from your original code)
def draw_tree(t, start_x, start_y, thick, itr, dl, angl):
    t.penup()
    t.goto(start_x, start_y)
    t.pendown()
    t.setheading(90)
    t.pencolor('#490000')  # Brown trunk
    t.pensize(thick)
    
    axiom = "22220"
    axmTemp = ""
    stc = []
    randint_low = 0
    randint_high = 10
    
    translate = {"1": "21",
                 "0": "1[-20]+20"}
    
    # L-system generation
    for k in range(itr):
        for ch in axiom:
            if ch in translate:
                axmTemp += translate[ch]
            else:
                axmTemp += ch
        axiom = axmTemp
        axmTemp = ""
    
    # Draw the tree
    for ch in axiom:
        if ch == "+":
            t.right(angl - randint(-13, 13))
        elif ch == "-":
            t.left(angl - randint(-13, 13))
        elif ch == "2":
            if randint(randint_low, randint_high) > 4:
                t.forward(dl)
        elif ch == "1":
            if randint(randint_low, randint_high) > 6:
                t.forward(dl)
        elif ch == "0":  # Leaves with varied colors
            stc.append(t.pensize())
            t.pensize(4)
            r = randint(randint_low, randint_high)
            
            colors = [
                '#009900', '#4F9900', '#ED9121', '#D2691E',
                '#C0A000', '#CD2626', '#667900', '#EEAD0E',
                '#BDB76B', '#DC143C'
            ]
            t.pencolor(colors[r % len(colors)])
            
            t.forward(dl)
            t.pensize(stc.pop())
            t.pencolor('#490000')
        elif ch == "[":
            thick = thick * 0.75
            t.pensize(thick)
            stc.append(thick)
            stc.append(t.xcor())
            stc.append(t.ycor())
            stc.append(t.heading())
        elif ch == "]":
            t.penup()
            t.setheading(stc.pop())
            t.sety(stc.pop())
            t.setx(stc.pop())
            thick = stc.pop()
            t.pensize(thick)
            t.pendown()

# Draw background trees (simplified)
def draw_background_trees():
    bg_tree = tt.Turtle()
    bg_tree.hideturtle()
    bg_tree.speed(0)
    
    for x in range(-400, 400, 80):
        if abs(x) > 100:  # Avoid overlapping with the central tree
            bg_tree.penup()
            bg_tree.goto(x, -200)
            bg_tree.pendown()
            bg_tree.pencolor("#3C2F2F")  # Darker brown for background trees
            bg_tree.pensize(8)
            bg_tree.setheading(90)
            bg_tree.forward(150)
            bg_tree.pencolor("#4F9900")  # Pine green
            bg_tree.pensize(4)
            for _ in range(3):
                bg_tree.forward(30)
                bg_tree.left(120)

# Main drawing function
def draw_forest_scene():
    tt.tracer(0)  # Turn off animation for faster drawing
    
    # Draw background elements
    draw_background()
    draw_background_trees()
    draw_grass_and_flowers()
    
    # Draw the central tree
    central_tree = tt.Turtle()
    central_tree.hideturtle()
    central_tree.speed(0)
    draw_tree(central_tree, 0, -200, 16, 12, 10, 16)
    
    tt.update()  # Update the screen
    tt.mainloop()

# Run the drawing
draw_forest_scene()