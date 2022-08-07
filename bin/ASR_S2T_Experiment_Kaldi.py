# Transcription function using Kaldi ASR Engine and default Model for ASR Evaluation
# Adapted from - https://github.com/alphacep/vosk-api/blob/master/python/example/test_simple.py and
# https://towardsdatascience.com/transcribe-large-audio-files-offline-with-vosk-a77ee8f7aa28
# Ahmed Jama
# # # # # # # # # # # # #
from vosk import Model, KaldiRecognizer
import wave
import json
import time
from vosk import SetLogLevel
SetLogLevel(-1) # Supresses Log messages

def kaldiEvaluation (extractedAudio):
    # Transcription function using Kaldi ASR Engine and default Model for ASR Evaluation
    # Adapted from - https://github.com/alphacep/vosk-api/blob/master/python/example/test_simple.py and
    # https://towardsdatascience.com/transcribe-large-audio-files-offline-with-vosk-a77ee8f7aa28
    model = Model(r"../models/Kaldi")
    recogniser = KaldiRecognizer(model, 16000)
    wf = wave.open(extractedAudio, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    transcription = []
    while True:
        t0 = time.time()
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            # Convert json output to dict
            result_dict = json.loads(rec.Result())
            # print(result_dict)
            transcription.append(result_dict.get("text", ""))
            # print(transcription)
    # Extracts transcript and returns transcript
    final_result = json.loads(rec.FinalResult())
    transcription.append(final_result.get("text", ""))
    transcription_text = ' '.join(transcription)
    transcription_text = str(transcription_text)
    t1 = time.time()
    total_transcription_time = t1 - t0
    print(str(total_transcription_time))
    return transcription_text, total_transcription_time

