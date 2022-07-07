import speech_recognition as sr

def PocketSphinxEvaluation(extractedAudio):
    r = sr.Recognizer()
    with sr.AudioFile(extractedAudio) as source:
        audio = r.listen(source)
        try:
            transcription_text = r.recognize_sphinx(audio)
        except:
            transcription_text = "ERROR - FAILED"
        return transcription_text
