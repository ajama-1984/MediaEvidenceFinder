import speech_recognition as sr

def PocketSphinxEvaluation(extractedAudio):
    r = sr.Recognizer()
    with sr.AudioFile(extractedAudio) as source:
        audio = r.listen(source)
        transcription_text = r.recognize_sphinx(audio)
        # print(transcription_text)
        return transcription_text
