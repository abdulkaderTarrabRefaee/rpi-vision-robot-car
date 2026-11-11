import cv2
from thread import start_new_thread
import time
import numpy as np
import socket
import sys
import cv2
CV_LOAD_IMAGE_COLOR=1
def create_socket(host, port, type):
    try:
        if type == 'UDP':
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        elif type == 'TCP':
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            return None
        return sock
    except:
        print("Could not create socket.")
        sys.exit(0)

def bind_socket(socket, host, port):

        socket.bind((host, port))
        print("[-] Socket Bound to port " + str(port))


def client_thread_cam(s, host, port, cap):
    while True:
        ret, frame = cap.read()
        if(ret==False):
            print 'Nie wykryto kamery, zamykam watek'
            cap.release()
            s.close()
            print "[-] Socket on port " + str(port) + " closed"
            break
        else:
            cv2.imshow('frame'+str(port),frame)
            ret, buff = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 75])
            data = np.array(buff)
            stringData = data.tostring()

            count = 0
            while count < len(stringData):
                if count+65565  > len(stringData):
                    s.sendto(stringData[count:], (host, port))
                else:
                    s.sendto(stringData[count:count+65565], (host, port))
                count += 65565

            if cv2.waitKey(1) & 0xFF == ord('q'):
                s.close()
                cap.release()
                cv2.destroyWindow('frame'+str(port))
                print "[-] Socket on port " + str(port) + " closed"
                break


#----------------------


HOST = '0.0.0.0'
destHOST = 'Drz'
PORT = 11001
PORT2 = 11002

#HOST = raw_input("Podaj swoj adres ip")
#destHOST = raw_input("Podaj adres ip serwera")
cap = cv2.VideoCapture(0)
#cap.set(3,320)
#cap.set(4,240)
#time.sleep(5)
s1 = create_socket(HOST, PORT, 'UDP')
bind_socket(s1, HOST, PORT)
client_thread_cam(s1, destHOST, PORT, cap)



while True:
    pass
