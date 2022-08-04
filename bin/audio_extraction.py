from moviepy.editor import AudioFileClip
import os
from pydub import AudioSegment
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

def splitAudio(Audiofilename, casepath):
    os.chdir(casepath)
    if not os.path.isdir("splitaudio"):
        os.mkdir("splitaudio")
    audio = AudioSegment.from_file(Audiofilename)
    lengthaudio = len(audio)
    chunklist = []
    start = 0
    threshold = 30000
    end = 0
    counter = 0

    AudioSourceFile = os.path.basename(Audiofilename)
    mediafile = os.path.splitext(AudioSourceFile)[0]

    while start < len(audio):
        end += threshold
        startStr = str(start)
        endStr = str(end)

        timewindow = str(startStr + ":" + endStr)
        chunk = audio[start:end]
        filename = f'splitaudio/{mediafile}-chunk{counter}.wav'
        filenameTimeWindow = filename + "|" + timewindow
        chunklist.append(filenameTimeWindow)
        chunk.export(filename, format="wav")
        counter += 1

        start += threshold
    return chunklist, lengthaudio, counter


def convertMillis(millis):
    duration_ms = int(millis)
    millisConverted = datetime.datetime.fromtimestamp(duration_ms / 1000.0)
    millisConverted = millisConverted.strftime('%H:%M:%S')
    return millisConverted


