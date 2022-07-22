from deepspeech import Model
import wave
import numpy as np
import time
import librosa

model_file_path = '../models/DeepSpeech/deepspeech-0.9.3-models.pbmm'
lm_file_path = '../models/DeepSpeech/deepspeech-0.9.3-models.scorer'
beam_width = 500
lm_alpha = 0.92
lm_beta = 1.18
model = Model(model_file_path)
model.enableExternalScorer(lm_file_path)
model.setScorerAlphaBeta(lm_alpha, lm_beta)
model.setBeamWidth(beam_width)

def read_wav_file(extractedAudioFile):
    with wave.open(extractedAudioFile, 'rb') as w:
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

def deepSpeechEvaluation(extractedAudioFile):
    duration = librosa.get_duration(filename=extractedAudioFile)
    t0 = time.time()
    transcription_text = DeepSpeech_transcribe(extractedAudioFile)
    t1 = time.time()
    total_transcription_time = t1 - t0
    print("Duration of Recording is = " + str(duration))
    print("Total Transcription Time = " + str(total_transcription_time))
    return transcription_text


if __name__ == '__main__':
    deepSpeechEvaluation(r"C:\Users\Ahmed\PycharmProjects\SpeechTranscription\dataset\commonVoice\extractedAudio\common_voice_en_1699.wav")