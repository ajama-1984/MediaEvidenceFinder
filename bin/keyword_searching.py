import os
from configparser import ConfigParser
from datetime import datetime


def search_Keywords (CaseConfigFileName):
    keywords = input("Please provide Keywords - Separate keyword with a comma: \n")
    keyword_list = str(keywords).split(",")
    print(keyword_list)
    config = ConfigParser(strict=False)
    config['CaseConfiguration'] = {}
    config.read(CaseConfigFileName)
    config.set('CaseConfiguration', 'case_keywords', str(keyword_list))
    EvidenceList = (config.get('CaseConfiguration', 'evidenceidlist'))
    EvidenceList = EvidenceList.split(",")
    EvidenceList[:] = [x for x in EvidenceList if x]
    for evidenceItem in EvidenceList:
        keywordsContainedEvidence = []
        transcriptlocation = config.get(str(evidenceItem), 'transcriptlocation')
        transcript = open(transcriptlocation, 'r')
        transcript_Lines = transcript.readlines()
        transcriptsStr = ''.join(transcript_Lines)
        for s in keyword_list:
            if s in transcriptsStr:
                print("Keyword " + s + " has been found in " + str(transcriptlocation))
                keywordsContainedEvidence.append(s)
        transcript.close()
        # print(keywordsContainedEvidence)
        config.set(str(evidenceItem), 'keywords', str(keywordsContainedEvidence))
        now = datetime.now()
        modifiedDateTime = now.strftime("%m/%d/%Y, %H:%M:%S")
        config.set('CaseConfiguration', 'modifieddatetime', modifiedDateTime)
        with open(CaseConfigFileName, 'w') as configfile:
            config.write(configfile)

def searchKeywords(keyword_list,transcription_text, start_time, end_time, evidenceItem):
    keywordsFoundList = []
    for keyword in keyword_list:
        if keyword in transcription_text:
            keywordsFoundList.append(keyword + "|" + start_time + "-" + end_time)
            print("The keyword of " + keyword + " Found in " + evidenceItem + " between " + str(
                start_time) + " and " + str(end_time))
    return keywordsFoundList










