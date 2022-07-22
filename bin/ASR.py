from yaspin import yaspin
from configparser import ConfigParser
from Case import Case
from audio_extraction import extract_audio_from_source
from Deepspeech_speech2text import deepSpeech
from CMUsphinx_speech2text import pocketSphinx
from Kaldi_speech2text import kaldi

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
        print("3 - DeepSpeech")
        userInput = input("Please Select ASR Engine for transcribing and searching evidence\n")
        if userInput == "1":
            userInput = input("Press 1 to use default model or 2 to enter a path to a custom model you wish to use for Kaldi\n")
            print("========================================================")
            if userInput == "1":
                try:
                    print("Extracting Audio from Evidence  - Please wait")
                    extractedAudio = ASREngine.extractAudio(self, CaseConfigFileName, CurrentCase)
                    print("Extracting Audio from Evidence Complete!")
                    casePath = Case.get_casePath(self, CurrentCase)
                    kaldi(extractedAudio, CaseConfigFileName, casePath)
                except:
                    print("Evidence Audio Extraction/ Automated transcription ERROR!")
                    func_code = "404"
                    return func_code
            else:
                userInput = input("Enter Path for Custom Kaldi Model - See https://alphacephei.com/vosk/models - for compatible models in several lanuages\n")
        else:
            if userInput == "2":
                print("Initialising default PocketSphinx model\n")
                try:
                    print("Extracting Audio from Evidence  - Please wait")
                    with yaspin():
                        extractedAudio = ASREngine.extractAudio(self, CaseConfigFileName, CurrentCase)
                    casePath = Case.get_casePath(self, CurrentCase)
                    pocketSphinx(extractedAudio, CaseConfigFileName, casePath)
                except:
                    print("Program Error")
                    func_code = "404"
                    return func_code
            else:
                if userInput == "3":
                    extractedAudio = ASREngine.extractAudio(self, CaseConfigFileName, CurrentCase)
                    casePath = Case.get_casePath(self, CurrentCase)
                    deepSpeech(extractedAudio, CaseConfigFileName, casePath)
                else:
                    print("Invalid Selection Exiting Program")
                    exit(0)