import cv2
import numpy as np
import math

theta=0
minLineLength = 5
maxLineGap = 10
maxSlider = 10

cap = cv2.VideoCapture(0)

if not cap.isOpened():
 print("Cannot open camera")

while(True):
    # Capture frame-by-frame
    ret, image = cap.read()

    cv2.imshow("Original", image)

    result = image.copy()

    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # lower boundary RED color range values; Hue (0 - 10)
    lower1 = np.array([0, 100, 20])
    upper1 = np.array([10, 255, 255])

    # upper boundary RED color range values; Hue (160 - 180)
    lower2 = np.array([160,100,20])
    upper2 = np.array([179,255,255])

    lower_mask = cv2.inRange(image, lower1, upper1)
    upper_mask = cv2.inRange(image, lower2, upper2)

    full_mask = lower_mask + upper_mask;

    result = cv2.bitwise_and(result, result, mask=full_mask)

    canny = cv2.Canny(result, 100, 200)

    lines = cv2.HoughLinesP(canny, 1, np.pi/180, maxSlider, minLineLength, maxLineGap)

    try:
        for x in range(0, len(lines)):
            for x1,y1,x2,y2 in lines[x]:
                # draw line in image using cv2.line function.
                cv2.line(image,(x1,y1),(x2,y2),(255,0,0),3)
                theta=theta+math.atan2((y2-y1),(x2-x1))
                print(theta)
    except:
        print("No lines detected")


    cv2.imshow('mask', full_mask)
    cv2.imshow('result', result)
    cv2.imshow('canny', canny)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()