#!/usr/local/bin/python3
"""
CONTRIBUTORS:
    Justin Culbertson-Faegre, Codie Orberson
DETAILED DESCRIPTION:
    This file is used for the detection of hand gestures within the system. This module simply loads the needed haar
    cascades and then adds the detection processes to the process manager to check for fists and palms within the
    current frame. More detailed information is available in section 3.2.10 in the SDD
REQUIREMENTS ADDRESSED:
    FR.2, FR.3, FR.10, FR.14, NFR.2, NFR.8, NFR.6, EIR.1
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


from gesture import Gesture
import keyboard


class CascadeGestureDetector():
    def __init__(self):
        self.gestures = Gesture()
        self.gestures.set_values("bestfist.xml", 1.2, 5)
        self.gestures.set_values("cascade.xml", 1.2, 30)
        self.gestures.set_values("eye3.xml", 1.1, 36)
        self.gestures.set_values("face.xml", 1.3, 5)
        
    def get_last_detected_gesture(self):
        return self.gestures.gesture_detected_frame
        
    def set_perimeters(self, perimeters):
        self.gestures.set_perimeters(perimeters)
        
    def detect_face(self, frame):
        return(self.gestures.detect_face(frame))
        
    def detect_eyes(self, frame):
        return(self.gestures.detect_eyes(frame))

    def detect_hand_gesture(self, frame):
        if self.gestures.first_hand_gesture_index_detected == 0:
            if self.gestures.detect_hand_gesture(frame, 0):
                return True
            return self.gestures.detect_hand_gesture(frame, 1)
            
        else:
            if self.gestures.detect_hand_gesture(frame, 1):
                return True
            return self.gestures.detect_hand_gesture(frame, 0)
        