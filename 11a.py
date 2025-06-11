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

def save_image_comparison(
    original_image: List[List[int]], 
    new_binary_image: List[List[int]], 
):
    _, axes = plt.subplots(1, 2, figsize=(18, 6))

    axes[0].imshow(original_image, cmap='gray', vmin=0, vmax=255)
    axes[0].set_title('Original Image')
    axes[0].axis('off')

    axes[1].imshow(new_binary_image, cmap='gray', vmin=0, vmax=255)
    axes[1].set_title('Binary image')
    axes[1].axis('off')

    filename = 'segmated_image_with_otsu_threshold.png'
    plt.savefig(filename)
    print(f"Image saved to file '{filename}'")

    plt.close()

    img = Image.open(filename)
    img.show()

# Otsu's method https://en.wikipedia.org/wiki/Otsu%27s_method
def calculate_threshold(histogram: List[int]) -> int:
    total_pixel_count = sum(histogram)
    weighted_total_intensity = sum(i * histogram[i] for i in range(len(histogram)))

    background_weight = 0
    background_total_sum = 0 
    highest_variance_between_classes = 0
    optimal_threshold = 0

    for t in range(len(histogram)):
        background_weight += histogram[t]
        if background_weight == 0:
            continue
        foreground_weight = total_pixel_count - background_weight
        if foreground_weight == 0:
            break

        background_total_sum += t* histogram[t]
        background_mean = background_total_sum / background_weight
        foreground_mean = (weighted_total_intensity - background_total_sum) / foreground_weight

        between_class_variance = background_weight * foreground_weight * (background_mean - foreground_mean) ** 2

        if between_class_variance > highest_variance_between_classes:
            highest_variance_between_classes = between_class_variance
            optimal_threshold = t
    
    return optimal_threshold

def apply_threshhold_to_image(image: List[List[int]], threshhold: int):
    new_image = []
    for row in image:
        new_row = []
        for p in row:
            if p > threshhold:
                new_row.append(255)
            else:
                new_row.append(0)
        new_image.append(new_row)
    return new_image

def main():
    grayscale_image = read_grayscale_image(IMAGE_PATH)
    histogram = calculate_histogram(grayscale_image)
    threshold = calculate_threshold(histogram)
    new_image = apply_threshhold_to_image(grayscale_image, threshold)
    save_image_comparison(grayscale_image, new_image)

if __name__ == "__main__":
    main()

