import cv2 as cv
import numpy as np

# main image
img = cv.imread(r'your_image_here.jpg')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

display = cv.resize(gray, (512, 512), interpolation=cv.INTER_CUBIC)
cv.imshow("Chessboard", display)

# reference image
img2 = cv.imread(r'your_reference_image_here.jpg')
gray2 = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
display2 = cv.resize(gray2, (512, 512), interpolation=cv.INTER_CUBIC)
cv.imshow("Chessboard Reference", display2)

# px value array for empty board reference
rows, cols = (8, 8)
arr = [[0 for _ in range(cols)] for _ in range(rows)]
ave = [[0 for _ in range(cols)] for _ in range(rows)]


# assigning chessboard squares
chessboard_squares = [
    ["A8", "B8", "C8", "D8", "E8", "F8", "G8", "H8"],
    ["A7", "B7", "C7", "D7", "E7", "F7", "G7", "H7"],
    ["A6", "B6", "C6", "D6", "E6", "F6", "G6", "H6"],
    ["A5", "B5", "C5", "D5", "E5", "F5", "G5", "H5"],
    ["A4", "B4", "C4", "D4", "E4", "F4", "G4", "H4"],
    ["A3", "B3", "C3", "D3", "E3", "F3", "G3", "H3"],
    ["A2", "B2", "C2", "D2", "E2", "F2", "G2", "H2"],
    ["A1", "B1", "C1", "D1", "E1", "F1", "G1", "H1"],
]

k = 0
l = 0

i = 0
j = 0


def find_occupancy(arr, ave, chessboard_squares, display, i, j):

     square = display[(j * 64):((j + 1) * 64), (i * 64):((i + 1) * 64)]
     if (i % 2 != 0 and j % 2 != 0) or (i % 2 == 0 and j % 2 == 0):
        square = cv.medianBlur(square, 5)
        thresh_square = cv.adaptiveThreshold(square, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 101, 14)
        num_black_square = np.sum(thresh_square == 0)
        cv.imshow("Sqr", thresh_square)

        if num_black_square >= 2.2 * arr[j][i] and num_black_square > 130:
            print(f'Square {chessboard_squares[j][i]} is occupied')
     else:
        if (np.mean(square) < (0.50 * ave[j][i])) or (np.min(square) < 40 and np.min(square) < (0.20 * ave[j][i])):
            print(f'Square {chessboard_squares[j][i]} is occupied.')
        if np.mean(square) > (1.1 * ave[j][i]) and np.mean(square) >= (ave[j][i] + 20) and np.mean(square) >= 140:
            print(f'Square {chessboard_squares[j][i]} is occupied.')


# reference pixel numbers
def comparison(arr, ave, display2, k, l):

    while k < 8:
        l = 0
        while l < 8:
            square = display2[(l * 64):((l + 1) * 64), (k * 64):((k + 1) * 64)]
            if (l % 2 != 0 and k % 2 != 0) or (l % 2 == 0 and k % 2 == 0):
                square = cv.medianBlur(square, 5)
                thresh_square = cv.adaptiveThreshold(square, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 101, 14)
                num_black_square = np.sum(thresh_square == 0)
                arr[l][k] = num_black_square

            else:
                ave[l][k] = np.mean(square)
            l += 1

        k += 1

    return arr, ave

comparison(arr, ave, display2, l, k)

# main occupancy loop
while i < 8:
    j = 0
    while j < 8:
        find_occupancy(arr, ave, chessboard_squares, display, i, j)
        j += 1
    i += 1

cv.waitKey(0)
