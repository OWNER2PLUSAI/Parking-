# imports
from multiprocessing.context import SpawnContext
import cv2 as cv
import pickle
import numpy as np
import cvzone

# read video
cap = cv.VideoCapture("video.mp4")

# read site of car Pos from DB
with open("carPosList", "rb") as f:
    posList = pickle.load(f)


weight, height = 140, 60


def chechCarParking(imgPro):
    spaceCounter = 0

    for pos in posList:

        x, y = pos
        imgCrop = imgPro[y:y + height, x:x + weight]
        count = cv.countNonZero(imgCrop)
        cvzone.putTextRect(img, str(count), (x, y+height), scale=1, thickness=2, offset=0,
                           colorR=(0, 0, 255))

        # condition for show color
        if count < 900:
            color = (0, 255, 0)
            thickness = 5
            spaceCounter += 1
        else:
            color = (0, 0, 255)
            thickness = 2
        # show color place
        cv.rectangle(img, pos, (pos[0]+weight,
                     pos[1]+height), color, thickness)

        # show space counter
        cvzone.putTextRect(img, f"Free : {str(spaceCounter)}/{len(posList)}", (100, 50), scale=3, thickness=5,
                           offset=20, colorR=(0, 255, 0))


while True:

    if cap.get(cv.CAP_PROP_POS_FRAMES) == cap.get(cv.CAP_PROP_FRAME_COUNT):
        cap.set(cv.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()

    # Preprocessing

    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    imgBlur = cv.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv.adaptiveThreshold(
        imgBlur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilated = cv.dilate(imgMedian, kernel=kernel, iterations=1)

    # imgPro
    chechCarParking(imgDilated)

    cv.imshow("imgDilated", img)
    cv.waitKey(10)
