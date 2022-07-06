from vosk import Model, KaldiRecognizer
import wave
import json
import os
from vosk import SetLogLevel
SetLogLevel(-1)

def kaldiEvaluation (extractedAudio):
    model = Model(r"../models/Kaldi")
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
    # print(transcription_text)
    return transcription_text

