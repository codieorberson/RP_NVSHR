#!/usr/local/bin/python3
"""
CONTRIBUTORS:
    Justin Culbertson-Faegre, Codie Orberson
DETAILED DESCRIPTION:
    This file is responsible for adding the perimeters to the gestures being detected. This is also where the system
    checks a flipped frame from the camera in order to recognize gestures from the users left hand. This is also where
    the system loads in the haar cascades used to detect the hand gestures.
REQUIREMENTS ADDRESSED:
    FR.2, FR.3, FR.14, NFR.2, NFR.6
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

import cv2
import imutils

class Gesture:
    def __init__(self, detection_check = lambda detected_gestures: len(detected_gestures) > 0, debug_color = (0, 0, 255)):
        self.haar_cascade = []
        self.scale_factor = []
        self.min_neighbors = []
        self.perimeters = []
        self.debug_color = debug_color
        self.detection_check = detection_check
        self.count = 0
        self.hand_gesture_angles = [[0, 20, 340, 40], [0, 15, 345, 30, 330, 45]]
        self.first_hand_gesture_index_detected = 0
        self.gesture_detected_frame = None
    
    def set_values(self, haar_cascade_xml, scale_factor, min_neighbors):
        self.haar_cascade.append(cv2.CascadeClassifier(haar_cascade_xml))
        self.scale_factor.append(scale_factor)
        self.min_neighbors.append(min_neighbors)
    
    def set_perimeters(self, perimeters):
        for i in perimeters:
            self.perimeters.append(i)

    def get_detected_face_dimensions(self, frame):
        for (x, y, w, h) in frame:
            if h <= 60:
                self.x = int(4.27 * (x+ 8))
                self.y = int(4.04 * (y + 13))
                self.w = int(4.27 * (w - 18))
                self.h = int(4.04 * (h -38))
                return
            self.x = int(4.27 * (x+ 9))
            self.y = int(4.04 * (y + 16))
            self.w = int(4.27 * (w - 19))
            self.h = int(4.04 * (h -49))
            
    
    def crop_frame(self, frame):
        self.crop_eye_frame = frame[self.y: self.y + self.h, self.x: self.x + self.w]
        resized_cropped_eye_frame = cv2.resize(self.crop_eye_frame, (675, 270), interpolation= cv2.INTER_AREA)
        return resized_cropped_eye_frame

    def detect_face(self, frame):
        gesture = self.haar_cascade[3].detectMultiScale(frame, self.scale_factor[3], self.min_neighbors[3])
        if self.detection_check(gesture):
            self.get_detected_face_dimensions(gesture)
            self.perimeters[4].set(gesture[0])
            return True
        return False
    
    def detect_eyes(self, frame):
        frame = self.crop_frame(frame)
        gesture = self.haar_cascade[2].detectMultiScale(frame, self.scale_factor[2], self.min_neighbors[2])
        if self.detection_check(gesture):
            self.perimeters[2].set([int(self.x/ 4.27),int(self.y/ 4.04), int(self.w/4.27),int(self.h/4.04) ])
            return False
        else:
            return True

    def detect_hand_gesture(self, frame, index):
        for j, i in enumerate(self.hand_gesture_angles[index]):
            if i != 0:
                new_frame = imutils.rotate_bound(frame, i)
            else:
                new_frame = frame
            gesture = self.haar_cascade[index].detectMultiScale(new_frame, self.scale_factor[index], self.min_neighbors[index])
            if self.detection_check(gesture):
                self.hand_gesture_angles[index][j], self.hand_gesture_angles[index][0] = self.hand_gesture_angles[index][0], i
                gesture[0][0], gesture[0][1], gesture[0][2], gesture[0][3] = int(gesture[0][0] / 1.3), int(gesture[0][1] / 1.5), int(gesture[0][2] / 1.3), int(gesture[0][3] / 1.5), 
                self.perimeters[index].set(gesture[0])
                self.gesture_detected_frame = gesture[0]
                self.first_hand_gesture_index_detected = index
                return True
        return False

    def detect_flipped_gesture(self, flipped_gesture, size):
        flipped_gesture[0][0] = size - flipped_gesture[0][0]
        return flipped_gesture
