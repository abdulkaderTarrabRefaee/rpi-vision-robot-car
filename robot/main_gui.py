#---------------------------------------------
#	        import library
#---------------------------------------------
from Tkinter import *
import cv2
import numpy as np
import RPi.GPIO as GPIO
import time
#---------------------------------------------
#		gpio setup
#---------------------------------------------
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(3,GPIO.OUT)
GPIO.setup(5,GPIO.OUT)
GPIO.setup(7,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(8,GPIO.OUT)
GPIO.setup(10,GPIO.OUT)
GPIO.setup(16,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
p = GPIO.PWM(13, 50)
p.start(9)
#---------------------------------------------
#		function for servo
#---------------------------------------------

def servo_top():
y=9
p.ChangeDutyCycle(y)
while y>=6:
    time.sleep(0.1)
    y=y-0.2
    print y
    p.ChangeDutyCycle(y)
return y

def servo_down():
y=6
p.ChangeDutyCycle(y)
while y<=9:
    time.sleep(0.1)
    y=y+0.2
    print y
    p.ChangeDutyCycle(y)
return y




    if(1<x<60):
        y=4

        while y!=7:
            time.sleep(0.5)
            y=y+0.5
            p.ChangeDutyCycle(y)


    if(60<x<120):
        y=7
        while y!=9:
            time.sleep(0.5)
            y=y+0.5
            p.ChangeDutyCycle(y)

    if(120<x<180):
        y=9
        while y!=7:
            time.sleep(0.5)
            y=y+0.5
            p.ChangeDutyCycle(y)
    if(180<x<240):
        y=10
        while y!=11:
            time.sleep(0.5)
            y=y+0.5
            p.ChangeDutyCycle(y)


    #x1=float(x)
    #time.sleep(0.8)
    #y=(73*x1+9927)/2500
    #y = abs( y -11)
    #print y




#---------------------------------------------
#		function for move
#---------------------------------------------
def Backward():

 # Motor 1
 GPIO.output(5, True)
 GPIO.output(3, False)
 # Motor 2
 GPIO.output(7, True)
 GPIO.output(11, False)

 # Motor 3
 GPIO.output(8, False)
 GPIO.output(10, True)

 # Motor 4
 GPIO.output(16, False)
 GPIO.output(18, True)


def stop():

    # Motor 1
    GPIO.output(3,0)
    GPIO.output(5,0)
    # Motor 2
    GPIO.output(7,0)
    GPIO.output(11,0)
    # Motor 3
    GPIO.output(8,0)
    GPIO.output(10,0)
    # Motor 4
    GPIO.output(16,0)
    GPIO.output(18,0)



def forward():

    # Motor 1
    GPIO.output(3,1)
    GPIO.output(5,0)
    # Motor 2
    GPIO.output(7,0)
    GPIO.output(11,1)
    # Motor 3
    GPIO.output(8,1)
    GPIO.output(10,0)
    # Motor 4
    GPIO.output(16,1)
    GPIO.output(18,0)



def Left():

 # Motor 1
 GPIO.output(5,False )
 GPIO.output(3, True)
 # Motor 2
 GPIO.output(7, True)
 GPIO.output(11, False)

 # Motor 3
 GPIO.output(8, True)
 GPIO.output(10, False)

 # Motor 4
 GPIO.output(16, False)
 GPIO.output(18, True)
 time.sleep(0.7)
 stop()




def Right():

 # Motor 1
 GPIO.output(5, True)
 GPIO.output(3, False)
 # Motor 2
 GPIO.output(7, False)
 GPIO.output(11, True)

 # Motor 3
 GPIO.output(8, False)
 GPIO.output(10, True)

 # Motor 4
 GPIO.output(16, True)
 GPIO.output(18, False)
 time.sleep(0.7)
 stop()
#---------------------------------------------
#		some variable
#---------------------------------------------
center_x = 160
center_y = 125

width = 320
height = 250

#------------------------------------------------------
#	function : main program for traffic_light
#------------------------------------------------------
def traffic_light():
    cap = cv2.VideoCapture(0)
    #capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, width)
    #capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, hight)
    cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,width)
    cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,height)
    coloris = "NONE"
    kernel = np.ones((10,10),np.uint8)
    while(1):
        _, frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_G = np.array([50,100,100])
        upper_G = np.array([100,255,255])
        mask1 = cv2.inRange(hsv, lower_G, upper_G)
        lower_R = np.array([0,100,100])
        upper_R = np.array([20,255,255])
        mask2 =  cv2.inRange(hsv, lower_R, upper_R)
        if mask1.mean() >= 10:
            if mask1.mean() > mask2.mean():
                coloris ="GREEN"
                forward()  #RUN ALL MOTOR
        if mask2.mean() >= 10:
            if mask2.mean() > mask1.mean():
                coloris ="RED"
                stop()   #STOP ALL MOTOR
        if mask1.mean() <10 and mask2.mean() <10:
            coloris = "NO COLOR"
            forward()
            time.sleep(1)
            stop()   #STOP ALL MOTOR

        print coloris
        mask = mask1 + mask2
        res = cv2.bitwise_and(frame,frame, mask= mask)
        res = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

        cnts, hierarchy = cv2.findContours(res.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        #cv2.circle(frame,(center_x,center_y), 5, (0,0,255), -1)
        for c in cnts:
            if cv2.contourArea(c) > 10:
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow('frame',frame)
        cv2.imshow('mask',mask)
        cv2.imshow('res',res)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            gpio.cleanup()
            break
    cv2.destroyAllWindows()
#------------------------------------------------------
#	function : main program for ogject_tracking
#------------------------------------------------------
def ogject_tracking():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, height)
    lower_G = np.array([50,100,100])
    upper_G = np.array([105,255,255])
    lower_R = np.array([0,100,100])
    upper_R = np.array([20,255,255])
    while(1):
        _, frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask1 = cv2.inRange(hsv, lower_G, upper_G)
        mask2 =  cv2.inRange(hsv, lower_R, upper_R)
        mask = mask1 + mask2
        res = cv2.bitwise_and(frame,frame, mask= mask)
        res = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        cnts, hierarchy = cv2.findContours(res.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cv2.circle(frame,(center_x,center_y), 5, (0,0,255), -1)
        for c in cnts:
            if cv2.contourArea(c) >200:
                m = cv2.moments(c)
                area = m['m00']
                cx = int(m['m10']/m['m00'])
                cy = int(m['m01']/m['m00'])

                cv2.circle(frame,(cx,cy), 5, (255,0,0), -1)

                if cy>140 and is_top:
                    servo_top



                if cx< 40:
                    print 'left'
                    time.sleep(0.09)
                    Left()

                elif cx > 80:
                    print 'right'
                    time.sleep(0.09)
                    Right()
                else:
                    print 'center'
                if area < 550:
                    print 'ForWard'
                    forward()
                    time.sleep(0.1)
                    stop()
                elif area > 2000:
                    print 'BackWard'
                    Backward()
                    time.sleep(0.1)
                    stop()
                else:
                    print 'Stop'
                    stop()
                print area
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow('frame',frame)
        cv2.imshow('res',res)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            stop()
            GPIO.cleanup()
            break
    cv2.destroyAllWindows()
#------------------------------------------------------
#	function : main program for object_tracking2
#------------------------------------------------------
def object_tracking2():
    cap = cv2.VideoCapture(0)
    fgbg = cv2.createBackgroundSubtractorKNN(detectShadows = True)

    while(1):
        ret, frame = cap.read()
        cv2.circle(frame,(325,250), 5, (0,0,255), -1)
        fgmask = fgbg.apply(frame)
        th = cv2.threshold(fgmask.copy(), 244, 255, cv2.THRESH_BINARY)[1]
        dilated = cv2.dilate(th, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)), iterations = 2)
        image, contours, hier = cv2.findContours(dilated, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            if cv2.contourArea(c) > 300:
                m = cv2.moments(c)
                cx = int(m['m10']/m['m00'])
                cy = int(m['m01']/m['m00'])
                if cx > 325:
                    print "RIGHT"
                    Right()
                else:
                    print "LEFT"
                    Left()
                (x,y,w,h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 255, 0), 2)
        cv2.imshow('frame',frame)
        cv2.imshow('fgmask',fgmask)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
