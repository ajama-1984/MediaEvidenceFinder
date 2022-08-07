# DeepSpeech ASR Engine Python File Ahmed Jama Date 05/09/2022 Code Adapted from - Mozilla DeepSpeech Documentation
# on Github - https://github.com/mozilla/DeepSpeech/releases/tag/v0.9.3 &
# DeepSpeech Labs - https://github.com/rosariomoscato/Rosario-Moscato-Lab/blob/main/Audio/DeepSpeech.ipynb
# DeepSpeech Python API Documentation - https://deepspeech.readthedocs.io/en/latest/Python-API.html
# DeepSpeech Python API Example - https://deepspeech.readthedocs.io/en/latest/Python-Examples.html
# importing libraries
import deepspeech
import numpy as np
from deepspeech import Model
import wave
from configparser import ConfigParser
from datetime import datetime
from audio_extraction import splitAudio
from audio_extraction import convertMillis
from keyword_searching import searchKeywords
from reportGenerator import generateReport
import sys
from os.path import abspath
filename = r'C:\Users\Ahmed\PycharmProjects\SpeechTranscription\definitions.py'
print(filename)
sys.path.insert(1, filename)
from definitions import *

# Initialising default model and its parameters
# Model and parameters from from https://github.com/mozilla/DeepSpeech/releases/tag/v0.9.3

model_file_path = ROOT_DIR + "\\model\\DeepSpeech\\" + 'deepspeech-0.9.3-models.pbmm'
scorer_file_path = ROOT_DIR + "\\model\\DeepSpeech\\" + 'deepspeech-0.9.3-models.scorer'

# model_file_path = r'C:\Users\Ahmed\PycharmProjects\SpeechTranscription\models\DeepSpeech\deepspeech-0.9.3-models.pbmm'
# scorer_file_path = r'C:\Users\Ahmed\PycharmProjects\SpeechTranscription\models\DeepSpeech\deepspeech-0.9.3-models.scorer'
# Default parameters utilised as detailed in - https://github.com/mozilla/DeepSpeech/releases/tag/v0.9.3 under Training Regimen + Hyperparameters for fine-tuning
beam_width = 500
lm_alpha = 0.92
lm_beta = 1.18
model = Model(model_file_path)
model.enableExternalScorer(scorer_file_path)
model.setScorerAlphaBeta(lm_alpha, lm_beta)
model.setBeamWidth(beam_width)

# Function reads an extracted audio file and returns the buffered frames as well as the framerate
# Buffer will be utilised for the model to transcribe each frame of audio
def read_extracted_wav_file(extractedaudioFileName):
    with wave.open(extractedaudioFileName, 'rb') as w:
        framerate = w.getframerate()
        frames = w.getnframes()
        buffer = w.readframes(frames)
    return buffer, framerate

# Transcription function of DeepSpeech. Transcribes evidence using engine and model
def DeepSpeech_transcribe(extractedaudioFileName):
    buffer, rate = read_extracted_wav_file(extractedaudioFileName)
    data16 = np.frombuffer(buffer, dtype=np.int16)
    return model.stt(data16)


# Overall ASR function for deepspeech, which calls the various function above and writes the generated transcripts to
# the transcripts' folder, updates the case configuration file with kewyords found on each peice of evidence as well
# as timestamps.
def deepSpeech(evidenceObjects, CaseConfigFileName, casePath):
    keywords = input("Please provide Keywords - Separate keyword with a comma: \n")
    # Keywords provided
    keyword_list = str(keywords).split(",")
    print("Transcribing Audio using DeepSpeech ASR Engine - Please wait")
    # For each piece of evidence the evidence is transcribed in 30 second chunks, and the resulting transcript is
    # searched for keywords and each segment of evidence transcribed is written to the transcript path which is a
    # text file with the evidence name as the filename
    for i in evidenceObjects:
        evidence = i.split("|")
        mediafile = evidence[0]
        transcriptPath = evidence[1]
        evidenceItem = evidence[2]
        # Evidence split into chunks so that each chunk of 30 seconds can be transcribed and keyword searching can be
        # conducted.
        chunklist, lengthaudio, counter = splitAudio(mediafile, casePath)
        # Empty keyword list
        keywordsFoundList = []
        print("Transcribing Evidence Item " + evidenceItem + " Please Wait")
        # Creates empty transcript text file ready for writing with ASR generated transcript
        open(transcriptPath, 'w').close()
        # for each 30 second chunk of evidence, the evidence is transcribed, written to the transcript text file and
        # the keywords found added to list, which includes the keyword, timestamp pairs
        for a in chunklist:
            z = a.split("|")
            wavchunk = z[0]
            timeframe = z[1]
            splitTimeframe = timeframe.split(":")
            starttime = convertMillis(int(splitTimeframe[0]))
            endtime = convertMillis(int(splitTimeframe[1]))
            transcription_text = DeepSpeech_transcribe(wavchunk)
            f = open(transcriptPath, "a")
            f.write("\n")
            f.write(transcription_text)
            f.close()
            keywordsFound = searchKeywords(keyword_list, transcription_text, starttime, endtime, evidenceItem)
            for x in keywordsFound:
                keywordsFoundList.append(x)

        # Once the evidence is transcribed, the resulting keywords, transcript location as well as what ASR
        # Engine/Model were utilised is updated for that evidence object.
        config = ConfigParser(strict=False)
        config['CaseConfiguration'] = {}
        config.read(CaseConfigFileName)
        deepspeechVersion = deepspeech.version()
        ASRModel = "DeepSpeech"
        ASREngineUsed = ASRModel + " " + deepspeechVersion
        deepspeechModel = str(model_file_path + " " + scorer_file_path)
        config.set(str(evidenceItem), 'asrtranscription_engine_used', ASREngineUsed)
        config.set(str(evidenceItem), 'asrtranscription_model_used', deepspeechModel)
        config.set(str(evidenceItem), 'transcriptlocation', transcriptPath)
        config.set(str(evidenceItem), 'keywords', str(keywordsFoundList))
        now = datetime.now()
        modifiedDateTime = now.strftime("%m/%d/%Y, %H:%M:%S")
        config.set('CaseConfiguration', 'modifieddatetime', modifiedDateTime)
        config.set('CaseConfiguration', 'case_keywords', keywords)
        # All the updated values are written to the case configuration file
        with open(CaseConfigFileName, 'w') as configfile:
            config.write(configfile)
    print("Transcription Completed!")
    generateReport(CaseConfigFileName)

