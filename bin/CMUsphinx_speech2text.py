import speech_recognition as sr
from pocketsphinx import get_model_path, get_data_path
from configparser import ConfigParser
from datetime import datetime
from audio_extraction import splitAudio
from audio_extraction import convertMillis
from keyword_searching import searchKeywords
model_path = get_model_path()
data_path = get_data_path()

def PocketSphinx_transcribe(extractedAudio):
    r = sr.Recognizer()
    with sr.AudioFile(extractedAudio) as source:
        audio = r.listen(source)
        try:
            transcription_text = r.recognize_sphinx(audio)
        except:
            transcription_text = "ERROR - FAILED"
        return transcription_text


def pocketSphinx(extractedAudio, CaseConfigFileName, casePath):
    keywords = input("Please provide Keywords - Separate keyword with a comma: \n")
    keyword_list = str(keywords).split(",")
    print(keyword_list)
    print("Transcribing evidence using PocketSphinx - Please Wait!")
    for i in extractedAudio:
        evidence = i.split("|")
        mediafile = evidence[0]
        transcriptPath = evidence[1]
        evidenceItem = evidence[2]
        chunklist, lengthaudio, counter = splitAudio(mediafile, casePath)
        keywordsFoundList = []
        r = sr.Recognizer()
        keywordsFoundList = []
        for a in chunklist:
            z = a.split("|")
            wavchunk = z[0]
            timeframe = z[1]
            splitTimeframe = timeframe.split(":")
            starttime = convertMillis(int(splitTimeframe[0]))
            endtime = convertMillis(int(splitTimeframe[1]))
            transcription_text = PocketSphinx_transcribe(wavchunk)
            keywordsFound = searchKeywords(keyword_list, transcription_text, starttime, endtime, evidenceItem)
            keywordsFoundList.append(keywordsFound)
            for x in keywordsFound:
                keywordsFoundList.append(x)
        try:
            transcription_text = PocketSphinx_transcribe(mediafile)
            f = open(transcriptPath, "w")
            f.write(transcription_text)
            f.close()
        except:
            print("Transcription Error!")
        config = ConfigParser(strict=False)
        config['CaseConfiguration'] = {}
        config.read(CaseConfigFileName)
        ASRModel = "PocketSphinx"
        ASRVersion = str(sr.__version__)
        ASREngineUsed = ASRModel + " " + ASRVersion
        PocketSphinxModel = str(model_path + " " + data_path)
        config.set(str(evidenceItem), 'asrtranscription_engine_used', ASREngineUsed)
        config.set(str(evidenceItem), 'asrtranscription_model_used', PocketSphinxModel)
        config.set(str(evidenceItem), 'transcriptlocation', transcriptPath)
        config.set(str(evidenceItem), 'keywords', str(keywordsFound))
        now = datetime.now()
        modifiedDateTime = now.strftime("%m/%d/%Y, %H:%M:%S")
        config.set('CaseConfiguration', 'modifieddatetime', modifiedDateTime)
        with open(CaseConfigFileName, 'w') as configfile:
            config.write(configfile)
    print("Transcription Completed!")

