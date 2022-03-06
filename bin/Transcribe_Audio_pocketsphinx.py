import mimetypes
import time
import wave, math, contextlib
import speech_recognition as sr
from moviepy.editor import AudioFileClip
from pathlib import Path
import magic
import os.path
from os import path
from pocketsphinx import AudioFile, get_model_path, get_data_path

model_path = get_model_path()
data_path = get_data_path()


def TranscribeAudio ():

    LOCATION = ('transcribed_audio_speech16bit2.wav')
    r = sr.Recognizer()

    with sr.AudioFile(LOCATION) as source:
        audio = r.record(source)
        print(r.recognize_sphinx(audio, language='en-us', show_all=False))


if __name__ == '__main__':
    TranscribeAudio()
