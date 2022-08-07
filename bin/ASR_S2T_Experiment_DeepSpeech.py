# DeepSpeech ASR Engine Evaluation Python File
# Date 05/09/2022
# Adapted from - Mozilla DeepSpeech Documentation on Github - https://github.com/mozilla/DeepSpeech/releases/tag/v0.9.3
# & DeepSpeech Labs - https://github.com/rosariomoscato/Rosario-Moscato-Lab/blob/main/Audio/DeepSpeech.ipynb
# https://deepspeech.readthedocs.io/en/latest/Python-API.html
# https://deepspeech.readthedocs.io/en/latest/Python-Examples.html
# https://discourse.mozilla.org/t/deepspeech-not-recognizing-indian-english-accent/70629
# Ahmed Jama
# # # # # # # # # # # # #

from deepspeech import Model
import wave
import numpy as np
import time

# Initialising default model and its parameters
# Model and parameters from from https://github.com/mozilla/DeepSpeech/releases/tag/v0.9.3
model_file_path = '../models/DeepSpeech/deepspeech-0.9.3-models.pbmm'
lm_file_path = '../models/DeepSpeech/deepspeech-0.9.3-models.scorer'
beam_width = 500
lm_alpha = 0.92
lm_beta = 1.18
model = Model(model_file_path)
model.enableExternalScorer(lm_file_path)
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

def deepSpeechEvaluation(extractedAudioFile):
    # Main function for the ASR engine evaluation of Deepspeech which transcribes the extracted audio files from the
    # experiment sample
    t0 = time.time()
    transcription_text = DeepSpeech_transcribe(extractedAudioFile)
    transcription_text = str(transcription_text)
    t1 = time.time()
    total_transcription_time = t1 - t0
    print(str(total_transcription_time))
    return transcription_text, total_transcription_time
