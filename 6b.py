from matplotlib import pyplot as plt
import math
from typing import List, Tuple

# projection value
D = 5.0  

# u and v value generation
VAL_COUNT = 10
START_VAL = 0
END_VAL = 2 * math.pi
STEP = (END_VAL - START_VAL) / (VAL_COUNT - 1)
U_VALS = [START_VAL + i * STEP for i in range(VAL_COUNT)]
V_VALS = [START_VAL + i * STEP for i in range(VAL_COUNT)]

def flat_plane(u: float, v: float):
    x = u
    y = v
    z = 0.0  # all z-values are zero for a flat plane
    return x, y, z

def sphere(u: float, v: float):
    x = math.sin(u) * math.cos(v)
    y = math.sin(u) * math.sin(v)
    z = math.cos(u)
    return x, y, z

def torus(u: float, v: float):
    R = 1.0
    r = 0.3
    x = (R + r * math.cos(v)) * math.cos(u)
    y = (R + r * math.cos(v)) * math.sin(u)
    z = r * math.sin(v)
    return x, y, z

def generate_surface_grid(
    surface_def, u_vals: List[float], v_vals: List[float]
) -> List[List[Tuple[float, float, float]]]:
    grid = []
    for u in u_vals:
        row = []
        for v in v_vals:
            row.append(surface_def(u, v))
        grid.append(row)
    return grid

def project_3d_point_to_2d(x: float, y: float, z: float, D: float) -> Tuple[float, float]:
    depth = z + D
    if depth == 0:
        depth = 1e-5  # using 0.00001 to avoid zero dvisionm
    x_proj = x / depth
    y_proj = y / depth

    return x_proj, y_proj

def project_surface_to_2d(grid: List[List[Tuple[float, float, float]]], D: float) -> List[List[Tuple[float, float, float]]]:
    rows = len(grid)
    cols = len(grid[0])

    projection_grid = []

    for i in range(rows):
        row = []
        for j in range(cols):
            x, y, z = grid[i][j]
            x_proj, y_proj = project_3d_point_to_2d(x, y, z, D) 
            row.append((x_proj, y_proj, z)) 
        projection_grid.append(row)

    return projection_grid

def create_triangle_mesh_from_projection_grid(
    projection_grid: List[List[Tuple[float, float, float]]]
) -> List[List[Tuple[float, float, float]]]:
    rows = len(projection_grid)
    cols = len(projection_grid[0])

    triangles = []

    for i in range(rows - 1):
        for j in range(cols - 1):
            p1 = projection_grid[i][j]
            p2 = projection_grid[i + 1][j]
            p3 = projection_grid[i][j + 1]
            p4 = projection_grid[i + 1][j + 1]

            triangles.append([p1, p2, p3])
            triangles.append([p2, p4, p3])

    return triangles

def plot_triangles_3d(triangles: List[Tuple[float, float, float]]) -> None:
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection="3d")

    for triangle in triangles:
        x = [p[0] for p in triangle] + [triangle[0][0]] # to connect last side to first
        y = [p[1] for p in triangle] + [triangle[0][1]]
        z = [p[2] for p in triangle] + [triangle[0][2]]
        ax.plot(x, y, z, color="black", linewidth=1)

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("3D Triangular Mesh (Wireframe)")
    plt.show()

def main():
    surfaces = [flat_plane, sphere, torus]

    for surface_def in surfaces:
        grid = generate_surface_grid(surface_def, U_VALS, V_VALS) 
        projection_grid = project_surface_to_2d(grid, D) 
        triangles = create_triangle_mesh_from_projection_grid(projection_grid)  
        plot_triangles_3d(triangles)  

if __name__ == "__main__":
    main()
