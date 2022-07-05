from moviepy.editor import AudioFileClip
import os
from pydub import AudioSegment
from pathlib import Path
import datetime

def extract_audio_from_source (evidenceitem, evidencefilename, casePath):

    print("evidenceitem: " + os.path.normpath(evidenceitem))
    print("evidencefilename: " + os.path.normpath(evidencefilename))
    evidencefilename1 = os.path.splitext(evidencefilename)[0]
    evidencefilename2 = "\\" + evidencefilename
    print("casePath: " + os.path.normpath(casePath))
    extractedAudioPath = casePath + "\\ExtractedAudioFiles\\" + evidencefilename1 + "audio.wav"
    extractedtranscriptPath = casePath + "\\Transcripts\\" + evidencefilename1 + ".txt"
    print("Extracted Audio Path: " + os.path.normpath(extractedAudioPath))
    print ("Full Path to Evidence: " + os.path.normpath(evidenceitem) + evidencefilename2)
    evidenceitemAudio = os.path.normpath(evidenceitem) + evidencefilename2
    print("TEST" + evidenceitemAudio)
    audioclip = AudioFileClip(evidenceitemAudio)
    audioclip.write_audiofile(extractedAudioPath, nbytes=2, codec='pcm_s16le', ffmpeg_params=["-ac", "1", "-ar", "16000"])
    return extractedAudioPath, extractedtranscriptPath

def splitAudio(filename, casepath):
    # print(filename + "\n" + casepath)
    os.chdir(casepath)
    if not os.path.isdir("splitaudio"):
        os.mkdir("splitaudio")
    audio = AudioSegment.from_file(filename)
    lengthaudio = len(audio)
    # print("Length of Audio File", lengthaudio)
    chunklist = []
    start = 0
    # # In Milliseconds, this will cut 10 Sec of audio
    threshold = 10000
    end = 0
    counter = 0
    basename = os.path.basename(filename)
    mediafile1 = os.path.splitext(basename)[0]
    # print(mediafile1)
    while start < len(audio):

        end += threshold
        startStr = str(start)
        endStr = str(end)

        timewindow = str(startStr + ":" + endStr)
        chunk = audio[start:end]
        filename = f'splitaudio/{mediafile1}-chunk{counter}.wav'
        # print(filename)
        filenameTimeWindow = filename + "|" + timewindow
        # print(filenameTimeWindow)
        chunklist.append(filenameTimeWindow)
        chunk.export(filename, format="wav")
        counter += 1
        # print(counter)

        start += threshold
        # print(start)
    # print(chunklist)
    return chunklist, lengthaudio, counter


def convertMillis(millis):
    duration_ms = int(millis)
    millisConverted = datetime.datetime.fromtimestamp(duration_ms / 1000.0).strftime('%M:%S.%f')[:-5]
    return millisConverted
