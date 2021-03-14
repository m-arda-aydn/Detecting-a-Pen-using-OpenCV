import cv2
import numpy as np

Pen_Bool=False
counter=0
cam=cv2.VideoCapture(0)

kernel=np.ones((5,5),np.uint8)
noise_variable=150
canvas=None
x1,y1=0,0

while True:
    ret, frame = cam.read()
    frame = cv2.flip(frame, 1) # flipping video
    if not ret:
        break
    if canvas is None:
        canvas=np.zeros_like(frame)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # converting image to hsv format
    # calibrated values from part 1 for my pen
    Low_H = 116
    Low_S = 133
    Low_V = 80
    High_H = 135
    High_S = 255
    High_V = 255
    ero = 0
    dilat = 10

    lower_range = np.array([Low_H, Low_S, Low_V])
    upper_range = np.array([High_H, High_S, High_V])

    mask = cv2.inRange(hsv, lower_range, upper_range)
    mask = cv2.erode(mask, kernel, iterations=ero)
    mask = cv2.dilate(mask, kernel, iterations=dilat)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    key = cv2.waitKey(1) & 0xFF
    # if user presses e, then pen will start to draw while not drawing or will stop to draw while drawing
    if key==ord("e"):
        if Pen_Bool==False:
            Pen_Bool=True
        elif Pen_Bool==True:
            Pen_Bool=False
            counter=0

    if Pen_Bool==True:
        counter=counter+1
        if contours and cv2.contourArea(max(contours, key=cv2.contourArea)) > noise_variable:
            max_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(max_contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (69, 200, 21), 1)  # drawing rectangle
        if contours and cv2.contourArea(max(contours, key=cv2.contourArea)) > noise_variable:
            max_contour = max(contours, key=cv2.contourArea)
            x2, y2, w, h = cv2.boundingRect(max_contour)
            if x1 == 0 and y1 == 0 or counter==1:
                x1, y1 = x2, y2
            else:
                canvas = cv2.line(canvas, (x1, y1), (x2, y2), (126, 135, 241), 3)
            x1, y1 = x2, y2
        else:
            x1, y1 = 0, 0



    cv2.imshow("image", frame)
    # drawing the line on the canvas


    frame = cv2.add(frame, canvas)
    stacked = np.hstack((canvas, frame))
    cv2.imshow("Trackbars",canvas)


    if key == 27:  # if user presses esc, then loop is finished
        break
    if key==ord("c"):  # if user presses c, then canvas is cleaned
        canvas=None
    if key==ord("s"): # if user presses s, then canvas is saved
        cv2.imwrite("C:/Users/Arda/Documents/RASOpenCV/Canvas.jpg",canvas)
        break
cv2.destroyAllWindows()
cam.release()
