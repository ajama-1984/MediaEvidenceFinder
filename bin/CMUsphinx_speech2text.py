import speech_recognition as sr
from pocketsphinx import AudioFile, get_model_path, get_data_path
from configparser import ConfigParser
from datetime import datetime
model_path = get_model_path()
data_path = get_data_path()

def pocketSphinx(extractedAudio, CaseConfigFileName):
    print("Transcribing evidence using PocketSphinx - Please Wait!")
    for i in extractedAudio:
        evidence = i.split("|")
        mediafile = evidence[0]
        transcriptPath = evidence[1]
        evidenceItem = evidence[2]
        r = sr.Recognizer()
        print(mediafile)
        with sr.AudioFile(mediafile) as source:
            audio = r.listen(source)
            try:
                transcription_text = r.recognize_sphinx(audio)
                print(transcription_text)
                f = open(transcriptPath, "w")
                f.write(transcription_text)
                f.close()
            except:
                print("Transcription Failed!")
                exit(0)
        config = ConfigParser(strict=False)
        config['CaseConfiguration'] = {}
        config.read(CaseConfigFileName)
        ASRModel = "PocketSphinx"
        ASRVersion = str(sr.__version__)
        ASREngineUsed = ASRModel + " " + ASRVersion
        deepspeechModel = str(model_path + " " + data_path)
        config.set(str(evidenceItem), 'asrtranscription_engine_used', ASREngineUsed)
        config.set(str(evidenceItem), 'asrtranscription_model_used', deepspeechModel)
        config.set(str(evidenceItem), 'transcriptlocation', transcriptPath)
        now = datetime.now()
        modifiedDateTime = now.strftime("%m/%d/%Y, %H:%M:%S")
        config.set('CaseConfiguration', 'modifieddatetime', modifiedDateTime)
        with open(CaseConfigFileName, 'w') as configfile:
            config.write(configfile)
    print("Transcription Completed!")

