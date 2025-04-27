#9.b) Izstrādāt datorprogrammu, kas realizē histogrammas vienmērīgošanu.
from typing import List
from PIL import Image
IMAGE_PATH = './img.png'

def read_grayscale_image(IMAGE_PATH: str) -> List[int]:
    try:
        img = Image.open(IMAGE_PATH)
        grayscale_img = img.convert('L') 
        return list(grayscale_img.getdata())  
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: Unable to load image at '{IMAGE_PATH}'")

def calculate_histogram(grayscale_image):
    histogram = [0 for _ in range(256)]

    for pixel in grayscale_image:
        histogram[pixel] += 1
        
def histogram_equalization():

def main():
    calculate_histogram()
    ()

if __name__ == "__main__":
    main()