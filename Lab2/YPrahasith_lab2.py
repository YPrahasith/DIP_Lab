# Program for image enhancement using pixel operations

from PIL import Image
import math

def linear_indentity(img):

    for i in range(img.width):
        for j in range(img.height):
            px = img.getpixel((i, j))
            img.putpixel((i, j), px)

    # img.show()
    img.save('identity.png')

def linear_negative(img):

    for i in range(img.width):
        for j in range(img.height):
            px = img.getpixel((i, j))
            img.putpixel((i, j), (px[1]-px[0], px[1]))

    # img.show()
    img.save('negative.png')

def logarithmic(img, c=31.875):

    for i in range(img.width):
        for j in range(img.height):
            px = img.getpixel((i, j))
            img.putpixel((i, j), (int(c * math.log(px[0]+1, 2)), px[1]))
    
    # img.show()
    img.save('logarithmic.png')

def power(img, gamma, c=31.875):

    for i in range(img.width):
        for j in range(img.height):
            px = img.getpixel((i, j))
            img.putpixel((i, j), (int(c * (px[0] ** (1/gamma))), px[1]))
    
    # img.show()
    img.save('power.png')

def piecewise_contrast_stretching(img, a, b, l, m, n, v, w):

    for i in range(img.width):
        for j in range(img.height):
            px = img.getpixel((i, j))
            if px[0] < a:
                img.putpixel((i, j), (int(l*px[0]), px[1]))
            elif a <= px[0] <= b:
                img.putpixel((i, j), (int(m*(px[0]-a)+v), px[1]))
            else:
                img.putpixel((i, j), (int(n*(px[0]-b)+w), px[1]))

    # img.show()
    img.save('contrast_stretching.png')

def piecewise_clipping(img, a, b):

    for i in range(img.width):
        for j in range(img.height):
            px = img.getpixel((i, j))
            if px[0] < a:
                img.putpixel((i, j), (0, px[1]))
            elif a <= px[0] <= b:
                img.putpixel((i, j), (int(((px[1]/(b-a))*px[0])), px[1]))
            else:
                img.putpixel((i, j), (px[1], px[1]))
        
    # img.show()
    img.save('clipping.png')

def piecewise_thresholding(img, t):

    for i in range(img.width):
        for j in range(img.height):
            px = img.getpixel((i, j))
            if px[0] >= t:
                img.putpixel((i, j), px)
            else:
                img.putpixel((i, j), (0, px[1]))

    # img.show()
    img.save('thresholding.png')

if __name__ == '__main__':
    
    img_name = input('Image filename: ')
    img = Image.open(img_name).convert('LA')

    print('1. Identity\n2. Negative\n3. Logarithmic\n4. Power\n5. Contrast Stretching\n6. Clipping\n7. Thresholding')
    choice = int(input('Pick required operation: '))

    if choice == 1:
        linear_indentity(img)
    
    elif choice == 2:
        linear_negative(img)

    elif choice == 3:
        c = float(input('c = '))
        logarithmic(img, c)

    elif choice == 4:
        c = float(input('c = '))
        gamma = float(input('Gamma = '))
        power(img, gamma, c)

    elif choice == 5:
        a, b = map(int, input('Input range = ').split())
        l, m, n = map(int, input('3 slopes = ').split())
        v, w = map(int, input('Output range = ').split())
        piecewise_contrast_stretching(img, a, b, l, m, n, v, w)

    elif choice == 6:
        a, b = map(int, input('Range = ').split())
        piecewise_clipping(img, a, b)

    elif choice == 7:
        threshold = int(input('Threshold = '))
        piecewise_thresholding(img, threshold)

    else:
        print('Invalid choice!')