from PIL import Image

IMAGE_WIDTH = 500
IMAGE_HEIGHT = 500
BACKGROUND_COLOR = (255, 255, 255)
PIXEL_COLOR = (255, 0, 0)

TRIANGLE = [
    (50.0, 50.0),
    (150.0, 200.0),
    (250.0, 50.0)
]

QUADRILATERAL = [
    (60.0, 60.0),
    (240.0, 80.0),
    (220.0, 220.0),
    (80.0, 200.0)
]

def edges_from_polygon(polygon):
    edges = []
    vertice_count = len(polygon)
    for i in range(vertice_count):
        start = polygon[i]
        end = polygon[(i + 1) % vertice_count]
        edges.append((start, end))
    return edges

def bubble_sort_polygon_edges(polygon_edges, sort_by='y'):
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

def line_intersect(edge, y):
    (x0, y0), (x1, y1) = edge

    if y1 == y0:
        return None

    t = (y - y0) / (y1 - y0)
    x_intersect = x0 + t * (x1 - x0)
    return x_intersect

def fill_polygon(polygon):
    filled_pixels = []
    
    polygon_edges = edges_from_polygon(polygon)
    polygon_edges = bubble_sort_polygon_edges(polygon_edges, sort_by='y')
    
    y_min = int(min(y for (_, y) in polygon))
    y_max = int(max(y for (_, y) in polygon))
    
    active_edges = []

    for y_level in range(y_min, y_max + 1):
        for edge in polygon_edges:
            (_, y0), (_, y1) = edge

            if y0 < y1:
                edge_y_min = y0
            else:
                edge_y_min = y1

            if y_level == edge_y_min:
                active_edges.append(edge)

        intersections = []
        for edge in active_edges:
            (_, y0), (_, y1) = edge
            x_intersection = line_intersect(edge, y_level)
            if x_intersection is not None:
                intersections.append((x_intersection, y_level))

        active_edges = [edge for edge in active_edges if max(edge[0][1], edge[1][1]) > y_level]

        intersections.sort(key=lambda point: point[0])

        while len(intersections) > 1:
            x_left, _ = intersections.pop(0)  
            x_right, _ = intersections.pop(0)  
        
            for x in range(int(round(x_left)), int(round(x_right)) + 1):
                filled_pixels.append((x, y_level))

    return filled_pixels

def show_polygon_fill(filled_pixels, background_color, pixel_color, image_size=(300, 300)):
    image = Image.new("RGB", image_size, background_color)

    pixels = image.load()

    for x, y in filled_pixels:
        if 0 <= x < image_size[0] and 0 <= y < image_size[1]:
            pixels[x, y] = pixel_color
    image.save("polygon_fill.png")
    image.show()

def main():
    polygon = QUADRILATERAL       

    filled_pixels = fill_polygon(polygon)
    show_polygon_fill(filled_pixels, BACKGROUND_COLOR, PIXEL_COLOR, image_size=(IMAGE_WIDTH, IMAGE_HEIGHT))

if __name__ == "__main__":
    main()
