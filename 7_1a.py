import math
from typing import Callable, List, Tuple
from matplotlib import pyplot as plt
import colour

WAVELENGTH_MIN = 380 
WAVELENGTH_MAX = 700   
WAVELENGHT_STEP = 1 

# user defined spectral sensitivity functions
def S(wavelength: float) -> float:
    return math.exp(-((wavelength - 440) / 20) ** 2)

def M(wavelength: float) -> float:
    return math.exp(-((wavelength - 540) / 25) ** 2)

def L(wavelength: float) -> float:
    return math.exp(-((wavelength - 580) / 30) ** 2)
 
def wavelength_to_rgb_colour(wavelength: float) -> Tuple[float, float, float]:
    xyz = colour.wavelength_to_XYZ(wavelength)
    rgb = colour.XYZ_to_sRGB(xyz)
    return tuple(max(0.0, min(1.0, c)) for c in rgb)

def get_color_coordinates(S: Callable[[float], float], M: Callable[[float], float], L: Callable[[float], float], wavelength: float) -> Tuple[float, float, float]:
    s = S(wavelength)
    m = M(wavelength)
    l = L(wavelength)
    return (l, m, s)

def scale_color_coordinates(color_coordinate: Tuple[float, float, float], t: float) -> Tuple[float, float, float]:
    return tuple(component * t for component in color_coordinate)

def plot_colors(L_vals: List[float], M_vals: List[float], S_vals: List[float], colors: List[Tuple[float, float, float]]) -> None:
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(L_vals, M_vals, S_vals, c=colors, s=8)
    ax.set_xlabel('L (long)')
    ax.set_ylabel('M (medium)')
    ax.set_zlabel('S (short)')
    ax.set_title('The surface of pure spectral colors in LMS space')
    plt.tight_layout()
    plt.show()

def main():
    L_vals, M_vals, S_vals = [], [], []
    colors = []
    wavelengths = []

    for wavelength in range(WAVELENGTH_MIN, WAVELENGTH_MAX, WAVELENGHT_STEP):
        base = get_color_coordinates(S, M, L, wavelength)
        rgb = wavelength_to_rgb_colour(wavelength)
        wavelengths.append(wavelength)

        for t in  range(0, 101, 5): 
            t = t/100.0  # 0.0, 0.05 .. 1.00
            l, m, s = scale_color_coordinates(base, t)
            L_vals.append(l)
            M_vals.append(m)
            S_vals.append(s)
            colors.append(rgb)

    plot_colors(L_vals, M_vals, S_vals, colors)

if __name__ == "__main__":
    main()