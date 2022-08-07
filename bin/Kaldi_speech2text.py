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
from yaspin import yaspin
from vosk import SetLogLevel
SetLogLevel(-1) # Supresses Log Messages

# Specify Model Path
model = Model(r"C:\Users\Ahmed\PycharmProjects\SpeechTranscription\models\Kaldi")
# Initialise ASR engine with the model
recogniser = KaldiRecognizer(model, 16000)

def Kaldi_Transcribe(extractedAudio):
    # Transcription function using Kaldi ASR Engine and default Model
    # Adapted from - https://github.com/alphacep/vosk-api/blob/master/python/example/test_simple.py and
    # https://towardsdatascience.com/transcribe-large-audio-files-offline-with-vosk-a77ee8f7aa28
    with yaspin():
        model = Model(r"C:\Users\Ahmed\PycharmProjects\SpeechTranscription\models\Kaldi")
        recogniser = KaldiRecognizer(model, 16000)
    wf = wave.open(extractedAudio, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    transcription = []
    while True:
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
    return transcription_text

def kaldi (extractedAudio, CaseConfigFileName, casePath):
    keywords = input("Please provide Keywords - Separate keyword with a comma: \n")
    keyword_list = str(keywords).split(",")
    print("Initialising Kaldi ASR Engine with default english model - Please Wait")
    for i in extractedAudio:
        evidence = i.split("|")
        mediafile = evidence[0]
        transcriptPath = evidence[1]
        evidenceItem = evidence[2]
        chunklist, lengthaudio, counter = splitAudio(mediafile, casePath)
        keywordsFoundList = []
        print("Transcribing Evidence Item " + evidenceItem + " Please Wait")
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
        print(keywordsFoundList)
        config = ConfigParser(strict=False)
        config['CaseConfiguration'] = {}
        config.read(CaseConfigFileName)
        ASRModel = "Kaldi"
        ASREngineUsed = ASRModel
        deepspeechModel =  str(r"C:\Users\Ahmed\PycharmProjects\SpeechTranscription\models\Kaldi")
        config.set(str(evidenceItem), 'asrtranscription_engine_used', ASREngineUsed)
        config.set(str(evidenceItem), 'asrtranscription_model_used', deepspeechModel)
        config.set(str(evidenceItem), 'transcriptlocation', transcriptPath)
        config.set(str(evidenceItem), 'keywords', str(keywordsFoundList))
        now = datetime.now()
        modifiedDateTime = now.strftime("%m/%d/%Y, %H:%M:%S")
        config.set('CaseConfiguration', 'modifieddatetime', modifiedDateTime)
        config.set('CaseConfiguration', 'case_keywords', keywords)
        with open(CaseConfigFileName, 'w') as configfile:
            config.write(configfile)
    print("Transcription Completed!")
    generateReport(CaseConfigFileName)
