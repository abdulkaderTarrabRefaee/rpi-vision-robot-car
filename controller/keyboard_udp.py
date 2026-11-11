import socket
import sys
import pygame
import cv2
import urllib
import thread
import numpy as np
import socket
import time
server_name = socket.gethostname()
server_port = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((server_name, server_port))

print 'Server is ready...'
5
message, client_address = server_socket.recvfrom(2048)





global y
y = None

#bar = pygame.image.load('bar.png')
pygame.init()
display_width = 320
display_height = 240
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Raspberry Racecar')
clock = pygame.time.Clock()
screen = pygame.display.get_surface()



message = ""
while True:
        for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                        continue

                if event.type == pygame.KEYUP:
                        message = "Center"

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
                        '''
                        elif event.key == 97:
                                message = "Cam Up"
                        elif event.key == 100:
                                message = "Cam Down"
                        '''
                if message:
                        #print message

                        server_socket.sendto(message, client_address)
                        message = ""

                if event.type == pygame.QUIT:
                        sock.close()
                        pygame.quit()
                        quit()
                        sys.exit()

        #if camImage == None:
                #continue
        #screen.blit(cvimageToPygame(y), (0,0))
        #screen.blit(bar,(0,480))
        pygame.display.flip()
        pygame.display.update()
        clock.tick(60)

