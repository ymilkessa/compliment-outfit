#!/usr/bin/env python

"""
This file houses functions to generate complements, save compliments to audio files,
or sound the compliment out loud.

Text-to-speech feature adopted from:
    https://www.geeksforgeeks.org/convert-text-speech-python/
"""

# import os
from playsound import playsound
from gtts import gTTS
import time
import os


def play_text_as_audio (text_string):
    tts = gTTS(text_string, lang='en')
    f_name = f"speech_{round(time.time())}.mp3"
    tts.save(f_name)

    # f_name is now like an mp3 file
    playsound(f_name)

    # The program should wait until the adio is played, and then delete the file
    os.remove (f_name)



if __name__=="__main__":
    play_text_as_audio ("Hello there!")
