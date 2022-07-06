import numpy as np
import cv2
import time
from math import sqrt

focal_length=3.67
sensor_width=4.8


webcam = cv2.VideoCapture(1)

prev_frame_time = 0
new_frame_time = 0

'''def callback(x):
	global H_low,H_high,S_low,S_high,V_low,V_high
	#assign trackbar position value to H,S,V High and low variable
	H_low = cv2.getTrackbarPos('low H','controls')
	H_high = cv2.getTrackbarPos('high H','controls')
	S_low = cv2.getTrackbarPos('low S','controls')
	S_high = cv2.getTrackbarPos('high S','controls')
	V_low = cv2.getTrackbarPos('low V','controls')
	V_high = cv2.getTrackbarPos('high V','controls')

cv2.namedWindow('controls',2)
cv2.resizeWindow("controls", 550,10);

H_low = 170
H_high = 179
S_low= 70
S_high = 255
V_low= 50
V_high = 255

cv2.createTrackbar('low H','controls',170,179,callback)
cv2.createTrackbar('high H','controls',179,179,callback)

cv2.createTrackbar('low S','controls',70,255,callback)
cv2.createTrackbar('high S','controls',255,255,callback)

cv2.createTrackbar('low V','controls',50,255,callback)
cv2.createTrackbar('high V','controls',255,255,callback)'''

sum = 0

while(1):
 
    _, imageFrame = webcam.read()


    '''lab = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2LAB)

    lab_planes = list(cv2.split(lab))

    clahe = cv2.createCLAHE(clipLimit=2.0,tileGridSize=(8,8))

    lab_planes[0] = clahe.apply(lab_planes[0])


    lab = cv2.merge(lab_planes)

    imageFrame = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)'''
    
    imageFrame = np.array(255*(imageFrame/255)**(0.4),dtype='uint8')

    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
 
    red_lower = np.array([136, 87, 111], np.uint8)
    red_upper = np.array([180, 255, 255], np.uint8)
   
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)
    kernal = np.ones((5, 5), "uint8")

    red_mask = cv2.dilate(red_mask, kernal)
    res_red = cv2.bitwise_and(imageFrame, imageFrame, 
                              mask = red_mask)

    contours, hierarchy = cv2.findContours(red_mask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    for pic, contour in enumerate(contours[:1]):
        area = cv2.contourArea(contour)
        if(area > 1000):
            x, y, w, h = cv2.boundingRect(contour)
            cx = x + w/2
            cy = y + h/2
            radius = w/2
            cv2.circle(imageFrame, (int(cx),int(cy)), int(radius), (0, 0, 255), 2)
            '''imageFrame = cv2.rectangle(imageFrame, (x, y), 
                                       (x + w, y + h), 
                                       (0, 0, 255), 2)'''
            
            '''cv2.putText(imageFrame, "Red Colour", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                        (0, 0, 255))'''

            coordinates=(int(x+w/2), int(y+h/2))
            center_point=(int(imageFrame.shape[1])//2,int(imageFrame.shape[0])//2)

            pixel_distance = sqrt((coordinates[0] - center_point[0]) ** 2 + (coordinates[1] - center_point[1]) ** 2)
            real_dist=round((500*sensor_width*pixel_distance)/(focal_length*center_point[0]*center_point[1]),2)
            #cv2.putText(imageFrame, "({}, {})".format(int(x+w/2), int(y+h/2)), (int(x+w/2), int(y+h/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            #cv2.circle(imageFrame,(x+w//2,y+h//2),5,(0,0,255),-1)
            cv2.line(imageFrame,((center_point[0]),(center_point[1])),coordinates,(0,255,0),2)
            cv2.putText(imageFrame,str(real_dist),((center_point[0]),(center_point[1])), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
    # Program Termination
    cv2.imshow("Multiple Color Detection in Real-TIme", imageFrame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break