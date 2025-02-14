import math
import random
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np

# Variables to change (min polygon vertices: 3 and min step: 1)
polygon_start_verteces = 5
polygon_end_verteces = 3
interpolation_steps = 3

# Generate polygons by giving n which is a number and func return list with tuplets
def generate_polygon_vertices(n):
    if n < 3:
        raise ValueError("A polygon must have at least 3 vertices.")
    r = 4 
    polygon_vertices = []
    angle_deg = 360 / n
    
    for i in range(n):
        angle = math.radians(angle_deg * i)  # Convert to radians
        x = r * round(math.cos(angle),4)
        y = r * round(math.sin(angle),4)
        polygon_vertices.append((x, y))  
        
    return polygon_vertices

def remove_vertex(polygon_verteces):
    if len(polygon_verteces) == 0:
        return polygon_verteces
        
    random_index = random.randint(0, len(polygon_verteces) - 1)
    polygon_verteces.pop(random_index)

def add_vertex(polygon_verteces):
    if len(polygon_verteces) == 0:
        return polygon_verteces
    
    random_index = random.randint(0, len(polygon_verteces) - 1)

    vertex_before = polygon_verteces[random_index]
    # Takes first vertex if out bounds
    vertex_after = polygon_verteces[(random_index + 1) % len(polygon_verteces)]

    new_vertex_x = (vertex_before[0] + vertex_after[0]) / 2
    new_vertex_y = (vertex_before[1] + vertex_after[1]) / 2

    polygon_verteces.insert(random_index + 1, (new_vertex_x, new_vertex_y))

def interpolate_polygon(polygon_start, polygon_end, t):
    interpolated_polygon = []

    for p_s, p_e in zip(polygon_start, polygon_end):
        interpolated_x = p_s[0] + (p_e[0] - p_s[0]) * t
        interpolated_y = p_s[1] + (p_e[1] - p_s[1]) * t
        interpolated_polygon.append((interpolated_x, interpolated_y))
    return interpolated_polygon

def morph_polygon(polygon_start, polygon_end, steps):

    while len(polygon_start) < len(polygon_end):
        add_vertex(polygon_start)

    while len(polygon_start) > len(polygon_end):
        remove_vertex(polygon_start)

    colors = cm.viridis([i / steps for i in range(steps + 1)])
    
    for step in range(steps + 1):
        t = step / steps
        interpolated_polygon = interpolate_polygon(polygon_start, polygon_end, t)

        x_vals, y_vals = zip(*interpolated_polygon)  
    
        # Plot the points and add the first point again at the end to close the polygon
        plt.plot(x_vals + (x_vals[0],), y_vals + (y_vals[0],), label=f'Step {step}', marker='o', color=colors[step])

        plt.pause(1)  

    plt.title("Morphing Steps")
    plt.legend()
    plt.tight_layout()
    plt.show()


def main():
    polygon_start = generate_polygon_vertices(polygon_start_verteces)
    polygon_end = generate_polygon_vertices(polygon_end_verteces)

    morph_polygon(polygon_start, polygon_end, steps=interpolation_steps)

if __name__ == "__main__":
    main()
