
import socket
import RPi.GPIO as GPIO
import time
#--------------------------
server_name = '192.168.1.101'
server_port = 5000

so = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
so.sendto("connect", (server_name, server_port))
#--------------------------

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


def Backward():

 # Motor 1
 GPIO.output(5, 1)
 GPIO.output(3, 0)
 # Motor 2
 GPIO.output(7, 1)
 GPIO.output(11, 0)

 # Motor 3
 GPIO.output(8, 0)
 GPIO.output(10, 1)

 # Motor 4
 GPIO.output(16, 0)
 GPIO.output(18, 1)



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

while True:

    recv, ads = so.recvfrom(2048)

    if recv=='1':
        print recv
        Right()

    if recv=='2':
        print recv

        Left()
    if recv=='3':
        print recv
        Backward()

    if recv=='4':
        print recv
        forward()


    if recv=='5':
        print recv
        stop()










print 'Received: ', receved_message
time.sleep(.5)





