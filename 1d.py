import math
import random
from matplotlib import cm
import matplotlib.pyplot as plt
from typing import List, Tuple

# constants (min polygon vertices: 3 and min step: 1)
# polygon end and start vertice difference can`t be bigger than step count
POLYGON_START_VERTICES = 4
POLYGON_END_VERTICES = 11
PARAMETRIC_INTERPOLATION_STEPS = 7

# generates a regular polygon with `n` vertices evenly spaced around a circle of radius `r`.
# returns a list of (x, y) coordinate tuples for each vertex.
def generate_polygon_vertices(n: int) -> List[Tuple[float, float]]:
    if n < 3:
        raise ValueError("A polygon must have at least 3 vertices.")
    r = 4
    polygon_vertices = []
    angle_deg = 360 / n
    
    for i in range(n):
        angle = math.radians(angle_deg * i)  
        x = r * round(math.cos(angle), 4)
        y = r * round(math.sin(angle), 4)
        polygon_vertices.append((x, y))  
    
    return polygon_vertices

def remove_vertex(polygon_vertices: List[Tuple[float, float]]) -> None:
    if len(polygon_vertices) == 0:
        return
    
    random_index = random.randint(0, len(polygon_vertices) - 1)
    polygon_vertices.pop(random_index)

def add_vertex(polygon_vertices: List[Tuple[float, float]]) -> None:
    if len(polygon_vertices) == 0:
        return
    
    random_index = random.randint(0, len(polygon_vertices) - 1)

    vertex_before = polygon_vertices[random_index]
    # takes first vertex if out bounds
    vertex_after = polygon_vertices[(random_index + 1) % len(polygon_vertices)]

    new_vertex_x = (vertex_before[0] + vertex_after[0]) / 2
    new_vertex_y = (vertex_before[1] + vertex_after[1]) / 2

    polygon_vertices.insert(random_index + 1, (new_vertex_x, new_vertex_y))

def parametric_interpolate_polygon(polygon_start, polygon_end, t):
    interpolated_polygon = []

    # interpolate the overlapping vertices
    for i in range(min(len(polygon_start), len(polygon_end))):
        p_s = polygon_start[i]
        p_e = polygon_end[i]

        interpolated_x = p_s[0] + (p_e[0] - p_s[0]) * t
        interpolated_y = p_s[1] + (p_e[1] - p_s[1]) * t
        interpolated_polygon.append((interpolated_x, interpolated_y))

    # add remaining vertices from polygon_start
    if len(polygon_start) > len(polygon_end):
        for j in range(len(polygon_end), len(polygon_start)):
            interpolated_polygon.append(polygon_start[j])

    return interpolated_polygon

def morph_polygon(polygon_start, polygon_end, steps):
    _, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 6))

    ax1.set_title("Generated end polygon")
    ax1.set_xlabel("X-axis")
    ax1.set_ylabel("Y-axis")
    x_vals, y_vals = zip(*polygon_end)
    ax1.plot(x_vals + (x_vals[0],), y_vals + (y_vals[0],), label=f'Final Polygon {len(polygon_end)}', marker='o')
    ax1.legend()

    ax2.set_title("Morphing from start to end polygon")
    ax2.set_xlabel("X-axis")
    ax2.set_ylabel("Y-axis")

    colors = cm.viridis([i / steps for i in range(steps + 1)])
    
    for step in range(steps + 1):
        t = step / steps

        interpolated_polygon = parametric_interpolate_polygon(polygon_start, polygon_end, t)

        if len(polygon_start) > len(polygon_end):
            remove_vertex(polygon_start)
        elif len(polygon_start) < len(polygon_end):
            add_vertex(polygon_start)

        x_vals, y_vals = zip(*interpolated_polygon)  
    
        ax2.plot(x_vals + (x_vals[0],), y_vals + (y_vals[0],), label=f'Step {step}', marker='o', color=colors[step])

        plt.pause(1)  

    plt.legend()
    plt.tight_layout()
    plt.show()

def main():
    min_polygon = min(POLYGON_START_VERTICES, POLYGON_END_VERTICES)
    max_polygon = max(POLYGON_START_VERTICES, POLYGON_END_VERTICES)

    if (max_polygon - min_polygon) > PARAMETRIC_INTERPOLATION_STEPS:
        raise ValueError("POLYGON_START_VERTICES and POLYGON_END_VERTICES difference can`t be bigger than PARAMETRIC_INTERPOLATION_STEP count")

    polygon_start = generate_polygon_vertices(POLYGON_START_VERTICES)
    polygon_end = generate_polygon_vertices(POLYGON_END_VERTICES)

    morph_polygon(polygon_start, polygon_end, PARAMETRIC_INTERPOLATION_STEPS)

if __name__ == "__main__":
    main()
