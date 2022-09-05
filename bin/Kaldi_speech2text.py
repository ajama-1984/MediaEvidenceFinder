# Transcription function using Kaldi ASR Engine and default Model for the tool
# Adapted from - https://github.com/alphacep/vosk-api/blob/master/python/example/test_simple.py and
# https://towardsdatascience.com/transcribe-large-audio-files-offline-with-vosk-a77ee8f7aa28
# Ahmed Jama
# # # # # # # # # # # # #
from vosk import Model, KaldiRecognizer
import wave
import json
from configparser import ConfigParser
from datetime import datetime
from audio_extraction import splitAudio
from audio_extraction import convertMillis
from keyword_searching import searchKeywords
from reportGenerator import generateReport
from halo import Halo
from vosk import SetLogLevel
SetLogLevel(-1) # Supresses Log Messages
import os

def Kaldi_Transcribe(extractedAudio):
    # Transcription function using Kaldi ASR Engine and default Model
    # Adapted from - https://github.com/alphacep/vosk-api/blob/master/python/example/test_simple.py and
    # https://towardsdatascience.com/transcribe-large-audio-files-offline-with-vosk-a77ee8f7aa28
    # Get directory of model folder without changing program directory.
    directory = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../models/Kaldi'))
    # Initalise Kaldi Model
    model = Model(directory)
    # Read audio file
    wf = wave.open(extractedAudio, "rb")
    # Intalises the Kaldi recogniser using the model and the opened audio file on a per frame basis
    rec = KaldiRecognizer(model, wf.getframerate())
    transcription = []
    while True:
        # Each frame of the audio file is read
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            # Convert json output to dict
            result_dict = json.loads(rec.Result())
            # Retrieve the value of the text key, which is the transcript
            transcription.append(result_dict.get("text", ""))
    final_result = json.loads(rec.FinalResult())
    transcription.append(final_result.get("text", ""))
    transcription_text = ' '.join(transcription)
    # Transcript returned
    return transcription_text

def kaldi (extractedAudio, CaseConfigFileName, casePath):
    print("#####################################################")
    keywords = input("Please provide Keywords - Separate keyword with a comma: \n")
    keyword_list = str(keywords).split(",")
    for i in extractedAudio:
        evidence = i.split("|")
        mediafile = evidence[0]
        transcriptPath = evidence[1]
        evidenceItem = evidence[2]
        evidenceName = evidence[3]
        print("#####################################################")
        print("Transcribing Evidence Item " + evidenceItem + " - " + evidenceName + " Using Kaldi. Please Wait!")
        print("#####################################################")
        chunklist, lengthaudio, counter = splitAudio(mediafile, casePath)
        keywordsFoundList = []
        open(transcriptPath, 'w').close()
        for a in chunklist:
            z = a.split("|")
            wavchunk = z[0]
            timeframe = z[1]
            splitTimeframe = timeframe.split(":")
            starttime = convertMillis(int(splitTimeframe[0]))
            endtime = convertMillis(int(splitTimeframe[1]))
            transcription_text = Kaldi_Transcribe(wavchunk)
            f = open(transcriptPath, "a")
            f.write("\n")
            f.write(transcription_text)
            f.close()
            keywordsFound = searchKeywords(keyword_list,transcription_text,starttime,endtime,evidenceItem)
            for x in keywordsFound:
                keywordsFoundList.append(x)
        config = ConfigParser(strict=False)
        config['CaseConfiguration'] = {}
        config.read(CaseConfigFileName)
        ASRModel = "Kaldi"
        ASREngineUsed = ASRModel
        directory = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../models/Kaldi'))
        kaldiModel =  str(directory)
        config.set(str(evidenceItem), 'asrtranscription_engine_used', ASREngineUsed)
        config.set(str(evidenceItem), 'asrtranscription_model_used', kaldiModel)
        config.set(str(evidenceItem), 'transcriptlocation', transcriptPath)
        config.set(str(evidenceItem), 'keywords', str(keywordsFoundList))
        now = datetime.now()
        modifiedDateTime = now.strftime("%m/%d/%Y, %H:%M:%S")
        config.set('CaseConfiguration', 'modifieddatetime', modifiedDateTime)
        config.set('CaseConfiguration', 'case_keywords', keywords)
        with open(CaseConfigFileName, 'w') as configfile:
            config.write(configfile)
    print("#####################################################")
    print("Transcription Completed!")
    print("#####################################################")
    generateReport(CaseConfigFileName)
