# Morphological image operations:
#   - Erosion
#   - Dilation
#   - Opening
#   - Closing
#   - Thinning
#   - Thickening
#   - Skeletons
#   - Pruning
#   - Boundary Extraction
#   - Hole Filling
#   - Extraction of Connected Components

import imageio
import numpy as np

image = imageio.imread("horse.png", "PNG", pilmode="1")


def erode(img, se):
    se_size_rows = se.shape[0]
    se_size_cols = se.shape[1]
    row_pad = (se_size_rows - 1) // 2
    col_pad = (se_size_cols - 1) // 2

    padded_img = np.pad(
        array=img,
        pad_width=((row_pad, row_pad), (col_pad, col_pad)),
        mode="constant",
        constant_values=0,
    )
    padded_img_size_rows = padded_img.shape[0]
    padded_img_size_cols = padded_img.shape[1]

    result = np.zeros(padded_img.shape, dtype=np.uint8)

    for i, row in enumerate(img):
        for j, _ in enumerate(row):
            match = True

            for img_px, se_px in zip(
                padded_img[i : i + 2 * row_pad + 1, j : j + 2 * col_pad + 1].flatten(),
                se.flatten(),
            ):
                if se_px != 1:
                    continue

                if img_px != se_px:
                    match = False
                    break

            if match:
                result[i + row_pad][j + col_pad] = 1

    return result[
        row_pad : padded_img_size_rows - row_pad,
        col_pad : padded_img_size_cols - col_pad,
    ]


def dilate(img, se):
    se_size_rows = se.shape[0]
    se_size_cols = se.shape[1]
    row_pad = (se_size_rows - 1) // 2
    col_pad = (se_size_cols - 1) // 2

    padded_img = np.pad(
        array=img,
        pad_width=((row_pad, row_pad), (col_pad, col_pad)),
        mode="constant",
        constant_values=0,
    )
    padded_img_size_rows = padded_img.shape[0]
    padded_img_size_cols = padded_img.shape[1]

    result = np.zeros(padded_img.shape, dtype=np.uint8)

    for i, row in enumerate(img):
        for j, _ in enumerate(row):
            for img_px, se_px in zip(
                padded_img[i : i + 2 * row_pad + 1, j : j + 2 * col_pad + 1].flatten(),
                se.flatten(),
            ):
                if se_px != 1:
                    continue

                if img_px == se_px:
                    result[i + row_pad][j + col_pad] = 1
                    break

    return result[
        row_pad : padded_img_size_rows - row_pad,
        col_pad : padded_img_size_cols - col_pad,
    ]


def opening(img, se):
    return dilate(erode(img, se), se)


def closing(img, se):
    return erode(dilate(img, se), se)


def hit_miss_transform(img, se):
    se_size_rows = se.shape[0]
    se_size_cols = se.shape[1]
    row_pad = (se_size_rows - 1) // 2
    col_pad = (se_size_cols - 1) // 2

    padded_img = np.pad(
        array=img,
        pad_width=((row_pad, row_pad), (col_pad, col_pad)),
        mode="constant",
        constant_values=0,
    )
    padded_img_size_rows = padded_img.shape[0]
    padded_img_size_cols = padded_img.shape[1]

    result = np.zeros(padded_img.shape, dtype=np.uint8)

    for i, row in enumerate(img):
        for j, _ in enumerate(row):
            if (
                padded_img[i : i + 2 * row_pad + 1, j : j + 2 * col_pad + 1] == se
            ).all():
                result[i + row_pad][j + col_pad] = 1

    return result[
        row_pad : padded_img_size_rows - row_pad,
        col_pad : padded_img_size_cols - col_pad,
    ]


def thinning(img, se):
    return (img - hit_miss_transform(img, se)).clip(min=0, max=1)


def thickening(img, se):
    return (img + hit_miss_transform(img, se)).clip(min=0, max=1)


def skeleton(img, se):
    max_k = 0
    empty_erosion = False

    erosion = img
    skeletons = []
    while not empty_erosion:
        skeleton = (erosion - opening(erosion, se)).clip(min=0, max=1)
        skeletons.append(skeleton)

        erosion = erode(erosion, se)

        # Check if erosion is null set
        empty_erosion = not np.any(erosion)

        if not empty_erosion:
            max_k += 1

    return sum(skeletons).clip(min=0, max=1)


def pruning(img, ses, num_thinning_iter, num_dilation_iter):
    thinning_result = img  # x1

    for _ in range(num_thinning_iter):
        for se in ses:
            thinning_result = thinning(thinning_result, se)

    hmt_result = np.zeros(thinning_result.shape, dtype=np.uint8)  # x2
    for se in ses:
        hmt_result += hit_miss_transform(thinning_result, se)

    hmt_result = hmt_result.clip(min=0, max=1)

    dilation_se = np.array(
        [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
        ]
    )  # h

    dilation_result = hmt_result  # x3
    for _ in range(num_dilation_iter):
        dilation_result = np.bitwise_and(dilate(dilation_result, dilation_se), img)

    return (thinning_result + dilation_result).clip(min=0, max=1)


