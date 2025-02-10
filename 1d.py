import matplotlib.pyplot as plt
import numpy as np

# Generate polygons by giving n which is a number and func return list with tuplets
def generate_polygon(n):
    r = 4
    polygon_points = []
    angle_deg = 360 / n
    for i in range (n):
        angle = ( angle_deg / n ) * i

    return polygon_points


def main():
    polygon_points = generate_polygon(2)

if __name__ == "__main__":
    main()
