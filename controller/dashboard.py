import pygame
import time
import random

from thread import start_new_thread
import numpy as np
import socket
import sys
import cv2
import pygame
import urllib
import thread
pygame.init()

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))


pygame.display.set_caption('car')

#icon = pygame.image.load("bar.png")
#pygame.display.set_icon(icon)

white = (255,255,255)
black = (0,0,0)


red = (200,0,0)
light_red = (255,0,0)

yellow = (200,200,0)
light_yellow = (255,255,0)

green = (34,177,76)
light_green = (0,255,0)

clock = pygame.time.Clock()




tankWidth = 40
tankHeight = 20

turretWidth = 5
wheelWidth = 5





smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 85)

#img = pygame.image.load('bar.png')
#appleimg = pygame.image.load('apple.png')


#---------------------------------
#---------------------------------
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

def cvimageToPygame(image):
	"""Convert cvimage into a pygame image"""
	return pygame.image.frombuffer(image.tostring(), image.shape[1::-1], "RGB")


def server_thread_cam(socket, client_count):
    global img_decoded
    global img_decoded1
    img_to_read = ''
    img_to_show = ''

    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyWindow('cam no ' + str(client_count))
            socket.close()
            print "Thread for camera no. "+str(client_count)+" finished"
            break

        while True:   # oczekujemy na obraz
            strng, addr = socket.recvfrom(65565)
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
        img_decoded1 = cv2.imdecode(np.fromstring(img_to_show, dtype=np.uint8), cv2.CV_LOAD_IMAGE_COLOR)
        img_decoded = cv2.cvtColor(img_decoded1, cv2.COLOR_BGR2RGB)


        #if img_decoded != None:
        #cv2.imshow('cam no ' + str(client_count), img_decoded)
        #else:
            #break

#--------------------------
CV_LOAD_IMAGE_COLOR=1
HOST = socket.gethostname()
print HOST
PORT = 11001
PORT2=5000
client_count = 0

#HOST = raw_input("Podaj swoj adres ip")


#----------------------------
def main():



    global img_decoded
    img_decoded = None

    bar = pygame.image.load('bar.png')
    pygame.init()
    display_width = 800
    display_height = 600
    gameDisplay = pygame.display.set_mode((display_width,display_height))
    pygame.display.set_caption('Raspberry Racecar')
    clock = pygame.time.Clock()
    screen = pygame.display.get_surface()

    thread.start_new_thread(server_thread_cam,(s1, client_count))

    message = ""
    while True:
        for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                        continue

                if event.type == pygame.KEYUP:
                        message = ""

                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                                message = "2"
                                print "Left"
                        elif event.key == pygame.K_RIGHT:
                                message = "1"
                                print "Right"
                        elif event.key == pygame.K_UP:
                                message = "4"
                                print "Up"
                        elif event.key == pygame.K_DOWN:
                                message = "3"
                                print "Down"
                        elif event.key == pygame.K_SPACE:
                                message = "5"
                                print "Stop"
                        elif event.key == pygame.K_w:
                                message = "7"
                                print "Cam_UP"

                        elif event.key == pygame.K_s:
                                message = "6"
                                print "Cam_Down"
                if message:
                    #print message

                    server_socket.sendto(message, client_address)
                    message = ""

        #if img_decoded == None:
                #continue
        #button("play", 150,500,100,50, green, light_green, action="play")
        button("Main", 675,150,100,50, red , light_red, action="main")
        button("quit", 675,250,100,50, red, light_red, action ="quit")



        pygame.display.update()

        clock.tick(15)
        screen.blit(cvimageToPygame(img_decoded), (0,0))
        screen.blit(bar,(0,480))
        pygame.display.flip()
        pygame.display.update()
        #clock.tick(5000)
def main2():



    global img_decoded
    global img_decoded1
    img_decoded = None

    bar = pygame.image.load('bar.png')
    pygame.init()
    display_width = 800
    display_height = 600
    gameDisplay = pygame.display.set_mode((display_width,display_height))
    pygame.display.set_caption('Raspberry Racecar')
    clock = pygame.time.Clock()
    screen = pygame.display.get_surface()

    thread.start_new_thread(server_thread_cam,(s1, client_count))

    message = ""
    take=0
    while True:
        for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                        continue

                if event.type == pygame.KEYUP:
                        message = ""

                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                                message = "2"
                                print "Left"
                        elif event.key == pygame.K_RIGHT:
                                message = "1"
                                print "Right"
                        elif event.key == pygame.K_UP:
                                message = "4"
                                print "Up"
                        elif event.key == pygame.K_DOWN:
                                message = "3"
                                print "Down"
                        elif event.key == pygame.K_SPACE:
                                message = "5"
                                print "Stop"
                        elif event.key == pygame.K_w:
                                message = "7"
                                print "Cam_UP"

                        elif event.key == pygame.K_s:
                                message = "6"
                                print "Cam_Down"
                        elif event.key == pygame.K_c:
                                print "Cam_take"
                                cv2.imwrite(str(take)+' cam+.png',img_decoded1)
                                take=take+1

                if message:
                    #print message

                    server_socket.sendto(message, client_address)
                    message = ""


        #if img_decoded == None:
                #continue
        #button("play", 150,500,100,50, green, light_green, action="play")
        button("Main", 675,150,100,50, red , light_red, action="main")
        button("quit", 675,250,100,50, red, light_red, action ="quit")



        pygame.display.update()

        clock.tick(15)

        screen.blit(cvimageToPygame(img_decoded), (0,0))
        screen.blit(bar,(0,480))
        pygame.display.flip()
        pygame.display.update()
        #clock.tick(5000)








