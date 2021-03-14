import cv2
import numpy as np


def nothing(x):
    pass

cam=cv2.VideoCapture(0)
cv2.namedWindow("Trackbars", cv2.WINDOW_AUTOSIZE)

#create trackbars for colour change
noise_variable=500

cv2.createTrackbar("low_H","Trackbars",0,179,nothing)
cv2.createTrackbar("high_H","Trackbars",179,179,nothing)
cv2.createTrackbar("low_S","Trackbars",0,255,nothing)
cv2.createTrackbar("high_S","Trackbars",255,255,nothing)
cv2.createTrackbar("low_V","Trackbars",0,255,nothing)
cv2.createTrackbar("high_V","Trackbars",255,255,nothing)
cv2.createTrackbar("dilation","Trackbars", 0, 10, nothing)
cv2.createTrackbar("erosion", "Trackbars", 0, 10, nothing)

while True:
    ret, frame= cam.read()
    if not ret:
        break
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV) # converting image to hsv format
    # getting trackbar values
    Low_H=cv2.getTrackbarPos("low_H","Trackbars")
    High_H = cv2.getTrackbarPos("high_H", "Trackbars")
    Low_S = cv2.getTrackbarPos("low_S", "Trackbars")
    High_S = cv2.getTrackbarPos("high_S", "Trackbars")
    Low_V = cv2.getTrackbarPos("low_V", "Trackbars")
    High_V = cv2.getTrackbarPos("high_V", "Trackbars")
    ero = cv2.getTrackbarPos("erosion", "Trackbars")
    dilat = cv2.getTrackbarPos("dilation","Trackbars")


    lower_range = np.array([Low_H, Low_S, Low_V])
    upper_range=np.array([High_H,High_S,High_V])
    mask=cv2.inRange(hsv,lower_range,upper_range)
    mask = cv2.erode(mask, None, iterations=ero)
    mask = cv2.dilate(mask, None, iterations=dilat)
    result = cv2.bitwise_and(frame, frame, mask=mask)
    new_mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    stacked = np.hstack((new_mask, frame, result))
    cv2.imshow("res",stacked)

    # drawing rectangle
    """" contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours and cv2.contourArea(max(contours,key=cv2.contourArea))>noise_variable:
        max_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(max_contour)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(69,200,21),1)

    cv2.imshow("image",frame) """""
    key=cv2.waitKey(1)
    if key==27: # if user presses esc, then loop is finished
        break
    if key==ord("s"): # if user presses s, then calibrated values are printed
        calibrated_array=[[Low_H,Low_S,Low_V],[High_H,High_S,High_V]]
        print(calibrated_array)
        break

cam.release()
cv2.destroyAllWindows()





