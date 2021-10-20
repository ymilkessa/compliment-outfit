#!/usr/bin/env python
"""
This uses tf-pose library to fetch the key points of a person in an image.
The function upper_body_color() then identifies the upper body and returns an analysis of the color content.
# Used https://pythonprogramming.net/haar-cascade-face-eye-detection-python-opencv-tutorial/
""" 

import cv2
import numpy as np
from threading import Thread

from compliment import play_text_as_audio


COLORS_CV2 = {
    (0,0,255): 'red',
    (0,255,0): 'green',
    (255,0,0): 'blue',
    (0, 165, 255): 'orange',
    (0,255,255): 'yellow',
    (0,0,0): 'black',
    (0,75,150): 'brown',
    (180, 105, 255): 'pink',
    (128,128,128): 'gray',
    (208,224,64): 'turquoise',
    (175,1,134): 'violet',
    (255,255,255): 'white'
}


def compliment_outfit_using_webcam():
    """
    Reads images from the webcam. Estimates the chest-abdomen region of a person in the image,
    estimates the dominant color, and then prints out a compliment about the supposed outfit
    """
    model2 = cv2.data.haarcascades + 'haarcascade_profileface.xml'
    upper_body_cascade = cv2.CascadeClassifier(model2)

    face_to_body_height_ratio = 1.5
    
    # This list below will hold 1 if the comment on image function has been called.
    usage_indicator = []

    cap = cv2.VideoCapture(0)
    while 1:
        ret, img = cap.read()
        img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_grey = cv2.equalizeHist(img_grey)

        # Detect face bounds (and then translate to upper body)
        u_body_boxes = upper_body_cascade.detectMultiScale(img_grey, 1.1, 8)

        for (x,y,w,h) in u_body_boxes:
            # Replace the face box coordinates with an estimate for the upper body
            # First shift the starting point to somewhere below the lower left corner
            # Here I'm moving down by an extra one-third of the height of the 'face-box'
            x, y = x, round(y+(4*h/3)) 
            w, h = w, round(h * face_to_body_height_ratio)
            # Proceed only if the upper body is expected to be in view:
            if y + h <= img.shape[0]:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            
            # Getting this portion of the grey/color images
            # roi_gray = img_grey[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]

            # Comment on the color in that upper body
            comment = Thread (target=comment_on_image, args=(roi_color,usage_indicator,))
            comment.start()
            # comment.join()
            

        cv2.imshow('img',img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break


def comment_on_image (image, usage_indicator=[]):
    """
    Identify the main color in image and then say,
    'I like that <insert color> that ...'
    """
    # If the audio is being used, just return without playing
    if usage_indicator:
        return

    # Otherwise, set an indicator in this list and play the audio
    usage_indicator.append(1)
    color = find_dominant_color(image)
    if color is not None:
        statement = f"I like that {color} thing that you have on. Where did you get it?"
        play_text_as_audio (statement)
        usage_indicator.remove(1)


def find_dominant_color(image):
    """
    Simply picks the average values for B-G-R from the pixels in the given image.
    It then identifies the color that it is closest with.
    """
    # First find the average for each column (returning just one row of averages).
    col_avg = np.average(image, axis=0)
    # Now find the average for all the columns
    total_avg = np.average(col_avg, axis=0)
    
    # Fetch the color that this is closest to
    nearest_color = None
    nearest_squared_gap = 3*(255**2)
    for color_vector in COLORS_CV2:
        gap = np.sum(np.square(color_vector-total_avg))
        if gap < nearest_squared_gap:
            nearest_squared_gap = gap
            nearest_color = COLORS_CV2[color_vector]
    
    return nearest_color


if __name__=="__main__":
    compliment_outfit_using_webcam()
