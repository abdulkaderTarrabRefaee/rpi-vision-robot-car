#!/usr/bin/python

import os
import pygame           # Imports pygame library that are made for developing games
import socket
import time
#--------------------------------



import socket
import time

server_name = socket.gethostname()
server_port = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((server_name, server_port))

print 'Server is ready...'
5
message, client_address = server_socket.recvfrom(2048)

print 'Saaaaady...'

#--------------------------------

pygame.init()                   # Starts pygame
t = pygame.time.Clock()         # Make a tracker

os.system('cls' if os.name=='nt' else 'clear')# Clear terminal // remove "there is no soundcard"
try:

        print "Number of Devices:", pygame.joystick.get_count()
        d = pygame.joystick.Joystick(0)
        d.init()                        # Start pygame.joystick.Joystick(0)

# Gives info about the device
        print "Connected device", d.get_name()
        print d.get_name(), "have"
        print "Buttons:", d.get_numbuttons()
        print "Axes:", d.get_numaxes()
        print "Hats:", d.get_numhats()
        print "Balls:", d.get_numballs()
        print "The device ID is", d.get_id()
        print "Press button 0 to exit"

# Start showing the info in terminal
        def loop(client_address):
                global d, t
                while pygame.event.get(pygame.QUIT) == []:

                        xy =pygame.event.get(pygame.JOYAXISMOTION) # call the infomation to
                # Axes Part
                        if xy != []:
                                xy_data = []

                                for c in range(0, d.get_numaxes()):
                                        xy_data+= [str(round(d.get_axis(c),1))]
                                        print d.get_axis(c)

                                if xy_data[0] == '1.0':
                                        print "Right"
                                        server_socket.sendto('1', client_address)
                                        #time.sleep(0.1)

                                elif xy_data[0] == '-1.0':
                                        print "left"
                                        server_socket.sendto('2', client_address)
                                        #time.sleep(0.1)

                                elif xy_data[1] == '1.0':
                                        server_socket.sendto('3', client_address)
                                        #time.sleep(0.1)
                                        print "top"

                                        print xy_data[1]
                                elif xy_data[1] == '-1.0':
                                        server_socket.sendto('4', client_address)
                                        #time.sleep(0.1)
                                        print "Butn"


                                        print xy_data[1]


                        # Button Part Down
                        downbutton = pygame.event.get(pygame.JOYBUTTONDOWN)
                        for button in downbutton:
                                print "Pressed button is", button.button
                                x=str(button.button)
                                if(x=='2'):

                                        server_socket.sendto('5', client_address)
                                if(x=='5'):

                                        server_socket.sendto('7', client_address)
                                if(x=='7'):

                                        server_socket.sendto('6', client_address)

                # Button Part Up
                        upbutton = pygame.event.get(pygame.JOYBUTTONUP)
                        for button in upbutton:
                                print "Button released was", button.button
                        t.tick(80)
        loop(client_address)

except:
        print "No device found"
        print "Please insert device and try agian"
        print "Shutting down now"

#Nicklas Jensen


