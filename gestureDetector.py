import time
import numpy as np
from matplotlib import pyplot as plt
from cascadeGestureDetector import CascadeGestureDetector
from multithreadedPerimeter import MultithreadedPerimeter
import imutils
import cv2

"""
CONTRIBUTORS:
    Justin Culbertson-Faegre, Codie Orberson, Landan Ginther
DETAILED DESCRIPTION:
    This file creates an interface for combining the detection of eye blinks and hand gestures. It starts by creating
    instances of the needed subcomponents and then sets up the system to begin drawing the red rectangles within the
    debug tab. Once everything is set up correctly, the system can then begin calling the detect method to reset the
    perimeters for the rectangles, detect the various gestures (including the left hand) and eye blinks, and triggering
    the linked events for those gestures. Once it recognizes a gesture, it begins to draw the rectangles that are shown
    in the debug tab. More detailed information is available in section 3.2.2 in the SDD
REQUIREMENTS ADDRESSED:
    FR.1, FR.2, FR.3, FR.8, FR.14, NFR.2, NFR.5, NFR.6, EIR.1, OR.1
LICENSE INFORMATION:
    Copyright (c) 2019, CSC 450 Group 4
    All rights reserved.
    Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
    following conditions are met:
        * Redistributions of source code must retain the above copyright notice, this list of conditions and the
          following disclaimer.
        * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and
          the following disclaimer in the documentation and/or other materials provided with the distribution.
        * Neither the name of the CSC 450 Group 4 nor the names of its contributors may be used to endorse or
          promote products derived from this software without specific prior written permission.
    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
    INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
    OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
    DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
    STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
    EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""


class GestureDetector:
    def __init__(self):
        self.__set_up_helpers__()
        self.__set_up_perimeters__()
        self.gesture_events = []
        self.gesture_detected = None
        self.timer_start = 0
        self.timer_end = 0
        self.first_frame = None
        self.frame_dimension = (400, 266)
        self.resized_frame = None
        self.temporary_hand_gesture_frame = 0
        self.repeated_detected_gestures = False

    def on_gesture(self, callback):
        self.gesture_events.append(callback)

    def get_gesture_detected(self):
        return self.gesture_detected

    # Method is to be run in separate thread
    def detect(self, frame, resized_frame, timestamp, open_eye_threshold):
        self.__reset_perimeters__()
        self.__detect_shapes__(frame, resized_frame)
        self.__trigger_events__(timestamp, open_eye_threshold)
        return self.__draw_rectangles__(resized_frame)

    def __detect_shapes__(self, frame, resized_frame):
        self.blinked = False
        if not self.repeated_detected_gestures:
            self.hand_gesture_frame = cv2.resize(frame, self.frame_dimension, interpolation= cv2.INTER_AREA)
            gaussian_frame = cv2.GaussianBlur(self.hand_gesture_frame, (21, 21), 0)

            if self.check_timer(gaussian_frame):
                return
            
            self.timer_start = time.time()
            if not self.contour_finder(gaussian_frame):
                return

        else:
            self.hand_gesture_frame = cv2.resize(frame, self.frame_dimension, interpolation= cv2.INTER_AREA)
            self.hand_gesture_frame = self.hand_gesture_frame[self.top:self.top+self.bottom, self.left:self.left+self.right]
        
        self.timer_start = time.time()
        if self.cascade_gesture_detector.detect_hand_gesture(self.hand_gesture_frame):
            self.timer_end = self.timer_start + 5
            self.repeated_detected_gestures = True
            return
        
        if (self.repeated_detected_gestures and self.timer_end - self.timer_start <4):
            self.repeated_detected_gestures = False

        if self.cascade_gesture_detector.detect_face(resized_frame):
            if self.cascade_gesture_detector.detect_eyes(frame):
                self.blinked = True
                self.timer_end = self.timer_start + 5
                return
        
    def check_timer(self, frame):
        if (self.timer_start > self.timer_end) or self.timer_start == 0:
            self.timer_start = time.time()
            self.timer_end = self.timer_start + 15
            self.first_frame = frame
            return True
        return False

    '''
    def contour_finder(self, frame):
        
        frameDelta = cv2.absdiff(self.first_frame, frame)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        #loop over the contours
        if len(cnts)> 0:
            c = max(cnts, key =cv2.contourArea)
            (x, y, w, h) = cv2.boundingRect(c)
            if x > 10:
                x = x - 10
            if y > 10:
                y = y -10
            self.hand_gesture_frame = self.hand_gesture_frame[y:y+h + 10, x:x+w + 10]
            return True
        return False
    '''
    def contour_finder(self, frame):
        
        frameDelta = cv2.absdiff(self.first_frame, frame)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        coordinates_box = []
        #loop over the contours
        if len(cnts)> 0:
            for c in cnts:
                if cv2.contourArea(c) < 200:
                    continue

                (x, y, w, h) = cv2.boundingRect(c)
                coordinates_box.append([x,y,x+w, y+h])
            
            if len(coordinates_box) == 0:
                return False

            coordinates_box = np.asarray(coordinates_box)
            self.left = np.min(coordinates_box[:,0])
            self.top = np.min(coordinates_box[:,1])
            self.right = np.max(coordinates_box[:,2])
            self.bottom = np.max(coordinates_box[:,3])

            if(self.left > 5):
                self.left -=5

            self.hand_gesture_frame = self.hand_gesture_frame[self.top:self.top+self.bottom, self.left:self.left+self.right]
            return True
        return False
    
    def __trigger_events__(self, timestamp, open_eye_threshold):
        self.gesture_detected = None

        self.__trigger_hand_events__(self.fist_perimeter, 'fist', timestamp)
        self.__trigger_hand_events__(self.palm_perimeter, 'palm', timestamp)
        self.__trigger_blink_events__(timestamp)

    def __trigger_hand_events__(self, perimeter, gesture_name, timestamp):
        if perimeter.is_set():
            self.gesture_detected = gesture_name
            for event in self.gesture_events:
                event(gesture_name, timestamp)

    def __trigger_blink_events__(self, timestamp):
        if self.blinked:
            self.gesture_detected = "blink"
            for event in self.gesture_events:
                event('blink', timestamp)

    def __draw_rectangles__(self, frame):
        for perimeter in self.perimeters:
            if perimeter.is_set():
                cv2.rectangle(frame, perimeter.get_top_corner(), perimeter.get_bottom_corner(), (0, 0, 255), 2)
        return frame

    def __reset_perimeters__(self):
        for perimeter in self.perimeters:
            perimeter.set((0, 0, 0, 0))

    def __set_up_helpers__(self):
        self.cascade_gesture_detector = CascadeGestureDetector()

    def __set_up_perimeters__(self):
        self.fist_perimeter = MultithreadedPerimeter()
        self.palm_perimeter = MultithreadedPerimeter()
        self.left_eye_perimeter = MultithreadedPerimeter()
        self.right_eye_perimeter = MultithreadedPerimeter()
        self.face_perimeter = MultithreadedPerimeter()

        self.perimeters = [
            self.fist_perimeter,
            self.palm_perimeter,
            self.left_eye_perimeter,
            self.right_eye_perimeter,
            self.face_perimeter
        ]

        self.cascade_gesture_detector.set_perimeters(self.perimeters)

    def flip_frame(self, frame):
        frame = cv2.flip(frame, flipCode=1)
        return frame
