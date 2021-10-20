#!/usr/bin/env python
"""
Tests on identifying body features using opencv
Using https://pythonprogramming.net/haar-cascade-face-eye-detection-python-opencv-tutorial/ 
"""


import cv2

FILE_NAME = "blue_sweater_guy2.jpg"


def test_cascade_stuff():
    """
    Prints out where in an image an upper body is located.
    TODO: This haarcascade actually generates a large box around the face. Dunno why.
    """
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


if __name__=="__main__":
    test_cascade_stuff()
