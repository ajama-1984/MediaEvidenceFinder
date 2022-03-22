import time
import wave, math, contextlib
import speech_recognition as sr
from pocketsphinx import AudioFile, get_model_path, get_data_path
model_path = get_model_path()
data_path = get_data_path()

def pocketsphinx_S2T (pathToFile, fileName, file_type, transcribed_audio_file_name, func_code):
    if transcribed_audio_file_name is not None and func_code == "200":
        with contextlib.closing(wave.open(transcribed_audio_file_name, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
        duration = frames / float(rate)
        print('rate', rate, 'frames', frames, 'duration', duration)
        total_duration = math.ceil(duration)
        r = sr.Recognizer()
        for z in range(0, total_duration):
            with sr.AudioFile(transcribed_audio_file_name) as source:
                audio = r.record(source, offset=z * 60, duration=60)
            timestr = time.strftime("%Y%m%d")
            transcript_folderpath = '../Transcriptions'
            f = open(transcript_folderpath + timestr + "-" + str(fileName) + "-" + "transcription.txt", "a")
            speech = r.recognize_sphinx(audio, language='en-us', show_all=False)
            print(speech)
            f.write(str(speech))
            f.write(" ")
        f.close()
        transcription_file = str(f)
        func_code = "200"
        return pathToFile, fileName, file_type,func_code, transcription_file
    else:
        func_code = "404"
        return func_code