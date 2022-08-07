# Keyword Searching Function

def searchKeywords(keyword_list,transcription_text, start_time, end_time, evidenceItem):
    # Takes the transcript for the segment of evidence along with the start and end time and the keyword list.
    # Searches for keywords in the transcript and returns the keywords found along with the start and end time as a list
    # This will then be updated for that evidence object in the case configuration file
    keywordsFoundList = []
    for keyword in keyword_list:
        if keyword in transcription_text:
            keywordsFoundList.append(keyword + "|" + start_time + "-" + end_time)
            print("The keyword of " + keyword + " Found in " + evidenceItem + " between " + str(
                start_time) + " and " + str(end_time))
    return keywordsFoundList










