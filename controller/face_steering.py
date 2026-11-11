import cv2

import socket
server_name = socket.gethostname()
server_port = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((server_name, server_port))

print 'Server is ready...'

message, client_address = server_socket.recvfrom(2048)

print 'Server is ready...'
print message
last=message
cascade_path = "face.xml"
cascade = cv2.CascadeClassifier(cascade_path)
color = (255, 255, 255)
cap = cv2.VideoCapture(0)
#cap.set(3,800)
#cap.set(4,600)

minsize = 100

def display(frame):
    cv2.imshow("frame",frame)

while True:
    ret,frame = cap.read()
    image_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rect = cascade.detectMultiScale(image_gray, scaleFactor=1.5, minNeighbors=2, minSize=(minsize,minsize))

    if len(rect) > 0:
        st=0
        for handRect in rect:
            x=handRect[0]
            y=handRect[1]
            cv2.rectangle(frame, tuple((handRect[0],handRect[1])),tuple((handRect[0]+handRect[2],handRect[1]+handRect[2])), color, thickness=2)
#------------------------------
        if x <150 and (y >100 and y<280 ):
            print("Right")

            if(last !='2'):
                server_socket.sendto('2', client_address)
                message, client_address = server_socket.recvfrom(2048)
            last=message

        elif x>200 and x<280 and (y >100 and y<280 ) :
            print("stop")
            if(last !='5'):
                server_socket.sendto('5', client_address)
                message, client_address = server_socket.recvfrom(2048)
            last=message


        elif x>320 and (y >100 and y<280 ):
            print("left")
            if(last !='1'):
                server_socket.sendto('1', client_address)

                message, client_address = server_socket.recvfrom(2048)
            last=message

        if y<100 and (x<320 or x>150)  :
            print("top")
            if(last !='4'):
                server_socket.sendto('4', client_address)
                message, client_address = server_socket.recvfrom(2048)
            last=message



        if y >280 and (x<320 or x>150) :
            print("butom")
            if(last !='3'):
                server_socket.sendto('3', client_address)

                message, client_address = server_socket.recvfrom(2048)
            last=message


#------------------------------

    display(frame)

    cv2.waitKey(1)
