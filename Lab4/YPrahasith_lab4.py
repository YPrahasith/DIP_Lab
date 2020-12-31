# Program for image enhancement using histogram equalization

from PIL import Image

def histogram_equalization(img):

    pixels = img.width * img.height
    grey_levels = img.getpixel((0, 0))[1] + 1

    arr = [0] * grey_levels

    for i in range(img.width):
        for j in range(img.height):
            px = img.getpixel((i, j))
            arr[px[0]] += 1

    for i in range(grey_levels):
        arr[i] = arr[i] / pixels

    for i in range(1, grey_levels):
        arr[i] += arr[i-1]

    for i in range(grey_levels):
        arr[i] *= (grey_levels - 1)

    for i in range(grey_levels):
        arr[i] = round(arr[i])

    # print(arr)

    for i in range(img.width):
        for j in range(img.height):
            px = img.getpixel((i, j))
            img.putpixel((i, j), (arr[px[0]], px[1]))

    # img.show()
    img.save('histogram_equalization.png')

if __name__ == '__main__':

    img_name = input('Image filename: ')
    img = Image.open(img_name).convert('LA')

    histogram_equalization(img)