from _transform_ import *
import cv2

# This module performs vanishing point rectification on an image
# The user selects points on the image to create vanishing lines
# After the vanishing lines are created, the vanishing points are calculated
# After the vanishing points are calculated, a homography matrix is created
# After the homography is created, the image is then rectified

im_name = 'some_image'
img = cv2.imread(im_name+'.jpg')
selectedPts = []

def getCrossProduct(x1, y1, z1, x2, y2, z2):
    a = y1*z2 - y2*z1
    b = z1*x2 - x1*z2
    c = x1*y2 - y1*x2
    return a, b, c

def calcVPs(lns):
    vps = []
    for i in range(2):
        vp_x, vp_y, vp_z = getCrossProduct(lns[i*2+0][0], lns[i*2+0][1], \
                                                   lns[i*2+0][2], \
                                           lns[i*2+1][0], lns[i*2+1][1], \
                                                   lns[i*2+1][2])
        print("vanishing point: ", vp_x/vp_z, vp_y/vp_z, vp_z/vp_z)
        vps.append([vp_x/vp_z, vp_y/vp_z, vp_z/vp_z])
    return vps

def calcParLines():
    lns = []
    for i in range(4):
        x1 = selectedPts[2*i + 0][0]
        y1 = selectedPts[2*i + 0][1]
        x2 = selectedPts[2*i + 1][0]
        y2 = selectedPts[2*i + 1][1]
        a, b, c = getCrossProduct(x1, y1, 1, x2, y2, 1)
        lns.append([a/c, b/c, c/c])

        xa, ya = 0, int(-c/b)
        xb, yb = img.shape[1], int((-c-a*img.shape[1])/b)
        cv2.line(img, (xa, ya), (xb, yb), (255, 255, 0), 1)

    cv2.imshow("Select points", img)
    cv2.imwrite(im_name + "_lines.jpg", img)
    vps = calcVPs(lns)

    print("\ncalculating homography...")
    h_matrix = getHomography(vps)

    print("\nrectifying...")
    final = rectify(h_matrix)

    cv2.imshow(im_name+" rectified", final)
    cv2.imwrite(im_name+"_rect.jpg", final)

def mouseCallback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img, (x,y), 5, (0, 255, 0), -1)
        selectedPts.append([x,y])
        cv2.imshow("Select points", img)
        if (len(selectedPts) == 8):
            calcParLines()
            selectedPts.append(-1)

def getHomography(vps):
    vp1_x = vps[0][0]
    vp1_y = vps[0][1]
    vp1_z = vps[0][2]

    vp2_x = vps[1][0]
    vp2_y = vps[1][1]
    vp2_z = vps[1][2]

    h_a, h_b, h_c = getCrossProduct(vp1_x, vp1_y, vp1_z, vp2_x, vp2_y, vp2_z)
    h_matrix = [[1, 0, 0],
                [0, 1, 0],
                [h_a/h_c, h_b/h_c, h_c/h_c]]
    print("\thomography:")
    for line in h_matrix:
        print("\t", line)

    return h_matrix

def rectify(h):
    return(transform(img, h))

cv2.namedWindow("Select points")
cv2.setMouseCallback("Select points", mouseCallback)
cv2.imshow("Select points", img)

cv2.waitKey(0)
