import matplotlib.pyplot as plt

def plot_polygon(polygon_dict, key):
    if key in polygon_dict:
        coordinates = polygon_dict[key]
        x, y = zip(*coordinates)  # Unzip coordinates into x and y lists
        x += (x[0],)  # Close the polygon by adding the first point again
        y += (y[0],)  # Close the polygon by adding the first point again

        plt.plot(x, y, marker='o')
        plt.fill(x, y, alpha=0)  
        plt.title(f"{key.capitalize()} Polygon")
        plt.show()
    else:
        print(f"Key '{key}' not found in the dictionary.")

def main():
    polygon_dict = {
        "triangle": [(0, 0), (2, 0), (1, 1)],  
        "quadrilateral": [(0, 0), (2, 0), (2, 2), (0, 2)],
        "pentagon": [(0, 0), (1, 0), (1.5, 1), (0.5, 2), (-0.5, 1)],
        "hexagon": [(0, 0), (1, 0), (1.5, 1), (1,2), (0, 2),(-0.5, 1)],
        "heptagon": [(0, 0), (1, 0), (1.5, 1), (1,2.5), (0.5, 3),(0, 2.5),(-0.5, 1)],
        "octagon": [(0, 0), (1, 0), (1.5, 0.5), (1.5, 1.5), (1, 2), (0, 2), (-0.5, 1.5), (-0.5, 0.5)],
        "nonagon": [(0, 0), (1, 0), (1.5, 0.5), (1.5, 1.5), (1, 2), (0, 2), (-0.5, 1.5), (-0.5, 0.5), (-1, 0)]
    }
    plot_polygon(polygon_dict=polygon_dict, key="heptagon")

if __name__ == "__main__":
    main()
