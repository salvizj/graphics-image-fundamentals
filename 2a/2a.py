import math
import matplotlib.pyplot as plt
import cv2
import numpy as np

def get_grayscale_matrix(image_path):
    matrix= cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if matrix is None:  
        raise FileNotFoundError(f"Error: Unable to load image at '{image_path}'")

    return matrix

def dft(input_list, inverse=False):
    N = len(input_list)
    output_list= [0.0j for _ in range(N)]

    sign = -1 if inverse else 1

    for k in range(N):
        sum_value = 0.0 + 0.0j

        for n in range(N):
            angle = 2 * math.pi * k * n / N

            sum_value += input_list[n] * (math.cos(angle) + sign * 1j * math.sin(angle))  

        if inverse:
            sum_value /= N

        output_list[k] = sum_value  

    return output_list

def dft2d(matrix, inverse=False):
    rows, cols = len(matrix), len(matrix[0])
    result_matrix = [[0.0j for _ in range(cols)] for _ in range(rows)]

    for j in range(cols):
        column_data = [matrix[i][j] for i in range(rows)]  
        transformed_col = dft(column_data, inverse)  
        for i in range(rows):
            result_matrix[i][j] = transformed_col[i]  

    for i in range(rows):
        result_matrix[i] = dft(result_matrix[i], inverse)  

    return result_matrix

def main():
    img_path = './img.png'

    img_matrix = get_grayscale_matrix(img_path)

    dft_matrix = dft2d(img_matrix)
    magnitude_spectrum_dft = np.log(1 + np.array(np.abs(dft_matrix)))

    idft_matrix = dft2d(dft_matrix, inverse=True)
    reconstructed_image_dft = np.real(np.array(idft_matrix)).astype(np.uint8)

    # Comparing results to built in FFT and IFFT
    fft_matrix = np.fft.fft2(img_matrix)
    magnitude_spectrum_fft = np.log(1 + np.abs(fft_matrix))

    ifft_matrix = np.fft.ifft2(fft_matrix)
    reconstructed_image_fft = np.real(ifft_matrix).astype(np.uint8)

    plt.figure(figsize=(12, 10))

    plt.subplot(2, 2, 1)
    plt.imshow(magnitude_spectrum_dft, cmap='gray')
    plt.colorbar()
    plt.title("DFT magnitude Spectrum")

    plt.subplot(2, 2, 2)
    plt.imshow(reconstructed_image_dft, cmap='gray')
    plt.title("IDFT")

    plt.subplot(2, 2, 3)
    plt.imshow(magnitude_spectrum_fft, cmap='gray')
    plt.colorbar()
    plt.title("Numpy FFT Magnitude Spectrum")

    plt.subplot(2, 2, 4)
    plt.imshow(reconstructed_image_fft, cmap='gray')
    plt.title("Numpy IFFT")

    plt.show()

if __name__ == "__main__":
    main()

