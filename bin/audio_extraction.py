from moviepy.editor import AudioFileClip
from pathlib import Path
import time
from moviepy.editor import AudioFileClip
import wave, math, contextlib

def extract_audio_from_source (pathToFile, fileName, file_type, func_code):
    if fileName is not None:
        if func_code == "200":
            if str(file_type).__contains__("audio")or str(file_type).__contains__("video"):
                extracted_audio_path = '../ExtractedAudio/'
                timestr = time.strftime("%Y-%m-%d")
                audio_extracted_file_name = extracted_audio_path + fileName + timestr + "audio.wav"
                transcribed_audio_file_name = str(audio_extracted_file_name)
                audioclip = AudioFileClip(audio_extracted_file_name)
                audioclip.write_audiofile(transcribed_audio_file_name, nbytes=2)
                func_code = "200"
                return pathToFile, fileName, file_type, transcribed_audio_file_name, func_code
            else:
                func_code = "422"
                return pathToFile, fileName, func_code
        else:
            return pathToFile, func_code
    else:
        func_code = "404"
        return func_code
