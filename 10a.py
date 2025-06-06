#10.a) Izstrādāt datorprogrammu, kas realizē izpludināšanas un asināšanas filtrus pie dažādu izmēru konvolūcijas maskām.
from typing import List, Sequence, Union
from PIL import Image
import matplotlib.pyplot as plt

IMAGE_PATH = './img.png'


BLUR_MASK_3x3:  Sequence[Sequence[float]] = [
    [1/9, 1/9, 1/9],
    [1/9, 1/9, 1/9],
    [1/9, 1/9, 1/9]
]
BLUR_MASK_5x5: Sequence[Sequence[float]] = [
    [1/25, 1/25, 1/25, 1/25, 1/25],
    [1/25, 1/25, 1/25, 1/25, 1/25],
    [1/25, 1/25, 1/25, 1/25, 1/25],
    [1/25, 1/25, 1/25, 1/25, 1/25],
    [1/25, 1/25, 1/25, 1/25, 1/25]
]
SHARPEN_MASK_3x3:  Sequence[Sequence[int]] = [
    [ 0, -1,  0],
    [-1,  5, -1],
    [ 0, -1,  0]
]
SHARPEN_MASK_5x5: Sequence[Sequence[int]] = [
    [ 0,  0, -1,  0,  0],
    [ 0,  0, -1,  0,  0],
    [-1, -1,  9, -1, -1],
    [ 0,  0, -1,  0,  0],
    [ 0,  0, -1,  0,  0]
]


def read_grayscale_image(image_path: str) -> List[List[int]]:
    img = Image.open(image_path).convert('L') 
    width, height = img.size
    pixels = list(img.getdata())

    grayscale_img = [pixels[i * width:(i + 1) * width] for i in range(height)]
    return grayscale_img

def get_pixel(image: List[List[int]], x: int, y: int) -> int:
    height = len(image)
    width = len(image[0])
    if 0 <= y < height and 0 <= x < width:
        return image[y][x]
    else:
        return 0  

def calculate_mask_sum_for_pixel(
    mask: Sequence[Sequence[float | int]],
    image: List[List[int]],
    center_x: int,
    center_y: int
) -> int:
    mask_size = len(mask)
    offset = mask_size // 2
    pixel_sum = 0.0
    for i in range(mask_size):
        for j in range(mask_size):
            x = center_x + j - offset
            y = center_y + i - offset
            pixel = get_pixel(image, x, y)
            weight = mask[i][j]
            pixel_sum += pixel * weight
    return int(round(pixel_sum))


def apply_mask_to_image(mask: Sequence[Sequence[float | int]], image: Sequence[Sequence[int]]) -> List[List[int]]:
    height = len(image)          
    width = len(image[0]) if height > 0 else 0 
    new_image = [[0 for _ in range(width)] for _ in range(height)]

    for y in range(height):
        for x in range(width):
            new_image[y][x] = calculate_mask_sum_for_pixel(mask, image, x, y) # type: ignore
    return new_image

def save_image_comparison(original: List[List[int]], shrapened_image_3x3: List[List[int]], blurred_image_3x3: List[List[int]], sharpened_image_5x5: List[List[int]], blurred_image_5x5: List[List[int]]):
    _, axes = plt.subplots(1, 5, figsize=(18, 6))

    axes[0].imshow(original, cmap='gray', vmin=0, vmax=255)
    axes[0].set_title('Oriģinālais attēls')
    axes[0].axis('off')

    axes[1].imshow(shrapened_image_3x3, cmap='gray', vmin=0, vmax=255)
    axes[1].set_title('Attēls ar asināšanas\nfiltru 3x3 masku')
    axes[1].axis('off')

    axes[2].imshow(blurred_image_3x3, cmap='gray', vmin=0, vmax=255)
    axes[2].set_title('Attēls ar izpludināšanas\nfiltru 3x3 masku')
    axes[2].axis('off')

    axes[3].imshow(sharpened_image_5x5, cmap='gray', vmin=0, vmax=255)
    axes[3].set_title('Attēls ar asināšanas\nfiltru 5x5 masku')
    axes[3].axis('off')

    axes[4].imshow(blurred_image_5x5, cmap='gray', vmin=0, vmax=255)
    axes[4].set_title('Attēls ar izpludināšanas\nfiltru 5x5 masku')
    axes[4].axis('off')

    filename = 'blurred_sharpened_masked_images.png'
    plt.savefig(filename)
    print(f"Attēls saglabāts failā '{filename}'")

    plt.close()

    img = Image.open(filename)
    img.show()


def main():
    grayscale_image = read_grayscale_image(IMAGE_PATH)
    sharpened_image_3x3 = apply_mask_to_image(SHARPEN_MASK_3x3, grayscale_image)
    blurred_image_3x3 = apply_mask_to_image(BLUR_MASK_3x3, grayscale_image)
    sharpened_image_5x5 = apply_mask_to_image(SHARPEN_MASK_5x5, grayscale_image)
    blurred_image_5x5 = apply_mask_to_image(BLUR_MASK_5x5, grayscale_image)

    save_image_comparison(grayscale_image, sharpened_image_3x3, blurred_image_3x3, sharpened_image_5x5, blurred_image_5x5)

if __name__ == "__main__":
    main()

