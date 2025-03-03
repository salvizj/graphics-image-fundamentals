import math
import random
from matplotlib import cm
import matplotlib.pyplot as plt


# Generate equilateral polygons by giving vertex count. Func returns list with tuplets of vertices
def generate_polygon_vertices(n):
    if n < 3:
        raise ValueError("A polygon must have at least 3 vertices.")
    r = 4 
    polygon_vertices = []
    angle_deg = 360 / n
    
    for i in range(n):
        angle = math.radians(angle_deg * i)  
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

def parametric_interpolate_polygon(polygon_start, polygon_end, t):
    polygon = []

    for p_s, p_e in zip(polygon_start, polygon_end):
        interpolated_x = p_s[0] + (p_e[0] - p_s[0]) * t
        interpolated_y = p_s[1] + (p_e[1] - p_s[1]) * t
        polygon.append((interpolated_x, interpolated_y))
    return polygon

# Adjust the start polygon's vertex count to match the generated end polygon's vertex count
def adjust_polygon(polygon_start, polygon_end, ax1):

    ax1.set_title("Adding/Removing vertices from generated starting polygon")
    ax1.set_xlabel("X-axis")
    ax1.set_ylabel("Y-axis")

    x_vals, y_vals = zip(*polygon_start)
    ax1.plot(x_vals + (x_vals[0],), y_vals + (y_vals[0],), label=f'Before adding or removing vertices {len(polygon_start)}', marker='o')

    while len(polygon_start) < len(polygon_end):
        add_vertex(polygon_start)
    while len(polygon_start) > len(polygon_end):
        remove_vertex(polygon_start)

    x_vals, y_vals = zip(*polygon_start)
    ax1.plot(x_vals + (x_vals[0],), y_vals + (y_vals[0],), label=f'After removing or adding vertices {len(polygon_start)}', marker='o')

    ax1.legend()

def morph_polygon(polygon_start, polygon_end, steps):
    _, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))

    adjust_polygon(polygon_start, polygon_end, ax1)

    ax2.set_title("Generated end polygon")
    ax2.set_xlabel("X-axis")
    ax2.set_ylabel("Y-axis")
    x_vals, y_vals = zip(*polygon_end)
    ax2.plot(x_vals + (x_vals[0],), y_vals + (y_vals[0],), label=f'Final Polygon {len(polygon_end)}', marker='o')
    ax2.legend()

    ax3.set_title("Morphing from start to end polygon")
    ax3.set_xlabel("X-axis")
    ax3.set_ylabel("Y-axis")

    colors = cm.viridis([i / steps for i in range(steps + 1)])
    
    for step in range(steps + 1):
        t = step / steps
        interpolated_polygon = parametric_interpolate_polygon(polygon_start, polygon_end, t)

        x_vals, y_vals = zip(*interpolated_polygon)  
    
        ax3.plot(x_vals + (x_vals[0],), y_vals + (y_vals[0],), label=f'Step {step}', marker='o', color=colors[step])

        plt.pause(1)  

    plt.legend()
    plt.tight_layout()
    plt.show()

def main():
    # Variables to change (min polygon vertices: 3 and min step: 1)
    polygon_start_verteces = 10
    polygon_end_verteces = 3
    parametric_interpolation_steps = 3

    polygon_start = generate_polygon_vertices(polygon_start_verteces)
    polygon_end = generate_polygon_vertices(polygon_end_verteces)

    morph_polygon(polygon_start, polygon_end, parametric_interpolation_steps)

if __name__ == "__main__":
    main()
