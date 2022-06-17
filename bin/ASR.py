from vosk import Model, KaldiRecognizer
import speech_recognition as sr
from yaspin import yaspin
from vosk import SetLogLevel
from configparser import ConfigParser
from Case import Case
import wave
import json
import os
SetLogLevel(-1)
from tqdm.notebook import tqdm
from audio_extraction import extract_audio_from_source

class ASREngine:
    def __init__(self, ASREngineName,ASREngineModel):
        self.ASREngineName = ASREngineName
        self.ASREngineModel = ASREngineModel

    def extractAudio (self,CaseConfigFileName, CurrentCase):
        config = ConfigParser(strict=False)
        config['CaseConfiguration'] = {}
        config.read(CaseConfigFileName)
        EvidenceList = (config.get('CaseConfiguration', 'evidenceidlist'))
        EvidenceList = EvidenceList.split(",")
        EvidenceList[:] = [x for x in EvidenceList if x]
        casePath = Case.get_casePath(self, CurrentCase)
        evidenceAudioFile = []
        for evidenceItem in EvidenceList:
            evidenceitem = config.get(str(evidenceItem), 'evidencefilepath')
            evidenceName = config.get(str(evidenceItem), 'evidencefilename')
            evidenceExtractedAudio, extractedtranscriptPath = extract_audio_from_source(evidenceitem,evidenceName,casePath)
            evidenceAudioFile.append(evidenceExtractedAudio + "|" + extractedtranscriptPath + "|" + evidenceItem)
        return evidenceAudioFile

    def ASREngine(self, CaseConfigFileName, CurrentCase):
        print("========================================================")
        print("Please Select ASR Engine for transcribing and searching evidence")
        print("1 - Kaldi")
        print("2 - PocketSphinx")
        userInput = input("Please Select ASR Engine for transcribing and searching evidence\n")
        if userInput == "1":
            userInput = input("Press 1 to use default model or 2 to enter a path to a custom model you wish to use for Kaldi\n")
            print("========================================================")
            if userInput == "1":
                try:
                    print("Extracting Audio from Evidence  - Please wait")
                    with yaspin():
                        extractedAudio = ASREngine.extractAudio(self, CaseConfigFileName, CurrentCase)
                    print("Extracting Audio from Evidence Complete!")
                    print("Initialising Kaldi ASR Engine with default english model - Please Wait")
                    with yaspin():
                        model = Model(r"C:\Users\Ahmed\PycharmProjects\SpeechTranscription\models\Kaldi")
                        recogniser = KaldiRecognizer(model, 16000)
                    print("Transcribing Evidence Please Wait")
                    with yaspin():
                        for i in extractedAudio:
                            # print(i)
                            evidence = i.split("|")
                            mediafile = evidence[0]
                            transcriptPath = evidence[1]
                            evidenceItem = evidence[2]
                            # print(mediafile)
                            # print(transcriptPath)
                            # print(evidenceItem)
                            wf = wave.open(mediafile, "rb")
                            file_size = os.path.getsize(mediafile)
                            # print(file_size)
                            rec = KaldiRecognizer(model, wf.getframerate())
                            transcription = []
                            while True:
                                data = wf.readframes(4000)
                                if len(data) == 0:
                                    break
                                if rec.AcceptWaveform(data):
                                    # Convert json output to dict
                                    result_dict = json.loads(rec.Result())
                                    # print(result_dict)
                                    transcription.append(result_dict.get("text", ""))
                                    # print(transcription)
                            final_result = json.loads(rec.FinalResult())
                            transcription.append(final_result.get("text", ""))
                            transcription_text = ' '.join(transcription)
                            # print(transcription_text)
                            f = open(transcriptPath, "w")
                            f.write(transcription_text)
                            f.close()
                    print("Transcription Complete! - Transcripts can be found in Transcripts folder of the case")
                except:
                    print("Evidence Audio Extraction/ Automated transcription ERROR!")
                    func_code = "404"
                    return func_code
            else:
                userInput = input("Enter Path for Custom Kaldi Model - See https://alphacephei.com/vosk/models - for compatible models in several lanuages\n")
                try:
                    with yaspin():
                        model = Model(userInput)
                        # recogniser = KaldiRecognizer(model, 16000)
                    func_code = "200"
                    ASREngineName = "Kaldi"
                    ASREngineModel = userInput
                    print("The following ASR Engine and model has been initialised: " + ASREngineName + " " + ASREngineModel)
                    return func_code, ASREngineName, ASREngineModel, model
                except:
                    print("Model/data is not valid. Chosen ASR Engine and Model has NOT been initialised")
                    func_code = "404"
                    return func_code
        else:
            if userInput == "2":
                userInput = input("Provide Path to Model folder for the PocketSphinx ASR Engine\n")
                userInput2 = input("Provide Path to data folder for the PocketSphinx ASR Engine\n")
                try:
                    model_path = userInput
                    data_path = userInput2
                    with yaspin():
                        recogniser = sr.Recognizer()
                    ASREngineName = "PocketSphinx"
                    ASREngineModel = model_path
                    func_code = "200"
                    print("The following ASR Engine and model has been initialised: " + ASREngineName + " " + ASREngineModel)
                    return recogniser, func_code, ASREngineName, ASREngineModel
                except:
                    print("Model/data is not valid. Chosen ASR Engine and Model has NOT been initialised")
                    func_code = "404"
                    return func_code
            else:
                print("Invalid Selection Exiting Program")
                exit(0)





