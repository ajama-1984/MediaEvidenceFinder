from moviepy.editor import AudioFileClip
from pathlib import Path
import time
from moviepy.editor import AudioFileClip
import wave, math, contextlib
import glob, os

def extract_audio_from_source (func_code, dbdict):
    if func_code == "200":
        #extractedAudi_dict = {}
        for key, value in dbdict.items():
            if value.__contains__("audio") or value.__contains__("video"):
                evidenceFile = key
                timestr = time.strftime("%Y-%m-%d-%H-%M")
                extracted_audio_path = '../ExtractedAudio/'
                audio_extracted_file_name = extracted_audio_path + evidenceFile + timestr + "audio.wav"
                audioclip = AudioFileClip(evidenceFile)
                audioclip.write_audiofile(audio_extracted_file_name, nbytes=2)
                print(audio_extracted_file_name)
                dbdict[key].extend(audio_extracted_file_name)
                print(dbdict)
        return func_code
    # if fileName is not None:
    #     if func_code == "200":
    #         if str(file_type).__contains__("audio")or str(file_type).__contains__("video"):
    #             extracted_audio_path = '../ExtractedAudio/'
    #             timestr = time.strftime("%Y-%m-%d")
    #             audio_extracted_file_name = extracted_audio_path + fileName + timestr + "audio.wav"
    #             transcribed_audio_file_name = str(audio_extracted_file_name)
    #             audioclip = AudioFileClip(audio_extracted_file_name)
    #             audioclip.write_audiofile(transcribed_audio_file_name, nbytes=2)
    #             func_code = "200"
    #             return pathToFile, fileName, file_type, transcribed_audio_file_name, func_code
    #         else:
    #             func_code = "422"
    #             return pathToFile, fileName, func_code
    #     else:
    #         return pathToFile, func_code
    # else:
    #     func_code = "404"
    #     return func_code
