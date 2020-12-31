# Program to filter an image using averaging low pass filter in spatial domain and median filter

from PIL import Image

def low_pass_mean_filter(img):
    
    mean_img = Image.new('L', (img.width, img.height))

    for i in range(img.width):
        for j in range(img.height):
            total = 0
            n = 0
            for m in [-1, 0, 1]:
                for n in [-1, 0, 1]:
                    if 0 <= i+m < img.width and 0 <= j+n < img.height:
                        total += img.getpixel((i, j))
                        n += 1
            mean_img.putpixel((i, j), round(total/n))

    # mean_img.show()
    mean_img.save('mean.png')

def low_pass_median_filter(img):
    
    median_img = Image.new('L', (img.width, img.height))

    for i in range(img.width):
        for j in range(img.height):
            arr = []
            n = 0
            for m in [-1, 0, 1]:
                for n in [-1, 0, 1]:
                    if 0 <= i+m < img.width and 0 <= j+n < img.height:
                        arr.append(img.getpixel((i, j)))
                        n += 1
            arr.sort()
            median_img.putpixel((i, j), arr[n//2])

    # median_img.show()
    median_img.save('median.png')

if __name__ == '__main__':

    img_name = input('Image filename: ')
    img = Image.open(img_name).convert('L')

    print('1. Box/Mean Filter\n2. Median Filter')
    choice = int(input('Pick required operation: '))

    if choice == 1:
        low_pass_mean_filter(img)

    elif choice == 2:
        low_pass_median_filter(img)

    else:
        print('Invalid choice!')