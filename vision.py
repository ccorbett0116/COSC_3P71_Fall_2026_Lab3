#!/usr/bin/env python3
"""
COSC 3P71 - Lab 3: Computer vision - colour + shape detection.

    YOUR NAME:

Copy this file, lab3_check.py and requirements.txt (replacing the Lab 2
one) into your Lab_2 folder, next to run_robot.py (README, Setup). Then,
from that folder:

    python vision.py --check      # test your work - no robot needed. Run it often.
    python vision.py              # the TurboPi's camera (robot Wi-Fi)
    python vision.py 0            # a webcam on this computer
    python vision.py ball.png     # a saved picture

GOAL: show the camera in a window and label every cube and sphere it sees
with its colour and shape, e.g. "red cube", "blue sphere".

--check calls the five functions and the COLOURS list below by name, so
keep those names and do what each docstring says. Everything else is up to
you: add as many helper functions as you like. The README walks you through
it one step at a time: do the steps IN ORDER and run --check after each one.
"""
import sys

import cv2              # pip install -r requirements.txt
import numpy as np

# The robot's camera, streamed by web_video_server on the robot as MJPEG.
# OpenCV can open this URL directly. Check it in a browser first (README, Setup).
ROBOT_IP = "192.168.149.1"
STREAM_URL = f"http://{ROBOT_IP}:8080/stream?topic=/image_raw"

# One dictionary per colour to find (README, Step 2). Each needs a "name":
# "red", "green", "blue" and "yellow". Add whatever other keys you need.
COLOURS = []


# -- Step 1: frames in, window out ---------------------------------------------

def open_source(source):
    """`source` is a string: "robot", a webcam number such as "0", or an
    image file name. Return something with a .read() method that returns
    (ok, frame), like cv2.VideoCapture does (README, Step 1)."""
    # TODO (Step 1)


# -- Steps 2 and 3: one colour -> a mask -----------------------------------------

def build_mask(hsv, colour):
    """`hsv` is a whole picture in HSV; `colour` is one entry of COLOURS.
    Return a 2-D mask the same height and width as `hsv`: white (255) where
    the picture is that colour, black (0) everywhere else, with specks
    removed and small holes filled (README, Steps 2 and 3)."""
    # TODO (Step 2, cleaned up in Step 3)


# -- Step 4: blobs -> shapes ---------------------------------------------------

def classify_shape(contour):
    """`contour` is one outline from cv2.findContours. Return "cube",
    "sphere" or "unknown" (README, Step 4)."""
    # TODO (Step 4)


# -- Step 5: every colour, every object ----------------------------------------

def detect(frame):
    """Find every object of every colour in one BGR frame. Return a list
    with one dictionary per object, each with at least:
        "colour": its colour's name, e.g. "red"
        "shape":  "cube", "sphere" or "unknown"
        "centre": (x, y) of its middle, in pixels
    (README, Step 5)."""
    # TODO (Step 5)


def draw_detections(frame, detections):
    """Draw an outline and a "colour shape" label on `frame` for each
    detection from detect() (README, Step 5)."""
    # TODO (Step 5)


# -- Putting it together -------------------------------------------------------

def main():
    print("vision.py is running - nothing implemented yet (Lab 3, Stage 2).")
    # TODO (Steps 1 - 5): read the source from sys.argv, then loop:
    #   grab a frame -> detect -> draw -> show -> handle keys (p saves, q quits).


if __name__ == "__main__":
    if "--check" in sys.argv:           # leave these three lines alone
        from lab3_check import self_check
        sys.exit(self_check())
    main()
