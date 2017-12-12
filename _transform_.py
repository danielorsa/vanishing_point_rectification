import numpy as np

# This module performs vanishing point rectification on an image by applying a homography to the image

def transform(im1, h):
    im1Height = im1.shape[0]
    im1Width = im1.shape[1]

    im1_topLeft = [[0],
                   [0],
                   [1]]
    im1_topRight = [[im1Width-1],
                    [0],
                    [1]]
    im1_bottomLeft = [[0],
                      [im1Height-1],
                      [1]]
    im1_bottomRight = [[im1Width-1],
                       [im1Height-1],
                       [1]]

    rect_topLeft = np.dot(h, im1_topLeft)
    rect_topLeft = np.round(np.multiply((1/rect_topLeft[2][0]), rect_topLeft)).astype(int)

    rect_topRight = np.dot(h, im1_topRight)
    rect_topRight = np.round(np.multiply((1/rect_topRight[2][0]), rect_topRight)).astype(int)

    rect_bottomLeft = np.dot(h, im1_bottomLeft)
    rect_bottomLeft = np.round(np.multiply((1 / rect_bottomLeft[2][0]), rect_bottomLeft)).astype(int)

    rect_bottomRight = np.dot(h, im1_bottomRight)
    rect_bottomRight = np.round(np.multiply((1/rect_bottomRight[2][0]), rect_bottomRight)).astype(int)

    print("\nim1 corners:")
    print("\ttop left ({0}, {1})".format(0, 0))
    print("\ttop right ({0}, {1})".format(im1Width-1, 0))
    print("\tbottom left ({0}, {1})".format(0, im1Height-1))
    print("\tbottom right ({0}, {1})".format(im1Width-1, im1Height-1))

    print("\nafter applying homography")
    print("\ttop left ({0}, {1})".format(rect_topLeft[0], rect_topLeft[1]))
    print("\ttop right ({0}, {1})".format(rect_topRight[0], rect_topRight[1]))
    print("\tbottom left ({0}, {1})".format(rect_bottomLeft[0], rect_bottomLeft[1]))
    print("\tbottom right ({0}, {1})".format(rect_bottomRight[0], rect_bottomRight[1]))

    # find dimensions of rectified image
    im1warpedLeftSideHeight = rect_bottomLeft[1] - rect_topLeft[1]
    im1warpedRightSideHeight = rect_bottomRight[1] - rect_topRight[1]
    im1warpedHeight = max(im1warpedLeftSideHeight, im1warpedRightSideHeight)

    im1warpedTopWidth = rect_topRight[0] - rect_topLeft[0]
    im1warpedBottomWidth = rect_bottomRight[0] - rect_bottomLeft[0]
    im1warpedWidth = max(im1warpedTopWidth, im1warpedBottomWidth)

    # determine x-offset and y-offset
    xOffset = 0
    yOffset = 0
    if rect_topLeft[0] < 0 or rect_bottomLeft[0] < 0:
        xOffset = min(rect_topLeft[0], rect_bottomLeft[0])
        xOffset = int(abs(xOffset))
    if rect_topLeft[1] < 0 or rect_topRight[1] < 0:
        yOffset = min(rect_topLeft[1], rect_topRight[1])
        yOffset = int(abs(yOffset))
    print("x-offset: {0}, y-offset: {1}".format(xOffset, yOffset))

    # find size of rectification
    rect_width = int(max(im1Width+xOffset, im1warpedWidth, rect_topRight[0], rect_bottomRight[0]))+xOffset
    rect_height = int(max(im1Height+yOffset, im1warpedHeight, rect_bottomLeft[1], rect_bottomRight[1]))+yOffset
    print("\ntransformed - H({0}), W({1})".format(rect_height, rect_width))

    transformed = np.zeros((rect_height, rect_width, 3), np.uint8)
    hInv = np.linalg.inv(h)

    # create image rectified by vanishing points
    for i in range(len(transformed)):
        for j in range(len(transformed[i])):
            vector = [[j-xOffset],
                      [i-yOffset],
                      [1]]
            warpVector = np.dot(hInv, vector)
            warpVector = np.multiply(1/warpVector[-1], warpVector)
            warpedX = int(warpVector[0][0])
            warpedY = int(warpVector[1][0])
            try:
                if (warpedX > 0 and warpedX < im1Width) and (warpedY > 0 and warpedY < im1Height):
                    transformed[i][j] = im1[warpedY][warpedX]

            except IndexError:
                pass

    return transformed