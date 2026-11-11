import numpy as np
import socket
import sys
import cv2
import argparse
import imutils
CV_LOAD_IMAGE_COLOR=1
def connect():
    server_name = socket.gethostname()
    server_port = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((server_name, server_port))

    print 'Server is ready...'

    message, client_address = server_socket.recvfrom(2048)

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

def server_thread_cam(socket, client_count):
    img_to_read = ''
    img_to_show = ''

    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyWindow('cam no ' + str(client_count))
            socket.close()
            print "Thread for camera no. "+str(client_count)+" finished"
            break

        while True:   # oczekujemy na obraz
            strng, addr = socket.recvfrom(132128)
            if len(strng) == 0:  # nie otrzymalismy wiadomosci
                if img_to_read != '':
                    img_to_show = img_to_read
                    img_to_read = ''
                break

            if (len(strng) < 65565) and (len(strng) > 0):
                # ostatnia czesc wiadomosci
                img_to_read += strng
                img_to_show = img_to_read
                img_to_read = '' # obraz zapisany, wychodzimy z petli
                break

            img_to_read += strng
        cv2.CV_LOAD_IMAGE_COLOR = 1

        frame = cv2.imdecode(np.fromstring(img_to_show, dtype=np.uint8), cv2.CV_LOAD_IMAGE_COLOR)
        #cv2.imshow('cam no ' + str(client_count), frame)
        #if img_decoded != None:

        ap = argparse.ArgumentParser()
        ap.add_argument("-v", "--video",
                help="path to the (optional) video file")
        ap.add_argument("-b", "--buffer", type=int, default=128,
                help="max buffer size")
        args = vars(ap.parse_args())
        frame = imutils.resize(frame, width=600)

        cascade_path = "fist.xml"
        cascade = cv2.CascadeClassifier(cascade_path)
        color = (255, 255, 255)

        minsize = 100





        image_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rect = cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=1, minSize=(minsize,minsize))

        if len(rect) > 0:
            for handRect in rect:
                x=handRect[0]
                y=handRect[1]
                cv2.rectangle(frame, tuple((handRect[0],handRect[1])),tuple((handRect[0]+handRect[2],handRect[1]+handRect[2])), color, thickness=2)
                print x,y
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



        cv2.imshow("Frame", frame)

        cv2.waitKey(1)
    #else:
        #break
