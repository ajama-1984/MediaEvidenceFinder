import self as self
from file_Identification import identify_file
from audio_extraction import extract_audio_from_source
# from CMUsphinx_speech2text import pocketsphinx_S2T
# from keyword_searching import search_Keywords
from Case import Case
from evidence import Evidence

if __name__ == '__main__':
    userChoice = input("Press 1 for New Case or 2 to open an existing Case \n")
    if userChoice == "1":
        CurrentCase = Case.createCase(self)
        print(CurrentCase)
        userChoice = input("Press 1 to add and process evidence \n")
        if userChoice == "1":
            evidenceToProcess = Evidence.selectEvidence(self)
    else:
        if userChoice == "2":
            CurrentCase = Case.openCase(self)
            print(CurrentCase)
            evidenceToProcess = Evidence.selectEvidence(self)
        else:
            print("Invalid Selection - Exiting Program")