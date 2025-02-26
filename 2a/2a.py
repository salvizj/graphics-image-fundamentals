import matplotlib.pyplot as plt
import cv2
import math
import numpy as np

def get_grayscale_matrix(image_path):
    matrix= cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  
    return matrix

def dft(input_list, inverse):
    N = len(input_list)
    output_list = [0j] * N

    sign = 1 if inverse else -1  

    for k in range(N):
        for n in range(N):
            theta = (2 * math.pi * k * n) / N
            exp_term = complex(math.cos(theta), sign * math.sin(theta))  # e^(-j*theta)
            output_list[k] += input_list[n] * exp_term

        if inverse:
            output_list[k] /= N 
    return output_list

def dft2d(matrix, inverse=False):

    rows,cols = len(matrix),len(matrix[0])
    result_matrix = [[0j] * cols for _ in range(rows)] 

    # Step 1: Apply 1D DFT to each row
    for i in range(rows):
        result_matrix[i] = dft(matrix[i], inverse)  

    # Step 2: Apply 1D DFT to each column
    for j in range(cols):
        column_data = [result_matrix[i][j] for i in range(rows)]  # Extract column
        transformed_col = dft(column_data, inverse)  # Transform column
        for i in range(rows):
            result_matrix[i][j] = transformed_col[i]  # Store back

    return result_matrix

def main():
    image_path = 'img.png'  

    # Step 1: Load Image
    matrix = get_grayscale_matrix(image_path)

    # Step 2: Compute 2D DFT
    dft_matrix = dft2d(matrix)
    magnitude_spectrum_dft = np.abs(dft_matrix)
    magnitude_spectrum_dft = np.log(1 + magnitude_spectrum_dft)

    # Step 3: Compute Inverse 2D DFT
    idft_matrix = dft2d(dft_matrix, inverse=True)
    reconstructed_image_dft = np.real(idft_matrix).astype(np.uint8)

    # Step 4: Compute FFT (Fast Fourier Transform)
    fft_matrix = np.fft.fft2(matrix)
    fft_shifted = np.fft.fftshift(fft_matrix)
    magnitude_spectrum_fft = np.log(1 + np.abs(fft_shifted))

    # Step 5: Compute Inverse FFT
    ifft_matrix = np.fft.ifft2(fft_matrix)
    reconstructed_image_fft = np.real(ifft_matrix).astype(np.uint8)

    # Step 6: Plot Results
    plt.figure(figsize=(12, 10))

    # Row 1: DFT Results
    plt.subplot(2, 2, 1)
    plt.imshow(magnitude_spectrum_dft, cmap='gray')
    plt.colorbar()
    plt.title("DFT Magnitude Spectrum")

    plt.subplot(2, 2, 2)
    plt.imshow(reconstructed_image_dft, cmap='gray')
    plt.title("Reconstructed Image (IDFT)")

    # Row 2: FFT Results
    plt.subplot(2, 2, 3)
    plt.imshow(magnitude_spectrum_fft, cmap='gray')
    plt.colorbar()
    plt.title("FFT Magnitude Spectrum (Fast)")

    plt.subplot(2, 2, 4)
    plt.imshow(reconstructed_image_fft, cmap='gray')
    plt.title("Reconstructed Image (IFFT)")

    plt.show()

if __name__ == "__main__":
    main()

