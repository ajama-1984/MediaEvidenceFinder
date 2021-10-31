import time
import wave, math, contextlib
import speech_recognition as sr
from moviepy.editor import AudioFileClip
from pathlib import Path

def TranscribeVideo (filepath):
    transcribed_audio_file_name = "transcribed_speech.wav"
    video_file_name = filepath
    audioclip = AudioFileClip(video_file_name)
    audioclip.write_audiofile(transcribed_audio_file_name)
    with contextlib.closing(wave.open(transcribed_audio_file_name, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
    total_duration = math.ceil(duration / 60)
    r = sr.Recognizer()
    for z in range(0, total_duration):
        with sr.AudioFile(transcribed_audio_file_name) as source:
            audio = r.record(source, offset=z * 60, duration=60)
        timestr = time.strftime("%Y%m%d")
        filename = Path(filepath).name
        video_transcript_folderpath = './transcripts/Video/'
        f = open(video_transcript_folderpath + timestr + "-" + str(filename) + "-" + "transcription.txt", "a")
        speech = r.recognize_google(audio, language='en-GB', show_all=True)
        print(speech)
        f.write(str(speech))
        f.write(" ")
    f.close()

def TranscribeAudio (filepath):
    transcribed_audio_file_name = "transcribed_speech.wav"
    audioclip = AudioFileClip(filepath)
    audioclip.write_audiofile(transcribed_audio_file_name)

    with contextlib.closing(wave.open(transcribed_audio_file_name, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
    total_duration = math.ceil(duration / 60)
    r = sr.Recognizer()
    for z in range(0, total_duration):
        with sr.AudioFile(transcribed_audio_file_name) as source:
            audio = r.record(source, offset=z * 60, duration=60)
        timestr = time.strftime("%Y%m%d-%H%M%S")
        filename = Path(filepath).name
        Audio_transcript_folderpath = "./transcripts/Audio/"
        f = open(Audio_transcript_folderpath + timestr + "-" + str(filename) + "-" + "transcription.txt", "a")
        speech = r.recognize_sphinx(audio, language='en', show_all=True)
        print(speech)
        f.write(str(speech))
        f.write(" ")
    f.close

if __name__ == '__main__':
    filepath = input("Please input the path to your file:    ")
    if filepath.endswith('.mp4') or filepath.endswith('.mp3'):
        print(filepath)
    else:
        print("empty/invalid input")
        filepath = input("Please input the path to your file")
    source_type = input("Is this a Video or Audio   ")
    if source_type == "Video":
        TranscribeVideo(filepath)
    else:
        if source_type == "Audio":
            print("Audio is not supported yet")
            exit(0)
