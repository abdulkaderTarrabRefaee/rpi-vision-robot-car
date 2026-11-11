# Raspberry Pi vision robot car (2016 – 2017)

University project from my Electrical & Electronic Engineering degree: a four-motor robot car driven by a Raspberry Pi 3, with a pan camera, live video over UDP and several OpenCV control modes. Archived here as it was written at the time.

> **Archive notice.** This is student code from 2016 – 2017, written for Python 2.7 and OpenCV 2.4 / 3.x. It is published unchanged apart from file names and line endings. It is not maintained and is not how I write Python today.

## What it does

| Mode | Where it runs | How |
|---|---|---|
| Manual drive | PC → Pi | Keyboard or USB joystick sends one-byte commands over UDP |
| Live dashboard | PC | pygame window shows the Pi camera stream and sends drive and camera-tilt commands |
| Face steering | PC | Haar cascade finds a face; its position in the frame becomes left / right / forward / back / stop |
| Hand steering | PC | Same idea with a fist cascade |
| Traffic light | Pi | HSV masks for red and green; green drives, red stops |
| Object tracking | Pi | Largest coloured contour; centroid steers, contour area sets forward or reverse |
| Motion tracking | Pi | KNN background subtraction; turns toward the moving object |

## Architecture

```
   PC (controller/)                         Raspberry Pi 3 (robot/)
 ┌───────────────────────┐   UDP :5000    ┌──────────────────────────┐
 │ dashboard / keyboard  │ ─────────────▶ │ drive_udp.py             │
 │ joystick / face / hand│  '1'..'7'      │  GPIO → 2× H-bridge → 4 DC│
 │                       │                │  PWM  → camera servo      │
 │ pygame + OpenCV       │ ◀───────────── │ camera_stream.py         │
 └───────────────────────┘   UDP :11001   │  JPEG frames, chunked     │
                             video        └──────────────────────────┘
```

Command bytes: `1` right · `2` left · `3` backward · `4` forward · `5` stop · `6` camera down · `7` camera up.

Video: each frame is JPEG-encoded at quality 75 and sent as UDP datagrams of up to 65,565 bytes. A datagram shorter than that marks the end of a frame.

## Hardware

- Raspberry Pi 3, USB or Pi camera
- 4 DC motors on two H-bridge drivers. BOARD pins 3/5, 7/11, 8/10, 16/18
- Servo for camera tilt on BOARD pin 13, 50 Hz PWM

## Files

```
robot/                       runs on the Pi
  main_gui.py                Tkinter launcher: traffic light, object tracking, motion tracking, manual buttons (Jul 2017)
  traffic_light_threaded.py  traffic-light mode in its own thread (May 2017)
  drive_udp.py               receives command bytes over UDP and drives the motors (May 2017)
  camera_stream.py           sends camera frames over UDP (Jul 2017)
  drive_tcp_2016.py          first version of remote drive, over TCP (Mar 2016)
  servo_sweep_2016.py        first servo test (Mar 2016)
controller/                  runs on the PC
  dashboard.py               pygame dashboard with live video and controls (Jul 2017)
  keyboard_udp.py            keyboard drive
  joystick_udp.py            joystick drive
  face_steering.py           steer by face position
  hand_steering.py           steer by fist position
  ball_tracking.py           HSV ball tracking prototype
```

The two steering scripts expect `face.xml` and `fist.xml` next to them. Use `haarcascade_frontalface_default.xml` from OpenCV for the first; the fist cascade is a third-party file and is not redistributed here.

## Credits

Parts of this project were adapted from tutorials and open-source code, as student projects are:

- The UDP video transport in `robot/camera_stream.py` and the receiving thread in `controller/dashboard.py` are based on the open-source `udp-camera-stream` example (its original Polish comments are still in the code). I added the pygame display, the command channel and the detection modes around it.
- `controller/ball_tracking.py` follows a public OpenCV colour-tracking tutorial.
- Haar cascades are by their respective authors (the frontal-face cascade is by Rainer Lienhart, shipped with OpenCV).

Everything else, including the motor and servo control, the command protocol, the Tkinter and pygame front ends and the integration, is my own work.

## Author

Abdulkader Tarrab Refaee · [abdulkadertarrab.com](https://abdulkadertarrab.com)
