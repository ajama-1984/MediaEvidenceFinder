def search_Keywords (pathToFile, fileName, file_type,func_code, transcription_file,keywords):
    keyword_list = str(keywords).split(",")
    print(keyword_list)
    transcript = open(transcription_file, 'r')
    transcript_Lines = transcript.readlines()
    transcriptsStr = ''.join(transcript_Lines)
    print(transcriptsStr)

    for s in keyword_list:
        if s in transcriptsStr:
            print("Keyword " + s + " has been found in " + str(pathToFile))
        else:
            print("Keyword " + s + " NOT FOUND IN " + str(pathToFile))

    transcript.close()