#---------------------------------
#---------------------------------

def score(score):

    text = smallfont.render("Score: "+str(score), True, black)
    gameDisplay.blit(text, [0,0])


def text_objects(text, color,size = "small"):

    if size == "small":
        textSurface = smallfont.render(text, True, color)
    if size == "medium":
        textSurface = medfont.render(text, True, color)
    if size == "large":
        textSurface = largefont.render(text, True, color)

    return textSurface, textSurface.get_rect()

def text_to_button(msg, color, buttonx, buttony, buttonwidth, buttonheight, size = "small"):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = ((buttonx+(buttonwidth/2)), buttony+(buttonheight/2))
    gameDisplay.blit(textSurf, textRect)

def message_to_screen(msg,color, y_displace = 0, size = "small"):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = (int(display_width / 2), int(display_height / 2)+y_displace)
    gameDisplay.blit(textSurf, textRect)


def game_controls():


    gcont = True

    while gcont:
        for event in pygame.event.get():
                #print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()


        gameDisplay.fill(white)
        message_to_screen("Controls",green,-100,size="large")
        message_to_screen("Move Car: Up and Down arrows",black,10)
        message_to_screen("Move Car: Left and Right arrows",black,60)
        message_to_screen("Move Camera: W and S arrows",black,100)
        message_to_screen("Stop: Space",black,140)


        button("play", 150,500,100,50, green, light_green, action="play")
        button("Main", 350,500,100,50, yellow, light_yellow, action="main")
        button("quit", 550,500,100,50, red, light_red, action ="quit")



        pygame.display.update()

        clock.tick(15)


def button(text, x, y, width, height, inactive_color, active_color, action = None):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #print(click)
    if x + width > cur[0] > x and y + height > cur[1] > y:
        pygame.draw.rect(gameDisplay, active_color, (x,y,width,height))
        if click[0] == 1 and action != None:
            if action == "quit":
                pygame.quit()
                quit()

            if action == "controls":
                game_controls()

            if action == "play":
                main()

            if action == "main":
                game_intro()
            if action == "play2":
                main2()
            if action == "con":
                connect()


    else:
        pygame.draw.rect(gameDisplay, inactive_color, (x,y,width,height))

    text_to_button(text,black,x,y,width,height)





def connect ():
    global s1
    global  server_socket
    global  client_address
    global message
    s1 = create_socket(HOST, PORT, 'UDP')
    bind_socket(s1, HOST, PORT)
    print 'Server1 is ready...'

    server_socket = create_socket(HOST, PORT2, 'UDP')
    bind_socket(server_socket, HOST, PORT2)
    print 'Starting new UDP thread'
    #server_thread_cam(s1, client_count)
    #client_count += 1

    print 'Server2 is ready...'
    message, client_address = server_socket.recvfrom(2048)
    print 'Server3 is ready...'
    game_intro()


def game_intro():

    intro = True



    while intro:
        for event in pygame.event.get():
                #print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        intro = False
                        connect ()
                    elif event.key == pygame.K_q:

                        pygame.quit()
                        quit()

        gameDisplay.fill(white)
        message_to_screen("Welcome to Car Robot!",green,-100,size="medium")
        #message_to_screen("The objective is to shoot and destroy",black,-30)
        #message_to_screen("the enemy tank before they destroy you.",black,10)
       # message_to_screen("The more enemies you destroy, the harder they get.",black,50)
        #message_to_screen("Press C to play, P to pause or Q to quit",black,180)


        #button("play", 150,500,100,50, green, light_green, action="play")
        button("play2", 150,500,100,50, green, light_green, action="play2")
        button("controls", 350,500,100,50, yellow, light_yellow, action="controls")
        button("con", 250,500,100,50, yellow, light_yellow, action="con")
        button("quit", 550,500,100,50, red, light_red, action ="quit")



        pygame.display.update()

        clock.tick(15)




game_intro()

