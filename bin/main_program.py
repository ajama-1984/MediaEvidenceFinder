from file_Identification import identify_file
from audio_extraction import extract_audio_from_source
from pocketsphinx_speech2text import pocketsphinx_S2T
from keyword_searching import search_Keywords


if __name__ == '__main__':
    identify_file()
    