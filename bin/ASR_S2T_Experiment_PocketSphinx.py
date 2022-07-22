import speech_recognition as sr
import os
from pocketsphinx import Pocketsphinx, get_model_path, get_data_path

# model_path = get_model_path()
# data_path = get_data_path()
#
# config = {
#     'hmm': os.path.join(model_path, 'en-us'),
#     'lm': os.path.join(model_path, 'en-70k-0.2.lm'),
#     'dict': os.path.join(model_path, 'cmudict-en-us.dict')
# }

# print(model_path)
# print(data_path)
# ps = Pocketsphinx(**config)
# extractedAudio = r"C:\Users\Ahmed\PycharmProjects\SpeechTranscription\venv\Lib\site-packages\pocketsphinx\data\goforward.raw"
# ps.decode(
#     audio_file=extractedAudio,
#     buffer_size=2048,
#     no_search=False,
#     full_utt=False
# )
# print(ps.hypothesis())


def PocketSphinxEvaluation(extractedAudio):
    r = sr.Recognizer()
    with sr.AudioFile(extractedAudio) as source:
        audio = r.listen(source)
        try:
            transcription_text = r.recognize_sphinx(audio)
        except:
            transcription_text = "ERROR - FAILED"
        print(transcription_text)
        return transcription_text