#------------------------------------------------------
#           main program for GUI
#------------------------------------------------------
fen1 = Tk()
lb1 = Label(fen1,text = 'SELECT PROJECT').grid(row =1,column =2)
lb2 = Label(fen1,text = '---------------------------').grid(row =2,column =2)
bou1 = Button(fen1,text='Trafic Light',command=traffic_light).grid(row =3, column =1,padx =10, pady =5)
bou2 = Button(fen1,text='Object Tracking',command=ogject_tracking).grid(row =3, column =2,padx =10, pady =5)
bou3 = Button(fen1,text='Object Tracking2',command=object_tracking2).grid(row =3, column =3,padx =10, pady =5)
lb3 = Label(fen1,text = 'SELECT DIRECTION').grid(row =4,column =2)
lb4 = Label(fen1,text = '---------------------------').grid(row =5,column =2)
bou4 = Button(fen1,text='FOR WARD',command=forward).grid(row =6, column =2,padx =10, pady =5)
bou5 = Button(fen1,text='LEFT',command=Left).grid(row =7, column =1,padx =10, pady =5,sticky =E)
bou6 = Button(fen1,text='STOP',command=stop).grid(row =7, column =2,padx =10, pady =5)
bou7 = Button(fen1,text='RIGHT',command=Right).grid(row =7, column =3,padx =10, pady =5,sticky =W)
bou8 = Button(fen1,text='BACK WARD',command=Backward).grid(row =8, column =2,padx =10, pady =5)
lb4 = Label(fen1,text = '---------------------------').grid(row =9,column =2)
bou1 = Button(fen1,text='Exit',command=fen1.destroy).grid(row =10,column =2,padx =10, pady =5)
fen1.mainloop()