def extract_boundary(img, se):
    return (img - erode(img, se)).clip(min=0, max=1)


def fill_holes(img, se, holes):
    result = holes
    inverse = 255 - img
    terminate = False

    while not terminate:
        new_result = np.bitwise_and(dilate(result, se), inverse)

        if (new_result == result).all():
            terminate = True

        result = new_result

    return (img + result).clip(min=0, max=1)


def connected_components(img, se, comps):
    result = comps
    terminate = False

    while not terminate:
        new_result = np.bitwise_and(dilate(result, se), img)

        if (new_result == result).all():
            terminate = True

        result = new_result

    return result


structuring_element = np.array(
    [
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
    ]
)

image = (image / 255).astype(np.uint8)

result = erode(image, structuring_element) * 255
imageio.imwrite("erosion.png", result, "PNG")

result = dilate(image, structuring_element) * 255
imageio.imwrite("dilation.png", result, "PNG")

result = opening(image, structuring_element) * 255
imageio.imwrite("opening.png", result, "PNG")

result = closing(image, structuring_element) * 255
imageio.imwrite("closing.png", result, "PNG")

result = hit_miss_transform(image, structuring_element) * 255
imageio.imwrite("hit_miss_transform.png", result, "PNG")

result = thinning(image, structuring_element) * 255
imageio.imwrite("thinning.png", result, "PNG")

result = thickening(image, structuring_element) * 255
imageio.imwrite("thickening.png", result, "PNG")

result = skeleton(image, structuring_element) * 255
imageio.imwrite("skeleton.png", result, "PNG")

pruning_ses = [
    np.array([[0, 0, 0], [1, 1, 0], [0, 0, 0]]),
    np.array([[0, 0, 0], [1, 1, 0], [1, 0, 0]]),
    np.array([[1, 0, 0], [1, 1, 0], [0, 0, 0]]),
    np.array([[1, 0, 0], [1, 1, 0], [1, 0, 0]]),
    np.array([[0, 1, 0], [0, 1, 0], [0, 0, 0]]),
    np.array([[0, 1, 1], [0, 1, 0], [0, 0, 0]]),
    np.array([[1, 1, 0], [0, 1, 0], [0, 0, 0]]),
    np.array([[1, 1, 1], [0, 1, 0], [0, 0, 0]]),
    np.array([[0, 0, 0], [0, 1, 1], [0, 0, 0]]),
    np.array([[0, 0, 0], [0, 1, 1], [0, 0, 1]]),
    np.array([[0, 0, 1], [0, 1, 1], [0, 0, 0]]),
    np.array([[0, 0, 1], [0, 1, 1], [0, 0, 1]]),
    np.array([[0, 0, 0], [0, 1, 0], [0, 1, 0]]),
    np.array([[0, 0, 0], [0, 1, 0], [0, 1, 1]]),
    np.array([[0, 0, 0], [0, 1, 0], [1, 1, 0]]),
    np.array([[0, 0, 0], [0, 1, 0], [1, 1, 1]]),
    np.array([[1, 0, 0], [0, 1, 0], [0, 0, 0]]),
    np.array([[0, 0, 1], [0, 1, 0], [0, 0, 0]]),
    np.array([[0, 0, 0], [0, 1, 0], [0, 0, 1]]),
    np.array([[0, 0, 0], [0, 1, 0], [1, 0, 0]]),
]

digit_img = (imageio.imread("digit.png", "PNG", pilmode="1") / 255).astype(
    np.uint8
)
result = pruning(digit_img, pruning_ses, 2, 2) * 255
imageio.imwrite("pruning.png", result, "PNG")

boundary_se = np.array(
    [
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1],
    ]
)

result = extract_boundary(image, boundary_se) * 255
imageio.imwrite("boundary_extraction.png", result, "PNG")

hole_filling_se = np.array(
    [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0],
    ]
)

boundary = result
boundary = (boundary / 255).astype(np.uint8)
holes = np.zeros(boundary.shape, dtype=np.uint8)
holes[160, 200] = 1
result = fill_holes(boundary, hole_filling_se, holes) * 255
imageio.imwrite("hole_filling.png", result, "PNG")

comps = np.zeros(image.shape, dtype=np.uint8)
comps[160, 200] = 1
result = connected_components(image, boundary_se, comps) * 255
imageio.imwrite("connected_components.png", result, "PNG")
