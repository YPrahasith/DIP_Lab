# Program to sharpen an image using 2-D laplacian high pass filter in spatial domain.

from PIL import Image

def high_pass_laplacian_filter(img):
    
    laplacian_img = Image.new('L', (img.width, img.height))

    for i in range(img.width):
        for j in range(img.height):
            n = 0
            total = 0
            if i-1 >= 0:
                total += img.getpixel((i-1, j))
                n += 1
            if i+1 < img.width:
                total += img.getpixel((i+1, j))
                n += 1
            if j-1 >= 0:
                total += img.getpixel((i, j-1))
                n += 1
            if j+1 < img.height:
                total += img.getpixel((i, j+1))
                n += 1
            px = max(0, total - (n * img.getpixel((i, j))))
            laplacian_img.putpixel((i, j), px)

    # laplacian_img.show()
    laplacian_img.save('laplacian.png')

if __name__ == '__main__':
    
    img_name = input('Image filename: ')
    img = Image.open(img_name).convert('L')

    high_pass_laplacian_filter(img)