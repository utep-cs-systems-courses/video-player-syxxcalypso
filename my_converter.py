#!/usr/bin/env python3

# Jen Sim
# CS 4375
# Video Player
# Collaborator: Nick Sims

import base64, cv2, os, numpy, sys

from threading import Thread
from my_queue import MyQueue as Queue  # Import custom queue

finished_extracting = False  # Extracting status boolean
finished_filtering = False  # Filtering status boolean


def main():

    count = 0
    maxFrames = 72
    color_buffer = Queue()  # Buffer for color frames
    greyscale_buffer = Queue()  # Buffer for grey frames
    video_capture = cv2.VideoCapture("clip.mp4")  # Create VideoCapture obj

    threads = [
        Thread(
            target=extract_frames, args=[video_capture, maxFrames, color_buffer],
        ),  # Func spec Threads
        Thread(target=convert_frames, args=[color_buffer, greyscale_buffer]),
        Thread(target=render, args=[greyscale_buffer]),
    ]

    for t in threads:  # For each thread
        t.start()  # start thread
    for t in threads:  # For each thread
        t.join()  # join the threads


"""
extract_frames()
reads the obj, extracts individual frames from input file
"""


def extract_frames(video_capture, maxFrames, color_buffer):
    global finished_extracting  # Declaration

    count = 1
    data = video_capture.read()
    while data and data[0] and count <= maxFrames:  # While there's data & <= cap:
        status, image = data  #
        color_buffer.put(image)  # Put frame image in queue
        data = video_capture.read()  # Read frames from obj
        count += 1  # Increase frame counter

    finished_extracting = True  # After all frames are read
    color_buffer.put(None)  # put None to signify done extracting


"""
convert_frames()
converts color frames to greyscale frames
input_buffer = color_buffer
output_buffer = grayscale_buffer
"""


def convert_frames(input_buffer, output_buffer):
    global finished_extracting  # Declaration
    global finished_filtering

    while not (
        input_buffer.is_empty() and finished_extracting
    ):  # if buffer !empty& !finished extracting frames

        colored_frame = input_buffer.get()  # gets colored frame from color_buffer
        if colored_frame is None:  # continue if no frames
            continue

        converted_frame = cv2.cvtColor(
            colored_frame, cv2.COLOR_BGR2GRAY
        )  # converts the color frame to gray
        output_buffer.put(converted_frame)  # put gray frame in queue

    finished_filtering = True  # done filtering, out of loop
    output_buffer.put(None)  # put None to signify done filtering


"""
render()
Display the gray-scale frames
input_buffer = grayscale buffer
"""


def render(input_buffer):
    global finished_filtering  # Declaration

    while not (
        input_buffer.is_empty() and finished_filtering
    ):  # graybuffer !empty & !finished filtering

        frame = input_buffer.get()  # get grayframe from queue
        if frame is None:  # continue through frames
            continue

        cv2.imshow("Video", frame)
        if cv2.waitKey(42) and 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()  # destroys all windows created


if __name__ == "__main__":
    main()
