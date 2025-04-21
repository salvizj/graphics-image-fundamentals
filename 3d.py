from PIL import Image
from typing import List, Tuple

IMAGE_WIDTH = 400
IMAGE_HEIGHT = 400
BACKGROUND_COLOR = (255, 255, 255)
PIXEL_COLOR = (0, 0, 0)
IMAGE_NAME = "polygon_fill.png"

PENTAGON: List[Tuple[int, int]] = [
    (30, 60),
    (100, 30),
    (180, 50),
    (150, 150),
    (60, 120)
]

TRIANGLE: List[Tuple[int, int]] = [
    (50, 100),  
    (150, 50),  
    (100, 200), 
]

NONAGON: List[Tuple[int, int]] = [
    (250, 100),
    (230, 160),
    (170, 200),
    (100, 190),
    (60, 130),
    (60, 70),
    (100, 10),
    (170, 0),
    (230, 40),
]

def edges_from_polygon(polygon: List[Tuple[int, int]]) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
    edges = []
    vertice_count = len(polygon)
    for i in range(vertice_count):
        start = polygon[i]
        end = polygon[(i + 1) % vertice_count]
        edges.append((start, end))
    return edges

def bubble_sort_polygon_edges(polygon_edges: List[Tuple[Tuple[int, int], Tuple[int, int]]], sort_by: str = 'y') -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
    edge_count = len(polygon_edges)

    for i in range(edge_count):
        swapped = False

        for j in range(edge_count - i - 1):
            current_edge = polygon_edges[j]
            next_edge = polygon_edges[j + 1]

            if sort_by == 'x':
                current_key = min(current_edge[0][0], current_edge[1][0])
                next_key = min(next_edge[0][0], next_edge[1][0])
            elif sort_by == 'y':
                current_key = min(current_edge[0][1], current_edge[1][1])
                next_key = min(next_edge[0][1], next_edge[1][1])
            else:
                raise ValueError("sort_by must be 'x' or 'y'")

            if current_key > next_key:
                polygon_edges[j], polygon_edges[j + 1] = polygon_edges[j + 1], polygon_edges[j]
                swapped = True

        if not swapped:
            break

    return polygon_edges

def line_intersect(edge: Tuple[Tuple[int, int], Tuple[int, int]], y: int) -> float:
    (x0, y0), (x1, y1) = edge

    if y0 == y1:
        return None
    
    t = (y - y0) / (y1 - y0)
    x_intersect = x0 + t * (x1 - x0)
    return x_intersect

def fill_polygon(polygon: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    filled_pixels = []
    
    polygon_edges = edges_from_polygon(polygon)
    polygon_edges = bubble_sort_polygon_edges(polygon_edges, sort_by='y')
    
    y_min = int(min(y for (_, y) in polygon))
    y_max = int(max(y for (_, y) in polygon))
    
    active_edges = []

    for y_level in range(y_min, y_max + 1):

        for edge in polygon_edges:
            (_, y0), (_, y1) = edge

            edge_y_min = min(y0,y1)

            if y_level == edge_y_min:
                active_edges.append(edge)

        active_edges = [edge for edge in active_edges if max(edge[0][1], edge[1][1]) > y_level]

        intersections = []
        for edge in active_edges:
            (x0, y0), (x1, y1) = edge

            if y0 == y1: 
                x_left = min(x0, x1)
                x_right = max(x0, x1)
                for x in range(int(round(x_left)), int(round(x_right)) + 1):
                    filled_pixels.append((x, y_level))
            else: 
                x_intersection = line_intersect(edge, y_level)
                if x_intersection is not None:
                    intersections.append((x_intersection, y_level))

        intersections.sort(key=lambda point: point[0])

        while len(intersections) > 1:
            x_left, _ = intersections.pop(0)  
            x_right, _ = intersections.pop(0)  
        
            for x in range(int(round(x_left)), int(round(x_right)) + 1):
                filled_pixels.append((x, y_level))

    return filled_pixels

def show_polygon_fill(filled_pixels: List[Tuple[int, int]]) -> None:
    image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), BACKGROUND_COLOR)

    pixels = image.load()

    for x, y in filled_pixels:
        if 0 <= x < IMAGE_WIDTH and 0 <= y < IMAGE_HEIGHT:
            pixels[x, y] = PIXEL_COLOR
    image.save(IMAGE_NAME)
    image.show()

def main() -> None:
    polygon = TRIANGLE

    filled_pixels = fill_polygon(polygon)
    show_polygon_fill(filled_pixels)

if __name__ == "__main__":
    main()
