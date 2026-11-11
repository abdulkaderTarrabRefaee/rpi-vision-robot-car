import socket
import RPi.GPIO as GPIO
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



s = socket.socket()
host = '192.168.43.14'
port = 5000
s.connect((host, port))
print host
# Get data from server
while True:
    print s.recv(4096)
    if s.recv(4096)=='Right':
        print '1'
        Right()
    if s.recv(4096)=='left':
        print '2'
        Left()
    if s.recv(4096)=='forward':
        print '3'
        forward()
    if s.recv(4096)=='backward':
        print '4'
        Backward()
s.close

