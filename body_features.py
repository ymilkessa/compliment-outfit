#!/usr/bin/env python
"""
This uses tf-pose library to fetch the key points of a person in an image.
The function upper_body_color() then identifies the upper body and returns an analysis of the color content.
"""
# TODO: try https://pythonprogramming.net/haar-cascade-face-eye-detection-python-opencv-tutorial/ 
# import tf_pose  # the installed version appears incomplete
import cv2
# import os
# import time

FILE_NAME = "blue_sweater_guy2.jpg"


def get_shoulder_dims (pose_obj):
    pass


def test_cascade_stuff():
    # cv2_base_dir = os.path.dirname(os.path.abspath(cv2.__file__))
    # haar_model = os.path.join(cv2_base_dir, 'data/haarcascade_upperbody.xml')
    model2 = cv2.data.haarcascades + 'haarcascade_upperbody.xml'
    upper_body_cascade = cv2.CascadeClassifier(model2)
    img = cv2.imread(FILE_NAME)

    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_grey = cv2.equalizeHist(img_grey)

    # Detect upper body bounds
    u_body_boxes = upper_body_cascade.detectMultiScale(img_grey, 1.1, 8)
    print (u_body_boxes)


def test_cascade_from_webcam():
    model2 = cv2.data.haarcascades + 'haarcascade_profileface.xml'
    upper_body_cascade = cv2.CascadeClassifier(model2)

    face_to_body_height_ratio = 1.5

    cap = cv2.VideoCapture(0)
    while 1:
        ret, img = cap.read()
        img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_grey = cv2.equalizeHist(img_grey)

        # Detect upper body bounds (?)
        u_body_boxes = upper_body_cascade.detectMultiScale(img_grey, 1.1, 8)

        for (x,y,w,h) in u_body_boxes:
            # Replace the face box coordinates with an estimate for the upper body
            x, y = x, y+h # First shift the starting point to the lower left corner
            w, h = w, round(h * face_to_body_height_ratio)
            # Proceed only if the upper body is expected to be in view:
            if y + h <= img.shape[0]:
                try:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                except TypeError:
                    breakpoint()
            
            # # Getting this portion of the grey/color images
            # # Can use this for color detection
            # roi_gray = img_grey[y:y+h, x:x+w]
            # roi_color = img[y:y+h, x:x+w]

        cv2.imshow('img',img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

        # print (u_body_boxes)



if __name__=="__main__":
    test_cascade_from_webcam()
