# Q3_dynamic_fractal_polygon.py
# Draw a regular polygon with recursive "Koch-style" indentations along each edge.
# Inputs: number of sides, side length (acts as radius), recursion depth, and indentation direction.
#
# Keys: S = save EPS, Q = quit

import turtle as T
import math

# ---------- Geometry helpers ----------

def generate_polygon_points(num_sides: int, radius: float, rotation_deg: float = -90.0):
    """
    Regular polygon centered at (0,0). rotation_deg=-90 makes the first vertex point up.
    Returns list of (x, y) vertices in CCW order.
    """
    pts = []
    for i in range(num_sides):
        ang = math.radians(rotation_deg + 360.0 * i / num_sides)
        x = radius * math.cos(ang)
        y = radius * math.sin(ang)
        pts.append((x, y))
    return pts

def transform_edge(start, end, inward: bool = True):
    """
    Koch-style transform for a single edge:
      Split the segment into thirds -> p1, p2.
      Build an equilateral 'dent' on p1--p2 with apex offset perpendicular to the base.
      'inward' selects the perpendicular direction (flip if you want outward spikes).
    Returns a list of 4 sub-edges: [(start,p1), (p1,apex), (apex,p2), (p2,end)]
    """
    x1, y1 = start
    x2, y2 = end
    dx, dy = (x2 - x1), (y2 - y1)

    # Division points at 1/3 and 2/3
    p1 = (x1 + dx / 3.0, y1 + dy / 3.0)
    p2 = (x1 + 2.0 * dx / 3.0, y1 + 2.0 * dy / 3.0)

    # Base (p1 -> p2)
    bx, by = (dx / 3.0, dy / 3.0)
    base_len = math.hypot(bx, by)
    if base_len == 0:
        # Degenerate edge: return straight piece
        return [(start, end)]

    # Height of equilateral triangle with base = base_len
    # height = (sqrt(3)/2) * base_len
    h = (math.sqrt(3) / 2.0) * base_len

    # Unit perpendicular to the base (choose orientation via 'inward')
    # Perp vectors to (bx,by) are (+-by, -+bx). Normalize then scale by height.
    nx, ny = (-by / base_len, bx / base_len)   # one of the perpendiculars
    indent_sign = -1.0 if inward else 1.0
    offx, offy = (indent_sign * h * nx, indent_sign * h * ny)

    # Apex at midpoint of p1-p2, then offset by perpendicular
    mx, my = ((p1[0] + p2[0]) / 2.0, (p1[1] + p2[1]) / 2.0)
    apex = (mx + offx, my + offy)

    return [(start, p1), (p1, apex), (apex, p2), (p2, end)]

def apply_fractal_recursively(edges, depth: int, inward: bool = True):
    """
    Recurse the transform across all edges 'depth' times.
    edges: list[(start,end)]
    """
    if depth <= 0:
        return edges
    new_edges = []
    for (a, b) in edges:
        new_edges.extend(transform_edge(a, b, inward=inward))
    return apply_fractal_recursively(new_edges, depth - 1, inward=inward)

# ---------- Drawing ----------

def edges_from_points(points):
    """Convert a closed polygon defined by vertices -> list of (start,end) edges."""
    edges = []
    n = len(points)
    for i in range(n):
        start = points[i]
        end = points[(i + 1) % n]
        edges.append((start, end))
    return edges

def draw_edges(edge_list, scale: float = 1.0):
    """
    Draw the edge list with Turtle. Auto-centers the figure roughly on screen.
    """
    # Compute bounds to center drawing
    all_pts = []
    for a, b in edge_list:
        all_pts.append(a); all_pts.append(b)
    xs = [p[0] for p in all_pts]; ys = [p[1] for p in all_pts]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    cx, cy = (min_x + max_x) / 2.0, (min_y + max_y) / 2.0

    T.reset(); T.hideturtle(); T.speed(0)
    T.pensize(2); T.pencolor("blue")

    # Start at first edge start
    (sx, sy), (ex, ey) = edge_list[0]
    T.penup(); T.goto((sx - cx) * scale, (sy - cy) * scale); T.pendown()
    T.goto((ex - cx) * scale, (ey - cy) * scale)

    # Continue through remaining edges
    last_end = (ex, ey)
    for (a, b) in edge_list[1:]:
        if a != last_end:
            # break in continuity: move without drawing
            T.penup(); T.goto((a[0] - cx) * scale, (a[1] - cy) * scale); T.pendown()
        T.goto((b[0] - cx) * scale, (b[1] - cy) * scale)
        last_end = b

def save_eps(filename="Q3_dynamic_fractal_polygon.eps"):
    try:
        T.getscreen().getcanvas().postscript(file=filename)
        print(f"Saved {filename}")
    except Exception as e:
        print("Could not save:", e)

def main():
    # ---- Inputs ----
    try:
        num_sides = int(input("Enter number of sides (>=3): ").strip())
    except:
        num_sides = 5
    if num_sides < 3:
        num_sides = 3

    try:
        side_length = float(input("Enter side length / radius (100–500 typical): ").strip())
    except:
        side_length = 180.0
    if side_length <= 0:
        side_length = 180.0

    try:
        recursion_depth = int(input("Enter recursion depth (0–3 typical): ").strip())
    except:
        recursion_depth = 1
    if recursion_depth < 0:
        recursion_depth = 0

    indent_mode = (input("Indent direction [inward/outward] (default inward): ").strip().lower() or "inward")
    inward = (indent_mode != "outward")

    # ---- Build base polygon -> edges ----
    pts = generate_polygon_points(num_sides, radius=side_length, rotation_deg=-90.0)
    edges = edges_from_points(pts)

    # ---- Apply fractal transform ----
    fractal_edges = apply_fractal_recursively(edges, recursion_depth, inward=inward)

    # ---- Draw ----
    draw_edges(fractal_edges, scale=1.0)

    # ---- Hotkeys ----
    scr = T.getscreen()
    scr.onkey(lambda: save_eps("Q3_dynamic_fractal_polygon.eps"), "s")
    scr.onkey(T.bye, "q")
    scr.listen()
    print("Tips: press 'S' to save EPS, 'Q' to quit.")
    T.done()

if __name__ == "__main__":
    main()
