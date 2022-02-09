import numpy as np
from PIL import Image

def load_img(filename):
    img = Image.open(filename)
    pil_img = img.convert('RGB')
    arr = np.array(pil_img.getdata(), dtype=np.uint8).reshape(pil_img.height, pil_img.width, 3)
    img = [[(int(p[0]), int(p[1]), int(p[2])) for p in row] for row in arr]
    return img

def save_img(img, filename):
    # Checks for empty image
    if len(img) == 0:
        raise RuntimeError("Cannot save empty image")
    # Checks if first row is empty
    if len(img[0]) == 0:
        raise RuntimeError("Cannot save image where rows have length 0")
    # Checks if all rows have the same length
    for i in range(1, len(img)):
        if len(img[i]) != len(img[i - 1]):
            raise RuntimeError("Cannot save image where not all rows have the same length")
    arr = np.asarray(img, dtype=np.uint8)
    pil_img = Image.fromarray(arr)
    pil_img.save(filename, format='png')

def create_img(height, width, color):
    result = [None] * height
    for i in range(len(result)):
        result[i] = [color] * width
    return result

def height(img):
    return len(img)

def width(img):
    return len(img[0])

def summarize(img):
    return "Image[width=%s,height=%s]" % (width(img), height(img))

def img_str_to_file(img, filename):
    # Converting to integer pixel values
    img = np.asarray(img, dtype=np.uint8)

    # Calculating max length
    max_length = len(str((255, 255, 255)))

    # Limiting the number of rows and columns to be printed
    r_limit = min(20, height(img))
    c_limit = min(20, width(img))

    with open(filename, 'w') as file:
        pix_str = ""
        for y in range(r_limit):
            for x in range(c_limit):
                # Creating the string representation
                temp_str = ("(" + str(img[y][x][0])
                            + "," + str(img[y][x][1])
                            + "," + str(img[y][x][2]) + ")")
                pix_str += temp_str
                # Added appropriate number of spaces to make it visually clear
                pix_str += " " * (max_length - len(temp_str))
            pix_str += "\n"
        file.write(pix_str)

    return pix_str


img = load_img("img.png")

def matrix_transformation(x, y, img4):
    matrix = [[1] * 5] * 5
    new = [0, 0, 0]
    matrix_sum = 25
    for i in range(5):
        for j in range(5):
            new_x = x - 5 // 2 + i
            new_y = y - 5 // 2 + j
            if 0 <= new_x < len(img4) and new_y >= 0 and new_y < len(img4[0]):
                for k in range(3):
                    new[k] += img4[new_x][new_y][k] * matrix[i][j]
    for k in range(3):
        new[k] /= matrix_sum
    return tuple((int(new[0]), int(new[1]), int(new[2])))



def blur(img3):
    lst = []
    for i in range(len(img3)):
        listik = []
        for j in range(len(img3[i])):
            listik.append(matrix_transformation(i, j, img3))
        lst.append(listik)
    save_img(lst, "blurik.png")

blur(img)

def ottenki(img):
    lst = []
    for i in range(len(img)):
        listik = []
        for j in range(len(img[i])): #img[i][j] = kortezh
            grey = (img[i][j][0] + img[i][j][1] + img[i][j][2]) // 3
            listik.append((grey, grey, grey))
        lst.append(listik)
    save_img(lst, "new.png")  #name of the image is a str

ottenki(img)

def bnw(img2):
    lst = []
    for i in img2:
        listik = []
        for j in i:
            if ((j[0] + j[1] + j[2]) / 3) > 255/2:
                listik.append((255, 255, 255))
            else:
                listik.append((0, 0, 0))
        lst.append(listik)
    save_img(lst, "bnw.png")

bnw(img)

def tricolor(img1):
    lst = []
    for i in range(len(img1)):
        listik = []
        for j in range(len(img1[i])):
            if 0 <= j <= width(img1) // 3:
                listik.append(((img[i][j][0] + img[i][j][1] + img[i][j][2]) // 3, 0, 0))
            elif ((2 * width(img1)) // 3) < j < width(img1):
                listik.append((0, 0, (img[i][j][0] + img[i][j][1] + img[i][j][2]) // 3))
            else:
                listik.append((0, (img[i][j][0] + img[i][j][1] + img[i][j][2]) // 3, 0))
        lst.append(listik)
    save_img(lst, "tricolor.png")

tricolor(img)

def bottom_right(img):
    new_img = []
    for i in range(height(img) // 2, height(img)):
        line = []
        for j in range(width(img) // 2, width(img)):
            line.append(img[i][j])
        new_img.append(line)
    save_img(new_img, "bottom_right.png")

bottom_right(img)
