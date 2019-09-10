import cv2
import numpy as np


def nothing (x) :
    pass

cap=cv2.VideoCapture(0)

#window for live change of color value
cv2.namedWindow('tracking')
cv2.createTrackbar('low h','tracking',97,255,nothing)
cv2.createTrackbar('low s','tracking',88,255,nothing)
cv2.createTrackbar('low v','tracking',103,255,nothing)

cv2.createTrackbar('high h','tracking', 193,255,nothing)
cv2.createTrackbar('high s','tracking',255,255,nothing)
cv2.createTrackbar('high v','tracking',255,255,nothing)


while True:
    ret,frame=cap.read()

    #adding the hsv mask
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    low_h= cv2.getTrackbarPos('low h','tracking')
    low_s= cv2.getTrackbarPos('low s','tracking')
    low_v= cv2.getTrackbarPos('low v','tracking')

    high_h= cv2.getTrackbarPos('high h', 'tracking')
    high_s= cv2.getTrackbarPos('high s', 'tracking')
    high_v= cv2.getTrackbarPos('high v', 'tracking')

    #setting the viseble colors:

    min=np.array([low_h,low_s,low_v])
    max=np.array([high_h,high_s, high_v])


    #applying the filtering mask
    filter=cv2.inRange(hsv,min,max)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(filter, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    if len(cnts) > 0:

        areas = [cv2.contourArea(c) for c in cnts]
        print(areas)
        max_index = np.argmax(areas)
        c = cnts[max_index]

        ((x, y), radius) = cv2.minEnclosingCircle(c)

        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        print("center")

        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
        cv2.circle(frame, center, 3, (0, 0, 255), -1)

    #showing the result:
    cv2.imshow('raw footge',frame)
    cv2.imshow('mask',mask)
    #qwcv2.imshow('res', res)

    if cv2.waitKey(1)& 0xFF==ord('q'):
               break

cap.release()
cv2.destroyAllWindows()