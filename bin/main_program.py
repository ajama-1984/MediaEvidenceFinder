import self as self

from file_Identification import identify_file
from audio_extraction import extract_audio_from_source
# from CMUsphinx_speech2text import pocketsphinx_S2T
# from keyword_searching import search_Keywords
from Case import Case

if __name__ == '__main__':
    userChoice = input("Press 1 for New Case or 2 to open an existing Case")
    if userChoice == "1":
        Case.createCase(self)



    #identification = identify_file()
    #extract_audio_from_source(identification[0],identification[1])