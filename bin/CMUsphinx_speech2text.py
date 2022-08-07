# PocketSphinx Functions

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
    # PocketSphinx ASR Engine Function for takes the audio file and uses the sphinx recogniser
    # to transcribe audio files
    # Adapted from - https://pypi.org/project/SpeechRecognition/ &
    # https://github.com/Uberi/speech_recognition &
    # https://github.com/Uberi/speech_recognition/blob/master/examples/audio_transcribe.py
    r = sr.Recognizer()
    with sr.AudioFile(extractedAudio) as source:
        audio = r.listen(source)
        try:
            transcription_text = r.recognize_sphinx(audio)
        except:
            transcription_text = "ERROR - FAILED"
        return transcription_text

# Overall ASR function for PocketSphinx, which calls the various function above and writes the generated transcripts to
# the transcripts' folder, updates the case configuration file with kewyords found on each peice of evidence as well
# as timestamps.
def pocketSphinx(extractedAudio, CaseConfigFileName, casePath):
    keywords = input("Please provide Keywords - Separate keyword with a comma: \n")
    keyword_list = str(keywords).split(",")
    print("Transcribing evidence using PocketSphinx - Please Wait!")
    for i in extractedAudio:
        evidence = i.split("|")
        mediafile = evidence[0]
        transcriptPath = evidence[1]
        evidenceItem = evidence[2]
        # Evidence split into chunks so that each chunk of 30 seconds can be transcribed and keyword searching can be
        # conducted.
        chunklist, lengthaudio, counter = splitAudio(mediafile, casePath)
        # Keywords provided
        keywordsFoundList = []
        print("Transcribing Evidence Item " + evidenceItem + " Please Wait")
        # Creates empty transcript text file ready for writing with ASR generated transcript
        open(transcriptPath, 'w').close()
        for a in chunklist:
            # for each 30 second chunk of evidence, the evidence is transcribed, written to the transcript text file and
            # the keywords found added to list, which includes the keyword, timestamp pairs
            z = a.split("|")
            wavchunk = z[0]
            timeframe = z[1]
            splitTimeframe = timeframe.split(":")
            starttime = convertMillis(int(splitTimeframe[0]))
            endtime = convertMillis(int(splitTimeframe[1]))
            transcription_text = PocketSphinx_transcribe(wavchunk)
            f = open(transcriptPath, "a")
            f.write("\n")
            f.write(transcription_text)
            f.close()
            keywordsFound = searchKeywords(keyword_list, transcription_text, starttime, endtime, evidenceItem)
            keywordsFoundList.append(keywordsFound)
            for x in keywordsFound:
                keywordsFoundList.append(x)
        # Once the evidence is transcribed, the resulting keywords, transcript location as well as what ASR
        # Engine/Model were utilised is updated for that evidence object.
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
        config.set(str(evidenceItem), 'keywords', str(keywordsFoundList))
        now = datetime.now()
        modifiedDateTime = now.strftime("%m/%d/%Y, %H:%M:%S")
        config.set('CaseConfiguration', 'modifieddatetime', modifiedDateTime)
        config.set('CaseConfiguration', 'case_keywords', keywords)
        with open(CaseConfigFileName, 'w') as configfile:
            config.write(configfile)
    print("Transcription Completed!")

