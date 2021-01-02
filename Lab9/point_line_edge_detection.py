# Points, lines and edges detection
import imageio
import numpy as np

image = imageio.imread("input.png", "PNG", pilmode="L")

# fmt: off

point_laplacian_kernel = np.array(
    [
        [1,  1,  1],
        [1, -8,  1],
        [1,  1,  1],
    ]
)

line_horizontal_kernel = np.array(
    [
        [-1, -1, -1],
        [ 2,  2,  2],
        [-1, -1, -1],
    ]
)

line_vertical_kernel = np.array(
    [
        [-1,  2, -1],
        [-1,  2, -1],
        [-1,  2, -1],
    ]
)

line_plus_45_kernel = np.array(
    [
        [ 2, -1, -1],
        [-1,  2, -1],
        [-1, -1,  2],
    ]
)

line_minus_45_kernel = np.array(
    [
        [-1, -1,  2],
        [-1,  2, -1],
        [ 2, -1, -1],
    ]
)

# fmt: on

row_pad = 1
column_pad = 1

# Pad the image with sufficient number of zeros
padded_image = np.pad(
    array=image,
    pad_width=((column_pad, column_pad), (row_pad, row_pad)),
    mode="edge",
)


def threshold_image(img, threshold):
    result = np.zeros(img.shape, dtype=np.uint8)

    for i, row in enumerate(img):
        for j, value in enumerate(row):
            if value > threshold:
                result[i][j] = 255

    return result


# Create arrays of same shape as padded image
points = np.zeros(padded_image.shape, dtype=int)
lines_horizontal = np.zeros(padded_image.shape, dtype=int)
lines_plus_45 = np.zeros(padded_image.shape, dtype=int)
lines_vertical = np.zeros(padded_image.shape, dtype=int)
lines_minus_45 = np.zeros(padded_image.shape, dtype=int)

# Convolve image with kernels
for i, row in enumerate(image):
    for j, _ in enumerate(row):
        points[i + row_pad][j + column_pad] = (
            point_laplacian_kernel
            * padded_image[i : i + 2 * row_pad + 1, j : j + 2 * column_pad + 1]
        ).sum(dtype=int)

        lines_horizontal[i + row_pad][j + column_pad] = (
            line_horizontal_kernel
            * padded_image[i : i + 2 * row_pad + 1, j : j + 2 * column_pad + 1]
        ).sum(dtype=int)

        lines_vertical[i + row_pad][j + column_pad] = (
            line_vertical_kernel
            * padded_image[i : i + 2 * row_pad + 1, j : j + 2 * column_pad + 1]
        ).sum(dtype=int)

        lines_plus_45[i + row_pad][j + column_pad] = (
            line_plus_45_kernel
            * padded_image[i : i + 2 * row_pad + 1, j : j + 2 * column_pad + 1]
        ).sum(dtype=int)

        lines_minus_45[i + row_pad][j + column_pad] = (
            line_minus_45_kernel
            * padded_image[i : i + 2 * row_pad + 1, j : j + 2 * column_pad + 1]
        ).sum(dtype=int)

points = threshold_image(points[1:-1, 1:-1].clip(min=0, max=255).astype(np.uint8), 200)
lines_horizontal = threshold_image(
    lines_horizontal[1:-1, 1:-1].clip(min=0, max=255).astype(np.uint8), 200
)
lines_vertical = threshold_image(
    lines_vertical[1:-1, 1:-1].clip(min=0, max=255).astype(np.uint8), 200
)
lines_plus_45 = threshold_image(
    lines_plus_45[1:-1, 1:-1].clip(min=0, max=255).astype(np.uint8), 200
)
lines_minus_45 = threshold_image(
    lines_minus_45[1:-1, 1:-1].clip(min=0, max=255).astype(np.uint8), 200
)

imageio.imwrite("points.png", points, "PNG")
imageio.imwrite("lines_horizontal.png", lines_horizontal, "PNG")
imageio.imwrite("lines_vertical.png", lines_vertical, "PNG")
imageio.imwrite("lines_plus_45.png", lines_plus_45, "PNG")
imageio.imwrite("lines_minus_45.png", lines_minus_45, "PNG")

# Edge detection: Roberts, Prewitt, Sobel operators program in '07_edge_detection_roberts_prewitt_sobel' directory
