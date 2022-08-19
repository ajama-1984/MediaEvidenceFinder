# ASR Class and Functions
# Ahmed Jama
# # # # # # # # # # # # #

# Importing needed libraries
from configparser import ConfigParser # writing to config file
from Case import Case # Class class and functions
from audio_extraction import extract_audio_from_source # audio extraction function
from Deepspeech_speech2text import deepSpeech # ASR engine function
from CMUsphinx_speech2text import pocketSphinx # ASR engine function
from Kaldi_speech2text import kaldi # ASR engine function

class ASREngine:
    def __init__(self, ASREngineName,ASREngineModel):
        # Intialise ASR class information
        self.ASREngineName = ASREngineName
        self.ASREngineModel = ASREngineModel
    # extracting audio function which extracts audio sotred in the evidence objects in the case configuration file
    def extractAudio (self,CaseConfigFileName, CurrentCase):
        config = ConfigParser(strict=False)
        config['CaseConfiguration'] = {}
        config.read(CaseConfigFileName)
        EvidenceList = (config.get('CaseConfiguration', 'evidenceidlist'))
        EvidenceList = EvidenceList.split(",")
        EvidenceList[:] = [x for x in EvidenceList if x]
        casePath = Case.get_casePath(self, CurrentCase)
        evidenceAudiodata = []
        for evidenceItem in EvidenceList: # For every piece of evidence, the audio contained in the evidence is
            # extracted and the extracted audio file path, as well as the transcript path is returned to be utilised
            # in the ASR function
            evidenceitem = config.get(str(evidenceItem), 'evidencefilepath')
            evidenceName = config.get(str(evidenceItem), 'evidencefilename')
            evidenceExtractedAudio, extractedtranscriptPath = extract_audio_from_source(evidenceitem,evidenceName,casePath)
            evidenceAudiodata.append(evidenceExtractedAudio + "|" + extractedtranscriptPath + "|" + evidenceItem + "|" + evidenceName)
        return evidenceAudiodata

    def ASREngine(self, CaseConfigFileName, CurrentCase):
        # This function is the main ASR sequence function which transcribes evidence and conduct keyword search utilising
        # several functions written on a per component basis
        # User is presented with a choice of ASR engines 
        print("========================================================")
        print("Please Select ASR Engine for transcribing and searching evidence")
        print("1 - Kaldi")
        print("2 - PocketSphinx")
        print("3 - DeepSpeech")
        userInput = input("Please Select ASR Engine for transcribing and searching evidence\n")
        # The audio is extracted for all items currently added as evidence in the case configuration file. Dependant
        # on the choice, the evidence is transcribed by the chosen ASR engine, which is called as the functions for
        # each ASR engine has been separated
        if userInput == "1":
            print("========================================================")
            userInput = input("Press 1 to use default model \n")
            print("========================================================")
            if userInput == "1":
                try:
                    # The audio is extracted for all items currently added as evidence in the case configuration file.
                    print("Extracting Audio from Evidence  - Please wait")
                    extractedAudio = ASREngine.extractAudio(self, CaseConfigFileName, CurrentCase)
                    print("Extracting Audio from Evidence Complete!")
                    casePath = Case.get_casePath(self, CurrentCase)
                    # Chosen ASR engine function is called.
                    kaldi(extractedAudio, CaseConfigFileName, casePath)
                except:
                    print("Evidence Audio Extraction/ Automated transcription ERROR!")
                    func_code = "404"
                    return func_code
            else:
                print("Invalid Selection Exiting Program")
                exit(0)
        else:
            if userInput == "2":
                print("Initialising default PocketSphinx model\n")
                try:
                    print("Extracting Audio from Evidence  - Please wait")
                    # Chosen ASR engine function is called.
                    extractedAudio = ASREngine.extractAudio(self, CaseConfigFileName, CurrentCase)
                    casePath = Case.get_casePath(self, CurrentCase)
                    # Chosen ASR engine function is called.
                    pocketSphinx(extractedAudio, CaseConfigFileName, casePath)
                except:
                    print("Program Error")
                    func_code = "404"
                    return func_code
            else:
                if userInput == "3":
                    # The audio is extracted for all items currently added as evidence in the case configuration file.
                    extractedAudio = ASREngine.extractAudio(self, CaseConfigFileName, CurrentCase)
                    # Case Path is retrieved as the case confuration file needs to be updated with the results of the
                    # transcripts
                    casePath = Case.get_casePath(self, CurrentCase)
                    # Chosen ASR engine function is called.
                    deepSpeech(extractedAudio, CaseConfigFileName, casePath)
                else:
                    # If selection is invalid, program will exit gracefully
                    print("Invalid Selection Exiting Program")
                    exit(0)