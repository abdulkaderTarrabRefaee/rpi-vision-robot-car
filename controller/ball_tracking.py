import cv2
#import pwm_motor as motor
#import dc_motor as motor

Color_Lower = (0, 130,46)
Color_Upper = (10, 255, 255)
Frame_Width  = 320
Frame_Height = 240

camera = cv2.VideoCapture(0)
#camera.set(3,  Frame_Width)
#camera.set(4, Frame_Height)

try:
    while True:
        (_, frame) = camera.read()

        # Do gaussian blur if needed
        frame = cv2.GaussianBlur(frame, (11, 11), 0)

        # Convert to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Convert to binary with given color
        mask = cv2.inRange(hsv, Color_Lower, Color_Upper)

        # Do erode if needed
        mask = cv2.erode(mask, None, iterations=2)

        # Do dilate if needed
        mask = cv2.dilate(mask, None, iterations=2)

        # Find the contours
        contours= cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        #(contours, _) = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Define mass center
        center = None


        if len(contours) > 0:

            # Find the max length of contours
            c = max(contours, key=cv2.contourArea)

            # Find the x, y, radius of given contours
            ((x, y), radius) = cv2.minEnclosingCircle(c)

            # Find the moments
            M = cv2.moments(c)


            try:
                # mass center
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                # process every frame
                cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)

                # turn right and turn left rule
                if center[0] > 220:
                    #motor.turnRight()
                    print"turnRight"
                elif center[0] < 100  :
                    #motor.turnLeft()
                    print"turnLeft"
                else:
                    #motor.stop()
                    print"stop"

                # Forward and backward rule
                if radius > 1 and radius < 10:
                    #motor.forward()
                    print"forward"
                elif radius > 25:
                   #motor.backward()
                    print"backward"
                else:
                   #motor.stop()
                    print"stop"
                print radius




            # if not find mass center
            except:
                pass


        # mark these lines below if you don't need to display and the car will get faster
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break
        # mark these lines above if you don't need to display and the car will get faster

finally:
        #motor.cleanup()
        camera.release()
        cv2.destroyAllWindows()
