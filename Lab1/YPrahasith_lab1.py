# Program to enhance image using image arithmetic and logical operations

from PIL import Image

def arithmetic_addition(img1, img2):

    for i in range(img1.width):
        for j in range(img1.height):
            px1 = img1.getpixel((i, j))
            if i < img2.width and j < img2.height:
                px2 = img2.getpixel((i, j))
                tmp = []
                for k in range(len(px1)):
                    tmp.append(min(255, px1[k]+px2[k]))
                px1 = tuple(tmp)
            img1.putpixel((i, j), px1)

    # img1.show()
    img1.save('addition.png')

def arithmetic_subtraction(img1, img2):

    for i in range(img1.width):
        for j in range(img1.height):
            px1 = img1.getpixel((i, j))
            if i < img2.width and j < img2.height:
                px2 = img2.getpixel((i, j))
                tmp = []
                for k in range(len(px1)):
                    tmp.append(max(0, px1[k]-px2[k]))
                px1 = tuple(tmp)
            img1.putpixel((i, j), px1)

    # img1.show()
    img1.save('subtraction.png')

def arithmetic_multiplication(img1, img2):

    for i in range(img1.width):
        for j in range(img1.height):
            px1 = img1.getpixel((i, j))
            if i < img2.width and j < img2.height:
                px2 = img2.getpixel((i, j))
                tmp = []
                for k in range(len(px1)):
                    tmp.append(min(255, px1[k]*px2[k]))
                px1 = tuple(tmp)
            img1.putpixel((i, j), px1)

    # img1.show()
    img1.save('multiplication.png')

def arithmetic_division(img1, img2):

    for i in range(img1.width):
        for j in range(img1.height):
            px1 = img1.getpixel((i, j))
            if i < img2.width and j < img2.height:
                px2 = img2.getpixel((i, j))
                tmp = []
                for k in range(len(px1)):
                    if px2[k] > 0:
                        tmp.append(max(0, px1[k]//px2[k]))
                    else:
                        tmp.append(255)
                px1 = tuple(tmp)
            img1.putpixel((i, j), px1)

    # img1.show()
    img1.save('division.png')

def logical_and(img1, img2):

    for i in range(img1.width):
        for j in range(img1.height):
            px1 = img1.getpixel((i, j))
            if i < img2.width and j < img2.height:
                px2 = img2.getpixel((i, j))
                tmp = []
                for k in range(len(px1)):
                    tmp.append(px1[k]&px2[k])
                px1 = tuple(tmp)
            img1.putpixel((i, j), px1)

    # img1.show()
    img1.save('and.png')

def logical_or(img1, img2):

    for i in range(img1.width):
        for j in range(img1.height):
            px1 = img1.getpixel((i, j))
            if i < img2.width and j < img2.height:
                px2 = img2.getpixel((i, j))
                tmp = []
                for k in range(len(px1)):
                    tmp.append(px1[k]|px2[k])
                px1 = tuple(tmp)
            img1.putpixel((i, j), px1)

    # img1.show()
    img1.save('or.png')

def logical_xor(img1, img2):

    for i in range(img1.width):
        for j in range(img1.height):
            px1 = img1.getpixel((i, j))
            if i < img2.width and j < img2.height:
                px2 = img2.getpixel((i, j))
                tmp = []
                for k in range(len(px1)):
                    tmp.append(px1[k]^px2[k])
                px1 = tuple(tmp)
            img1.putpixel((i, j), px1)

    # img1.show()
    img1.save('xor.png')

if __name__ == '__main__':

    print('1. Addition\n2. Subtraction\n3. Multiplication\n4. Division\n5. And\n6. Or\n7. Xor')
    choice = int(input('Pick required operation: '))
    
    img_name1 = input('Image 1 filename: ')
    img1 = Image.open(img_name1).convert('RGB')

    img_name2 = input('Image 2 filename: ')
    img2 = Image.open(img_name2).convert('RGB')

    if choice == 1:
        arithmetic_addition(img1, img2)

    elif choice == 2:
        arithmetic_subtraction(img1, img2)

    elif choice == 3:
        arithmetic_multiplication(img1, img2)

    elif choice == 4:
        arithmetic_division(img1, img2)

    elif choice == 5:
        logical_and(img1, img2)

    elif choice == 6:
        logical_or(img1, img2)

    elif choice == 7:
        logical_xor(img1, img2)

    else:
        print('Invalid choice!')
