from typing import List
from PIL import Image
import matplotlib.pyplot as plt

IMAGE_PATH = './img.png'

def read_grayscale_image(image_path: str) -> List[List[int]]:
    img = Image.open(image_path).convert('L') 
    width, height = img.size
    pixels = list(img.getdata())

    grayscale_img = [pixels[i * width:(i + 1) * width] for i in range(height)]
    return grayscale_img

def calculate_histogram(grayscale_image: List[List[int]]) -> List[int]:
    histogram = [0] * 256
    for row in grayscale_image:
        for pixel in row:
            histogram[pixel] += 1
    return histogram

def histogram_equalization(image: List[List[int]]) -> List[List[int]]:
    height = len(image)
    width = len(image[0]) if height > 0 else 0
    total_pixels = height * width

    histogram = calculate_histogram(image)

    cdf = [0 for _ in range(256)]
    cumulative = 0
    for i, count in enumerate(histogram):
        cumulative += count
        cdf[i] = cumulative

    cdf_min = next(value for value in cdf if value > 0)

    transform_map = [0 for _ in range(256)]
    transform_map = [0] * 256
    for i in range(256):
        if cdf[i] == 0:
            transform_map[i] = 0
        else:
            val = round((cdf[i] - cdf_min) / (total_pixels - cdf_min) * 255)
            val = max(0, min(255, val)) 
            transform_map[i] = val

    equalized_image = []

    for row in image:
        new_row = [transform_map[pixel] for pixel in row]
        equalized_image.append(new_row)

    return equalized_image


def save_image_comparison(original: List[List[int]], equalized: List[List[int]]):
    _, axes = plt.subplots(1, 2, figsize=(12, 6))
    axes[0].imshow(original, cmap='gray', vmin=0, vmax=255)
    axes[0].set_title('Oriģinālais attēls')
    axes[0].axis('off')

    axes[1].imshow(equalized, cmap='gray', vmin=0, vmax=255)
    axes[1].set_title('Vienmērīgots attēls')
    axes[1].axis('off')

    filename = 'histogram_equalization_result.png'
    plt.savefig(filename)
    print(f"Attēls saglabāts failā '{filename}'")

    plt.close()

    img = Image.open(filename)
    img.show()

def main():
    grayscale_image = read_grayscale_image(IMAGE_PATH)
    equalized_image = histogram_equalization(grayscale_image)
    save_image_comparison(grayscale_image, equalized_image)

if __name__ == "__main__":
    main()