import deepspeech
import numpy as np
from deepspeech import Model
import wave
from configparser import ConfigParser
from datetime import datetime
from audio_extraction import splitAudio
from audio_extraction import convertMillis
from keyword_searching import searchKeywords
# Initialising default model and its parameters
model_file_path = '../models/DeepSpeech/deepspeech-0.9.3-models.pbmm'
lm_file_path = '../models/DeepSpeech/deepspeech-0.9.3-models.scorer'
beam_width = 500
lm_alpha = 0.92
lm_beta = 1.18
model = Model(model_file_path)
model.enableExternalScorer(lm_file_path)
model.setScorerAlphaBeta(lm_alpha, lm_beta)
model.setBeamWidth(beam_width)

# def read_wav_file(filename):
#     with wave.open(filename, 'rb') as w:
#         rate = w.getframerate()
#         frames = w.getnframes()
#         buffer = w.readframes(frames)
#         print(rate)
#         print(frames)
#     return buffer, rate
#
#
# def DeepSpeech_transcribe(extractedAudioFile):
#     buffer, rate = read_wav_file(extractedAudioFile)
#     data16 = np.frombuffer(buffer, dtype=np.int16)
#     return model.stt(data16)
#
# def deepSpeech(extractedAudio, CaseConfigFileName):
#     print("Transcribing Audio using DeepSpeech ASR Engine - Please wait")
#     for i in extractedAudio:
#         evidence = i.split("|")
#         mediafile = evidence[0]
#         transcriptPath = evidence[1]
#         evidenceItem = evidence[2]
#         print(evidenceItem)
#         # print(transcriptPath)
#         # print(mediafile)
#         transcription_text = DeepSpeech_transcribe(mediafile)
#         # print(transcription_text)
#         f = open(transcriptPath, "w")
#         f.write(transcription_text)
#         f.close()
#         config = ConfigParser(strict=False)
#         config['CaseConfiguration'] = {}
#         config.read(CaseConfigFileName)
#         deepspeechVersion = deepspeech.version()
#
#         ASRModel = "DeepSpeech"
#         ASREngineUsed = ASRModel + " " + deepspeechVersion
#         deepspeechModel =  str(model_file_path + " " + lm_file_path)
#         config.set(str(evidenceItem), 'asrtranscription_engine_used', ASREngineUsed)
#         config.set(str(evidenceItem), 'asrtranscription_model_used', deepspeechModel)
#         config.set(str(evidenceItem), 'transcriptlocation', transcriptPath)
#         now = datetime.now()
#         modifiedDateTime = now.strftime("%m/%d/%Y, %H:%M:%S")
#         config.set('CaseConfiguration', 'modifieddatetime', modifiedDateTime)
#         with open(CaseConfigFileName, 'w') as configfile:
#             config.write(configfile)
#     print("Transcription Completed!")

def read_wav_file(filename):
    with wave.open(filename, 'rb') as w:
        rate = w.getframerate()
        frames = w.getnframes()
        buffer = w.readframes(frames)
        # print(rate)
        # print(frames)
    return buffer, rate


def DeepSpeech_transcribe(extractedAudioFile):
    buffer, rate = read_wav_file(extractedAudioFile)
    data16 = np.frombuffer(buffer, dtype=np.int16)
    return model.stt(data16)

def deepSpeech(extractedAudio, CaseConfigFileName, casePath):
    keywords = input("Please provide Keywords - Separate keyword with a comma: \n")
    keyword_list = str(keywords).split(",")
    print(keyword_list)
    print("Transcribing Audio using DeepSpeech ASR Engine - Please wait")
    for i in extractedAudio:
        evidence = i.split("|")
        mediafile = evidence[0]
        transcriptPath = evidence[1]
        evidenceItem = evidence[2]
        # print(evidenceItem)
        chunklist, lengthaudio, counter = splitAudio(mediafile,casePath)
        # print(chunklist)
        keywordsFoundList = []
        for a in chunklist:
            z = a.split("|")
            wavchunk = z[0]
            timeframe = z[1]
            # print(wavchunk)
            # print(timeframe)
            splitTimeframe = timeframe.split(":")
            starttime = convertMillis(int(splitTimeframe[0]))
            endtime = convertMillis(int(splitTimeframe[1]))
            transcription_text = DeepSpeech_transcribe(wavchunk)
            # print(transcription_text)
            keywordsFound = searchKeywords(keyword_list,transcription_text,starttime,endtime,evidenceItem)
            for x in keywordsFound:
                keywordsFoundList.append(x)
        print(keywordsFoundList)
        transcription_text = DeepSpeech_transcribe(mediafile)
        # print(transcription_text)
        f = open(transcriptPath, "w")
        f.write(transcription_text)
        f.close()
        config = ConfigParser(strict=False)
        config['CaseConfiguration'] = {}
        config.read(CaseConfigFileName)
        deepspeechVersion = deepspeech.version()
        ASRModel = "DeepSpeech"
        ASREngineUsed = ASRModel + " " + deepspeechVersion
        deepspeechModel =  str(model_file_path + " " + lm_file_path)
        config.set(str(evidenceItem), 'asrtranscription_engine_used', ASREngineUsed)
        config.set(str(evidenceItem), 'asrtranscription_model_used', deepspeechModel)
        config.set(str(evidenceItem), 'transcriptlocation', transcriptPath)
        config.set(str(evidenceItem), 'keywords', str(keywordsFound))
        now = datetime.now()
        modifiedDateTime = now.strftime("%m/%d/%Y, %H:%M:%S")
        config.set('CaseConfiguration', 'modifieddatetime', modifiedDateTime)
        with open(CaseConfigFileName, 'w') as configfile:
            config.write(configfile)
    print("Transcription Completed!")








