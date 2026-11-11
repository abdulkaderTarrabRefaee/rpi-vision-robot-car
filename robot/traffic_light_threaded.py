#---------------------------------------------
#	        import library
#---------------------------------------------
from Tkinter import *
import cv2
import numpy as np
import RPi.GPIO as GPIO
import threading
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
#---------------------------------------------
#		function for move
#---------------------------------------------
def backward():
 print "Backward"
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
    print "stop"
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
    print "forward"
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



def left():
 print "Left"
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



def wright():
 print "Right"
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
#---------------------------------------------
#		some variable
#---------------------------------------------
center_x = 170
center_y = 150

width = 160
height = 120
#------------------------------------------------------
#	class : main program for traffic_light
#------------------------------------------------------

class tfl(threading.Thread):
   def __init__(self):
         threading.Thread.__init__(self)
   def run(self):
        cap = cv2.VideoCapture(0)

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


        coloris = "NONE"
        kernel = np.ones((10,10),np.uint8)
        while(1):
            _, frame = cap.read()
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            lower_G = np.array([75,50,50])
            upper_G = np.array([105,255,255])
            mask1 = cv2.inRange(hsv, lower_G, upper_G)
            lower_R = np.array([-10,50,50])
            upper_R = np.array([10,255,255])
            mask2 =  cv2.inRange(hsv, lower_R, upper_R)
            if mask1.mean() >= 10:
                if mask1.mean() > mask2.mean():
                    coloris ="GREEN"
                    #Forward()  #RUN ALL MOTOR
            if mask2.mean() >= 10:
                if mask2.mean() > mask1.mean():
                    coloris ="RED"
                    S#top()   #STOP ALL MOTOR
            if mask1.mean() <10 and mask2.mean() <10:
                coloris = "NO COLOR"
                #Forward()   #RUN ALL MOTOR
            print coloris
            mask = mask1 + mask2
            res = cv2.bitwise_and(frame,frame, mask= mask)
            res = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
            image, cnts, hierarchy = cv2.findContours(res.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            cv2.circle(frame,(center_x,center_y), 5, (0,0,255), -1)
            for c in cnts:
                if cv2.contourArea(c) > 100:
                    (x, y, w, h) = cv2.boundingRect(c)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.imshow('frame',frame)
            cv2.imshow('mask',mask)
            cv2.imshow('res',res)
            k = cv2.waitKey(5) & 0xFF
            if k == 27:
                #gpio.cleanup()
                break
        cv2.destroyAllWindows()
#------------------------------------------------------
#	function : main program for traffic_light
#------------------------------------------------------
def traffic_light():
    global tfl
    tfl = tfl()
    tfl.start()
#------------------------------------------------------
#	class : main program for show_frame
#------------------------------------------------------
class shf(threading.Thread):
    def __init__(self):
         threading.Thread.__init__(self)
    def run(self):
        cap = cv2.VideoCapture(0)
        cap.set(3, width)
        cap.set(4, height)
        while(1):
            _, frame = cap.read()
            cv2.imshow('frame',frame)
            k = cv2.waitKey(5) & 0xFF
            if k == 27:
                break
                threading.Thread._Thread__delete
        print 'end run'

#------------------------------------------------------
#	function : main program for show_frame
#------------------------------------------------------
def show_frame():
    global shf
    shf = shf()
    shf.start()


#------------------------------------------------------
#	class : main program for object_tracking
#------------------------------------------------------
class obt(threading.Thread):
   def __init__(self):
         threading.Thread.__init__(self)
   def run(self):
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        lower_G = np.array([75,50,50])
        upper_G = np.array([105,255,255])
        lower_R = np.array([-10,50,50])
        upper_R = np.array([10,255,255])
        while(1):
            _, frame = cap.read()
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask1 = cv2.inRange(hsv, lower_G, upper_G)
            mask2 =  cv2.inRange(hsv, lower_R, upper_R)
            mask = mask1 + mask2
            res = cv2.bitwise_and(frame,frame, mask= mask)
            res = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
            image, cnts, hierarchy = cv2.findContours(res.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            cv2.circle(frame,(center_x,center_y), 5, (0,0,255), -1)
            for c in cnts:
                if cv2.contourArea(c) >200:
                    m = cv2.moments(c)
                    area = m['m00']
                    cx = int(m['m10']/m['m00'])
                    cy = int(m['m01']/m['m00'])
                    cv2.circle(frame,(cx,cy), 5, (255,0,0), -1)
                    if cx< 100:
                        print 'left'
                        #Left()
                    elif cx > 240:
                        print 'right'
                    else:
                        print 'center'
                        #Right()
                    if area < 8000:
                        print 'ForWard'
                    elif area > 15000:
                        print 'BackWard'
                    else:
                        print 'Stop'
                    (x, y, w, h) = cv2.boundingRect(c)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.imshow('frame',frame)
            cv2.imshow('res',res)
            k = cv2.waitKey(5) & 0xFF
            if k == 27:
                #gpio.cleanup()
                break
        cv2.destroyAllWindows()
#------------------------------------------------------
#	function : main program for object_tracking
#------------------------------------------------------
def ogject_tracking():
    global obt
    obt = obt()
    obt.start()

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
                else:
                    print "LEFT"
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
#            class : main program for GUI
#------------------------------------------------------
class widget(threading.Thread):
   def __init__(self):
         threading.Thread.__init__(self)
   def run(self):
        fen1 = Tk()
        lb1 = Label(fen1,text = 'SELECT PROJECT').grid(row =1,column =2)
        lb2 = Label(fen1,text = '---------------------------').grid(row =2,column =2)
        bou1 = Button(fen1,text='Trafic Light',command=traffic_light).grid(row =3, column =1,padx =10, pady =5)
        bou2 = Button(fen1,text='Object Tracking',command=ogject_tracking).grid(row =3, column =2,padx =10, pady =5)
        bou3 = Button(fen1,text='Show Frame',command=show_frame).grid(row =3, column =3,padx =10, pady =5)
        lb3 = Label(fen1,text = 'SELECT DIRECTION').grid(row =4,column =2)
        lb4 = Label(fen1,text = '---------------------------').grid(row =5,column =2)
        bou4 = Button(fen1,text='FOR WARD',command =forward).grid(row =6, column =2,padx =10, pady =5)
        bou5 = Button(fen1,text='LEFT' , command = left).grid(row =7, column =1,padx =10, pady =5,sticky =E)
        bou6 = Button(fen1,text='STOP',command =stop).grid(row =7, column =2,padx =10, pady =5)
        bou7 = Button(fen1,text='RIGHT',command =wright).grid(row =7, column =3,padx =10, pady =5,sticky =W)
        bou8 = Button(fen1,text='BACK WARD',command =backward).grid(row =8, column =2,padx =10, pady =5)
        lb4 = Label(fen1,text = '---------------------------').grid(row =9,column =2)
        bou1 = Button(fen1,text='Exit',command=fen1.destroy).grid(row =10,column =2,padx =10, pady =5)
        fen1.mainloop()
#------------------------------------------------------
#             main program
#------------------------------------------------------
widget = widget()
widget.start()





