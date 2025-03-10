# Sorts list of tuples
def bubble_sort_polygon(polygon):
    vertices_count = len(polygon)

    for i in range(vertices_count):
        swapped = False 

        for j in range(vertices_count - i - 1):
            if polygon[j][1] > polygon[j + 1][1]:
                polygon[j], polygon[j + 1] = polygon[j + 1], polygon[j]
                swapped = True
        
        if not swapped:
            break

    return polygon

def get_polygon_y_values(polygon):
    y_values = []

    for vertex in polygon:
        y_values.append(vertex[1])
    
    return y_values

def main():
    triangle = [
    (1, 1),  
    (3, 5),  
    (5, 1)   
]
    quadrilateral = [
    (1.5, 2.0),  
    (4.0, 3.5),  
    (3.0, 1.0),  
    (2.0, 1.0)  
]
    sorted_polygon = bubble_sort_polygon(triangle)

    y_min = sorted_polygon[0][1]
    y_max = sorted_polygon[-1][1]

    y_values = get_polygon_y_values(sorted_polygon)




if __name__ == "__main__":
    main()


