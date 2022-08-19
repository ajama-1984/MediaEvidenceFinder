# Audio Extraction Python File
# Ahmed Jama


# Importing libraries needed
from moviepy.editor import AudioFileClip
import os
from pydub import AudioSegment
import datetime

def extract_audio_from_source (evidenceitem, evidencefilename, casePath):
    # Takes the evidence item and filename as well as the casepath, extracts the audio from media files and writes it
    # to the extracted audio folder within the case folder
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
    audioclip = AudioFileClip(evidenceitemAudio)
    audioclip.write_audiofile(extractedAudioPath, nbytes=2, codec='pcm_s16le', ffmpeg_params=["-ac", "1", "-ar", "16000"])
    audioclip.close()
    return extractedAudioPath, extractedtranscriptPath

def splitAudio(Audiofilename, casepath):
    # Takes the extracted audio file and splits it into 30 second chunks, thus prividing a timeframe for when a keyword was detected.
    # Adapted from - https://stackoverflow.com/questions/36799902/how-to-splice-an-audio-file-wav-format-into-1-sec-splices-in-python
    os.chdir(casepath)
    if not os.path.isdir("splitaudio"):
        os.mkdir("splitaudio")
    audio = AudioSegment.from_file(Audiofilename)
    lengthaudio = len(audio)
    segmentedEvidenceList = []
    starttime = 0
    threshold = 30000
    endtime = 0
    numberofSegments = 0

    AudioSourceFile = os.path.basename(Audiofilename)
    mediafile = os.path.splitext(AudioSourceFile)[0]

    while starttime < len(audio):
        # A while loop which based on the start, end time will loop the splitting of the audio file until the start
        # time matches the end time. A counter allows for the identification as to how many chunks are there,
        # as well as for naming each chunk in numerical order
        # returns the list of file chunks, the length of audio as well as the number of chunks
        endtime += threshold
        startimeStr = str(starttime)
        endtimeStr = str(endtime)

        timewindow = str(startimeStr + ":" + endtimeStr)
        # Split the audio based on start and end time
        segment = audio[starttime:endtime]
        filename = f'splitaudio/{mediafile}-chunk{numberofSegments}.wav'
        filenameTimeWindow = filename + "|" + timewindow
        segmentedEvidenceList.append(filenameTimeWindow)
        # exports the segmented file as a wav file preserving the audio properties (such as number of channels sample
        # rate etc)
        segment.export(filename, format="wav")
        numberofSegments += 1
        starttime += threshold
    return segmentedEvidenceList, lengthaudio, numberofSegments


def convertMillis(millis):
    # Converts the timestamps (the start and end time for each segment of evidence) from milliseconds to
    # hours:minutes:seconds
    duration_in_ms = int(millis)
    millisConverted = datetime.datetime.fromtimestamp(duration_in_ms / 1000.0)
    millisConverted = millisConverted.strftime('%H:%M:%S')
    return millisConverted


