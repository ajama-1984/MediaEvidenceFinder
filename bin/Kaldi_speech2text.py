from vosk import Model, KaldiRecognizer
import wave
import json
import os
from configparser import ConfigParser
from datetime import datetime
from yaspin import yaspin
from vosk import SetLogLevel
SetLogLevel(-1)

model = Model(r"C:\Users\Ahmed\PycharmProjects\SpeechTranscription\models\Kaldi")
recogniser = KaldiRecognizer(model, 16000)

def Kaldi_Transcribe(extractedAudio):
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
            # print(result_dict)
            transcription.append(result_dict.get("text", ""))
            # print(transcription)
    final_result = json.loads(rec.FinalResult())
    transcription.append(final_result.get("text", ""))
    transcription_text = ' '.join(transcription)
    return transcription_text

def kaldi (extractedAudio, CaseConfigFileName):
    print("Initialising Kaldi ASR Engine with default english model - Please Wait")
    with yaspin():
        model = Model(r"C:\Users\Ahmed\PycharmProjects\SpeechTranscription\models\Kaldi")
        recogniser = KaldiRecognizer(model, 16000)
    print("Transcribing Evidence Please Wait")
    for i in extractedAudio:
        evidence = i.split("|")
        mediafile = evidence[0]
        transcriptPath = evidence[1]
        evidenceItem = evidence[2]
        wf = wave.open(mediafile, "rb")
        file_size = os.path.getsize(mediafile)
        rec = KaldiRecognizer(model, wf.getframerate())
        transcription = []
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                # Convert json output to dict
                result_dict = json.loads(rec.Result())
                # print(result_dict)
                transcription.append(result_dict.get("text", ""))
                # print(transcription)
        final_result = json.loads(rec.FinalResult())
        transcription.append(final_result.get("text", ""))
        transcription_text = ' '.join(transcription)
        # print(transcription_text)
        f = open(transcriptPath, "w")
        f.write(transcription_text)
        f.close()
        config = ConfigParser(strict=False)
        config['CaseConfiguration'] = {}
        config.read(CaseConfigFileName)
        ASRModel = "Kaldi"
        ASREngineUsed = ASRModel
        deepspeechModel =  str(r"C:\Users\Ahmed\PycharmProjects\SpeechTranscription\models\Kaldi")
        config.set(str(evidenceItem), 'asrtranscription_engine_used', ASREngineUsed)
        config.set(str(evidenceItem), 'asrtranscription_model_used', deepspeechModel)
        config.set(str(evidenceItem), 'transcriptlocation', transcriptPath)
        now = datetime.now()
        modifiedDateTime = now.strftime("%m/%d/%Y, %H:%M:%S")
        config.set('CaseConfiguration', 'modifieddatetime', modifiedDateTime)
        with open(CaseConfigFileName, 'w') as configfile:
            config.write(configfile)
    print("Transcription Complete! - Transcripts can be found in Transcripts folder of the case")
