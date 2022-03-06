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
from termcolor import colored

model_path = get_model_path()
data_path = get_data_path()

def TranscribeVideo (filepath):
    transcribed_audio_file_name = "transcribed_video_speech.wav"
    video_file_name = filepath
    audioclip = AudioFileClip(video_file_name)
    audioclip.write_audiofile(transcribed_audio_file_name, nbytes=2)
    with contextlib.closing(wave.open(transcribed_audio_file_name, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        print('rate', rate, 'frames', frames, 'duration', duration)
    total_duration = math.ceil(duration / 60)
    r = sr.Recognizer()
    for z in range(0, total_duration):
        with sr.AudioFile(transcribed_audio_file_name) as source:
            audio = r.record(source, offset=z * 60, duration=60)
        timestr = time.strftime("%Y%m%d")
        filename = Path(filepath).name
        video_transcript_folderpath = '../transcripts/Video/'
        f = open(video_transcript_folderpath + timestr + "-" + str(filename) + "-" + "transcription.txt", "a")
        speech = r.recognize_sphinx(audio, language='en-us', show_all=False)
        print(speech)
        f.write(str(speech))
        f.write(" ")
    f.close()

def TranscribeAudio (filepath):
    transcribed_audio_file_name = "transcribed_audio_speech.wav"
    audioclip = AudioFileClip(filepath)
    audioclip.write_audiofile(transcribed_audio_file_name, nbytes=2)

    with contextlib.closing(wave.open(transcribed_audio_file_name, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        print('rate', rate, 'frames', frames, 'duration', duration)
    total_duration = math.ceil(duration / 60)
    r = sr.Recognizer()
    for z in range(0, total_duration):
        with sr.AudioFile(transcribed_audio_file_name) as source:
            audio = r.record(source, offset=z * 60, duration=60)
        timestr = time.strftime("%Y-%m-%d-%H-%M")
        filename = Path(filepath).name
        Audio_transcript_folderpath = "../transcripts/Audio/"
        f = open(Audio_transcript_folderpath + timestr + "-" + str(filename) + "-" + "transcription.txt", "a")
        speech = r.recognize_sphinx(audio, language='en-us')
        print(speech)
        f.write(str(speech))
        f.write(" ")
        transcription_path1 = ""
        transcription_path= transcription_path1 + str(f.name)
    f.close
    print(transcription_path)
    return transcription_path


def keyWord_Search (transcription_path,keywords):
    keyword_list = str(keywords).split(",")
    print(keyword_list)
    transcript = open(transcription_path, 'r')
    transcript_Lines = transcript.readlines()
    transcriptsStr = ''.join(transcript_Lines)
    print(transcriptsStr)

    for s in keyword_list:
        if s in transcriptsStr:
            print("Keyword " + s + " has been found in " + str(transcription_path))
        else:
            print("Keyword " + s + " NOT FOUND IN " + str(transcription_path))

    transcript.close()

if __name__ == '__main__':
    mime = magic.Magic(mime=True)
    filepath = input("Please input the path to your file:")
    if path.exists(filepath):
        FileType = mime.from_file(filepath)
        print(FileType)
        if str(FileType).__contains__("audio"):
            keywords = input("Please input the keywords:")
            transcription_path = TranscribeAudio(filepath)
            keyWord_Search(transcription_path,keywords)
        else:
            if str(FileType).__contains__("video"):
                TranscribeVideo(filepath)
            else:
                print("Not Valid File")
    else:
        print("File does not exist")
        exit(0)