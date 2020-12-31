# Program for detecting edges in an image using Roberts cross gradient operator, prewitt operator and sobel operator.

from PIL import Image
import math

def robert_operator(img):
    Gx = [[1, 0], [0, -1]]
    Gy = [[0, 1], [-1, 0]]

    robert = Image.new('L', (img.width, img.height))

    for i in range(img.width-1):
        for j in range(img.height-1):
            x, y = 0, 0
            for p in range(2):
                for q in range(2):
                    x += (img.getpixel((i+p, j+q)) * Gx[p][q])
                    y += (img.getpixel((i+p, j+q)) * Gy[p][q])
            robert.putpixel((i, j), int(math.sqrt(((x**2)+(y**2)))))

    # robert.show()
    robert.save('robert.png')

def prewitt_operator(img):
    Gx = [[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]
    Gy = [[1, 1, 1], [0, 0, 0], [-1, -1, -1]]

    prewitt = Image.new('L', (img.width, img.height))

    for i in range(1, img.width-1):
        for j in range(1, img.height-1):
            x, y = 0, 0
            for p in [-1, 0, 1]:
                for q in [-1, 0, 1]:
                    x += (img.getpixel((i+p, j+q)) * Gx[p+1][q+1])
                    y += (img.getpixel((i+p, j+q)) * Gy[p+1][q+1])
            prewitt.putpixel((i, j), int(math.sqrt(((x**2)+(y**2)))))

    # prewitt.show()
    prewitt.save('prewitt.png')

def sobel_operator(img):
    Gx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    Gy = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]

    sobel = Image.new('L', (img.width, img.height))

    for i in range(1, img.width-1):
        for j in range(1, img.height-1):
            x, y = 0, 0
            for p in [-1, 0, 1]:
                for q in [-1, 0, 1]:
                    x += (img.getpixel((i+p, j+q)) * Gx[p+1][q+1])
                    y += (img.getpixel((i+p, j+q)) * Gy[p+1][q+1])
            sobel.putpixel((i, j), int(math.sqrt(((x**2)+(y**2)))))

    # sobel.show()
    sobel.save('sobel.png')

if __name__ == '__main__':
    
    img_name = input('Image filename: ')
    img = Image.open(img_name).convert('L')

    print('1. Robert operator\n2. Prewitt operator\n3. Sobel operator')
    choice = int(input('Pick required operation: '))

    if choice == 1:
        robert_operator(img)

    elif choice == 2:
        prewitt_operator(img)

    elif choice == 3:
        sobel_operator(img)

    else:
        print('Invalid choice!')