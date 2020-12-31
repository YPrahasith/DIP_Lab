# Program for gray level slicing with and without background

from PIL import Image

def gray_level_slicing_with_background(img, a, b):
    
    for i in range(img.width):
        for j in range(img.height):
            px = img.getpixel((i, j))
            if a <= px[0] <= b:
                img.putpixel((i, j), (px[1], px[1]))

    #img.show()
    img.save('gray_level_slicing_with_background.png')

def gray_level_slicing_without_background(img, a, b):
    
    for i in range(img.width):
        for j in range(img.height):
            px = img.getpixel((i, j))
            if a <= px[0] <= b:
                img.putpixel((i, j), (px[1], px[1]))
            else:
                img.putpixel((i, j), (0, px[1]))

    #img.show()
    img.save('gray_level_slicing_without_background.png')

if __name__ == '__main__':
    a = int(input('Lower value: '))
    b = int(input('Upper value: '))

    img_name = input('Image filename: ')
    img = Image.open(img_name).convert('LA')

    print('1. Gray level slicing with background\n2. Gray level slicing without background')
    
    choice = int(input('Pick required operation: '))

    if choice == 1:
        gray_level_slicing_with_background(img, a, b)

    elif choice == 2:
        gray_level_slicing_without_background(img, a, b)

    else:
        print('Invalid choice!')