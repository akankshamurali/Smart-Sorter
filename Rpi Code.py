import cv2
import numpy as np
from picamera2 import Picamera2
import time
import serial
 
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640,480)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()


def nothing(x):
    # any operation
    pass

cv2.namedWindow("Trackbars")
cv2.createTrackbar("L-H", "Trackbars", 80, 180, nothing)
cv2.createTrackbar("L-S", "Trackbars", 159, 255, nothing)
cv2.createTrackbar("L-V", "Trackbars", 160, 255, nothing)
cv2.createTrackbar("U-H", "Trackbars", 125, 180, nothing)
cv2.createTrackbar("U-S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U-V", "Trackbars", 255, 255, nothing)

font = cv2.FONT_HERSHEY_COMPLEX
t = 0
ser = serial.Serial('/dev/ttyACM0', 9600);
ser.flush()
ser.close()
ser.open()
while True :
    t = t+1
    frame = picam2.capture_array()
    frame = frame[171:335,0:639]
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    l_h = cv2.getTrackbarPos("L-H", "Trackbars")
    l_s = cv2.getTrackbarPos("L-S", "Trackbars")
    l_v = cv2.getTrackbarPos("L-V", "Trackbars")
    u_h = cv2.getTrackbarPos("U-H", "Trackbars")
    u_s = cv2.getTrackbarPos("U-S", "Trackbars")
    u_v = cv2.getTrackbarPos("U-V", "Trackbars")

    lower_green = np.array([25, 27, 126])
    upper_green = np.array([94, 255, 255])
    
    lower_red = np.array([80, 159, 160])
    upper_red = np.array([125, 255, 255])
    
    lower_blue = np.array([130, 150, 123])
    upper_blue = np.array([176, 255, 255])
    
    lower_unknow = np.array([0, 81, 113])
    upper_unknow = np.array([180, 255, 255])    

    mask1 = cv2.inRange(hsv, lower_green, upper_green)
    mask2 = cv2.inRange(hsv, lower_red, upper_red)
    mask3 = cv2.inRange(hsv, lower_blue, upper_blue)
    mask4 = cv2.inRange(hsv, lower_unknow, upper_unknow)
    
    kernel = np.ones((5, 5), np.uint8)
    mask1 = cv2.erode(mask1, kernel)
    mask2 = cv2.erode(mask2, kernel)
    mask3 = cv2.erode(mask3, kernel)
    mask4 = cv2.erode(mask4, kernel)
    # Contours detection
    if int(cv2.__version__[0]) > 3: 
        # Opencv 4.x.x
        contours1, _ = cv2.findContours(mask1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours2, _ = cv2.findContours(mask2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours3, _ = cv2.findContours(mask3, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours4, _ = cv2.findContours(mask4, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        
    s = "circle"

    for cnt in contours1:
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
        x = approx.ravel()[0]
        y = approx.ravel()
        print(t)
        if t > 200 and t<500:
            if area > 1500:
                cv2.drawContours(frame, [approx], 0, (0, 0, 0), 5)
                if len(approx) == 3:
                    send_string =("5")
                    # Send the string. Make sure you encode it before you send it to the Arduino.
                    ser.write(str.encode(send_string))
                    receive_string = ser.readline().decode('utf-8').rstrip()
                    # Print the data received from Arduino to the terminal
                    print(receive_string)
                    t = 0
                    break
                elif len(approx) == 4:
                    s = "Rectangle"
                    send_string =("8")
                    # Send the string. Make sure you encode it before you send it to the Arduino.
                    ser.write(str.encode(send_string))
                    receive_string = ser.readline().decode('utf-8').rstrip()
                    # Print the data received from Arduino to the terminal
                    print(receive_string)
                    t = 0
                    break
                elif  6 < len(approx) < 800:
                    s = "Circle"
                    send_string =("2")
                    # Send the string. Make sure you encode it before you send it to the Arduino.
                    ser.write(str.encode(send_string))
                    receive_string = ser.readline().decode('utf-8').rstrip()
                    # Print the data received from Arduino to the terminal
                    print(receive_string)
                    t = 0

    for cnt in contours2:
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
        x = approx.ravel()[0]
        y = approx.ravel()[1]
        print(t)
        if t > 200 and t<500:
            if area > 800:
                cv2.drawContours(frame, [approx], 0, (0, 0, 0), 5)
                if len(approx) == 3:
                    cv2.putText(frame, "Triangle", (x, y), font, 1, (0, 0, 0))
                    s = "Triangle"
                    send_string =("4")
                    # Send the string. Make sure you encode it before you send it to the Arduino.
                    ser.write(str.encode(send_string))
                    receive_string = ser.readline().decode('utf-8').rstrip()
                    # Print the data received from Arduino to the terminal
                    print(receive_string)
                    t = 0
                    break
                elif len(approx) == 4:
                    cv2.putText(frame, "Rectangle", (x, y), font, 1, (0, 0, 0))
                    s = "Rectangle"
                    send_string =("7")
                    # Send the string. Make sure you encode it before you send it to the Arduino.
                    ser.write(str.encode(send_string))
                    receive_string = ser.readline().decode('utf-8').rstrip()
                    # Print the data received from Arduino to the terminal
                    print(receive_string)
                    t = 0
                    break
                elif 6 < len(approx) < 800:
                    cv2.putText(frame, "Circle", (x, y), font, 1, (0, 0, 0))
                    s = "Circle"
                    send_string =("1")
                    # Send the string. Make sure you encode it before you send it to the Arduino.
                    ser.write(str.encode(send_string))
                    receive_string = ser.readline().decode('utf-8').rstrip()
                    # Print the data received from Arduino to the terminal
                    print(receive_string)
                    t = 0
                    break
    for cnt in contours3:
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
        x = approx.ravel()[0]
        y = approx.ravel()[1]
        print(t)
        if t > 200 and t < 500:
            if area > 800:
                cv2.drawContours(frame, [approx], 0, (0, 0, 0), 5)
                if len(approx) == 3:
                    cv2.putText(frame, "Triangle", (x, y), font, 1, (0, 0, 0))
                    s = "Triangle"
                    send_string =("6")
                    # Send the string. Make sure you encode it before you send it to the Arduino.
                    ser.write(str.encode(send_string))
                    receive_string = ser.readline().decode('utf-8').rstrip()
                    # Print the data received from Arduino to the terminal
                    print(receive_string)
                    t = 0
                    break
                elif len(approx) == 4:
                    cv2.putText(frame, "Rectangle", (x, y), font, 1, (0, 0, 0))
                    s = "Rectangle"
                    send_string =("9")
                    # Send the string. Make sure you encode it before you send it to the Arduino.
                    ser.write(str.encode(send_string))
                    receive_string = ser.readline().decode('utf-8').rstrip()
                    # Print the data received from Arduino to the terminal
                    print(receive_string)
                    t = 0
                    break
                elif 6 < len(approx) < 800:
                    cv2.putText(frame, "Circle", (x, y), font, 1, (0, 0, 0))
                    s = "Circle"
                    send_string =("3")
                    # Send the string. Make sure you encode it before you send it to the Arduino.
                    ser.write(str.encode(send_string))
                    receive_string = ser.readline().decode('utf-8').rstrip()
                    # Print the data received from Arduino to the terminal
                    print(receive_string)
                    t = 0
                    break
    for cnt in contours4:
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
        x = approx.ravel()[0]
        y = approx.ravel()[1]
        if t >600:
            if area > 800:
                cv2.drawContours(frame, [approx], 0, (0, 0, 0), 5)
                send_string =("0")
                    # Send the string. Make sure you encode it before you send it to the Arduino.
                ser.write(str.encode(send_string))
                receive_string = ser.readline().decode('utf-8').rstrip()
                    # Print the data received from Arduino to the terminal
                print(receive_string)
                t = 0
                break
    if t>1000:
        t = 0
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask1)
    cv2.imshow("Mask2", mask2)
    cv2.imshow("Mask33", mask3)
    cv2.imshow("Mask4",mask4)
    key = cv2.waitKey(1)
    if key == 27:
        break
#if s == "Circle":
#print("Circle")
#t = 0
#7t < 600



picam2.stop()
cv2.destroyAllWindows()
