import time
from moviepy.editor import AudioFileClip
from os.path import expanduser
import os
from pydub import AudioSegment as am


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
    audioclip.write_audiofile(extractedAudioPath, nbytes=2, codec='pcm_s16le', ffmpeg_params=["-ac", "1"])
    return extractedAudioPath, extractedtranscriptPath