# Q3_star_from_svg.py
# Recreates your SVG star polygon in Python Turtle.
# Press S to save an EPS image; Q to quit.

import turtle as T

# SVG points (viewBox -150..150, -150..150)
POINTS = [(0, -100), (29, 80), (-95, 31), (95, 31), (-29, 80)]

def draw_polygon(points, scale=1.0):
    T.reset(); T.hideturtle(); T.speed(0)
    T.pensize(2); T.pencolor("blue")
    T.penup(); T.goto(points[0][0]*scale, points[0][1]*scale); T.pendown()
    for x, y in points[1:]:
        T.goto(x*scale, y*scale)
    # close the polygon
    T.goto(points[0][0]*scale, points[0][1]*scale)

def save_eps(filename="Q3_star.eps"):
    try:
        T.getscreen().getcanvas().postscript(file=filename)
        print(f"Saved {filename}")
    except Exception as e:
        print("Could not save:", e)

def main():
    try:
        scale = float(input("Scale (1 = original SVG size): ").strip())
    except:
        scale = 1.0
    draw_polygon(POINTS, scale)
    scr = T.getscreen()
    scr.onkey(lambda: save_eps("Q3_star.eps"), "s")
    scr.onkey(T.bye, "q")
    scr.listen()
    print("Press 'S' to save as EPS, 'Q' to quit.")
    T.done()

if __name__ == "__main__":
    main()
