# PocketSphinx ASR Engine Function for takes the audio file and uses the sphinx recogniser
# to transcribe audio files

import speech_recognition as sr
import time

def PocketSphinxEvaluation(extractedAudio):
    # PocketSphinx ASR Engine Function for ASR Evaluation Takes the audio file and uses the sphinx recogniser
    # transcribe audio files
    # Adapted from - https://pypi.org/project/SpeechRecognition/ &
    # https://github.com/Uberi/speech_recognition &
    # https://github.com/Uberi/speech_recognition/blob/master/examples/audio_transcribe.py
    r = sr.Recognizer()
    with sr.AudioFile(extractedAudio) as source:
        t0 = time.time()
        audio = r.listen(source)
        try:
            # Using the PocketSphinx Recogniser
            transcription_text = r.recognize_sphinx(audio)
        except:
            transcription_text = "ERROR - FAILED"
        print(transcription_text)
    transcription_text = str(transcription_text)
    t1 = time.time()
    total_transcription_time = t1 - t0
    print(str(total_transcription_time))
    return transcription_text, total_transcription_time