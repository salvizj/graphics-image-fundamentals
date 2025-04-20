import math
from typing import Callable, List, Tuple
from matplotlib import pyplot as plt
import colour

WAVELENGTH_MIN = 380 
WAVELENGTH_MAX = 700   
WAVELENGTH_STEP = 1 
T_STEPS = 5

# user defined spectral sensitivity functions
def S(wavelength: float) -> float:
    return math.exp(-((wavelength - 420) / 40) ** 2)

def M(wavelength: float) -> float:
    return math.exp(-((wavelength - 534) / 50) ** 2)

def L(wavelength: float) -> float:
    return math.exp(-((wavelength - 564) / 60) ** 2)

def wavelength_to_rgb_colour(wavelength: float) -> Tuple[float, float, float]:
    xyz = colour.wavelength_to_XYZ(wavelength)
    rgb = colour.XYZ_to_sRGB(xyz)
    return tuple(max(0.0, min(1.0, c)) for c in rgb)

def get_color_coordinates(S: Callable[[float], float], M: Callable[[float], float], L: Callable[[float], float], wavelength: float) -> Tuple[float, float, float]:
    s = S(wavelength)
    m = M(wavelength)
    l = L(wavelength)
    return (s, m, l)

def scale_color_coordinates(color_coordinate: Tuple[float, float, float], t: float) -> Tuple[float, float, float]:
    s, m, l = color_coordinate
    return (s * t, m * t, l * t)

def plot_colors(S_vals: List[float], M_vals: List[float], L_vals: List[float], colors: List[Tuple[float, float, float]], S_base: List[float], M_base: List[float], L_base: List[float]) -> None:
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(S_vals, M_vals, L_vals, c=colors, s=4, alpha=0.7)
    ax.plot(S_base, M_base, L_base, color='black', linewidth=4)
    ax.set_zlabel('S (short)')
    ax.set_ylabel('M (medium)')
    ax.set_xlabel('L (long)')
    ax.set_title('The surface of pure spectral colors in LMS space')
    ax.text2D(0.05, 0.95, f"Wavelength range: {WAVELENGTH_MIN}-{WAVELENGTH_MAX}nm", transform=ax.transAxes)
    plt.tight_layout()
    plt.show()

def main():
    S_vals, M_vals, L_vals = [], [], []
    S_base, M_base, L_base = [], [], []
    colors = []
    wavelengths = []

    for wavelength in range(WAVELENGTH_MIN, WAVELENGTH_MAX, WAVELENGTH_STEP):
        s_base, m_base, l_base = get_color_coordinates(S, M, L, wavelength)
        S_base.append(s_base)
        M_base.append(m_base)
        L_base.append(l_base)

    for wavelength in range(WAVELENGTH_MIN, WAVELENGTH_MAX, WAVELENGTH_STEP):
        base = get_color_coordinates(S, M, L, wavelength)
        rgb = wavelength_to_rgb_colour(wavelength)
        wavelengths.append(wavelength)

        for t in  range(0, 101, T_STEPS): 
            t = t/100.0  # 0.0, 0.05 .. 1.00
            s, m, l = scale_color_coordinates(base, t)
            S_vals.append(s)
            M_vals.append(m)
            L_vals.append(l)
            colors.append(rgb)
                
    plot_colors(S_vals, M_vals, L_vals, colors, s_base, m_base, l_base)

if __name__ == "__main__":
    main()