import cv2 as cv
import pickle

weight,height = 140 , 60
try:
    with open ("carPosList", "rb") as f :
            posList = pickle.load(f)
except:
    posList = []



def mouseClick(event,x,y,flags,params):
    if event == cv.EVENT_LBUTTONDBLCLK:
        posList.append((x,y))

    if event == cv.EVENT_RBUTTONDBLCLK:
        for i,pos in enumerate(posList):
            x1,y1 = pos
            if x1<x<x + weight and y1<y<y1 + height :
                posList.pop(i)

    with open ("carPosList", "wb") as f :
        pickle.dump(posList ,f)



while True:
    img = cv.imread("22.png")
    for pos in posList:
        cv.rectangle(img ,pos ,(pos[0]+weight ,pos[1]+height) ,(255,0,255) ,2)
        
    cv.imshow("Result", img)
    cv.setMouseCallback("Result",mouseClick)

    cv.waitKey(1)






