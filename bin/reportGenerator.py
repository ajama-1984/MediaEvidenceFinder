from fpdf import FPDF
from configparser import ConfigParser
import os
from Case import *


def generateReport(CaseConfigFile):
    print("Generating Report")
    config = ConfigParser()
    config['CaseConfiguration'] = {}
    caseFile = os.path.normpath(CaseConfigFile)
    filename, extension = (os.path.splitext(caseFile))
    file_exists = os.path.exists(caseFile)
    if extension == ".CASE" and file_exists == True:
        config.read(caseFile)
        caseID = str(config.get('CaseConfiguration', 'caseID'))
        caseName = str(config.get('CaseConfiguration', 'caseName'))
        caseDescription = str(config.get('CaseConfiguration', 'caseDescription'))
        investigator = str(config.get('CaseConfiguration', 'investigator'))
        CaseConfigName = str(config.get('CaseConfiguration', 'CaseConfigName'))
        casePath = str(config.get('CaseConfiguration', 'casePath'))
        CreatedTime = str(config.get('CaseConfiguration', 'CreatedTime'))
        ModifiedDateTime = str(config.get('CaseConfiguration', 'ModifiedDateTime'))
        NumberOfEvidenceItems = str(config.get('CaseConfiguration', 'NumberOfEvidenceItems'))
        EvidenceIDList = str(config.get('CaseConfiguration', 'evidenceidlist'))
        case_Keywords = config.get('CaseConfiguration', 'case_Keywords')

        reportPDF = FPDF('P','mm','A4')
        reportPDF.add_page()
        reportPDF.set_font('helvetica','', 18)
        reportPDF.cell(30,10,"Case Information", ln=True)
        reportPDF.set_font('helvetica', '', 12)
        reportPDF.cell(0, 5, "Case ID - " + caseID, ln=True)
        reportPDF.cell(0, 5, "Case Name - " + caseName, ln=True)
        reportPDF.cell(0, 5, "Case Description - " + caseDescription, ln=True)
        reportPDF.cell(0, 5, "Investigator Name - " + investigator, ln=True)
        reportPDF.cell(0, 5, "Case Configuration Filename - " + CaseConfigName, ln=True)
        reportPDF.cell(0, 5, "Case Folder Path - " + casePath, ln=True)
        reportPDF.cell(0, 5, "Case Creation Date & Time - " + CreatedTime, ln=True)
        reportPDF.cell(0, 5, "Case Last Modified Date & Time  - " + ModifiedDateTime, ln=True)
        reportPDF.cell(0, 5, "Number of Evidence Contained in Case - " + NumberOfEvidenceItems, ln=True)
        reportPDF.cell(0, 5, "List of Evidence ID's: ", ln=True)
        reportPDF.multi_cell(0,5,EvidenceIDList)
        reportPDF.cell(0, 5, "Keywords of Case - " + case_Keywords, ln=True)
        reportPDF.line(10, 75, 195, 75)

        EvidenceList = (config.get('CaseConfiguration', 'evidenceidlist'))
        EvidenceList = EvidenceList.split(",")
        EvidenceList[:] = [x for x in EvidenceList if x]
        for evidenceItem in EvidenceList:
            reportPDF.add_page()
            evidenceid = config.get(str(evidenceItem), 'evidenceid')
            evidenceitem = config.get(str(evidenceItem), 'evidenceitem')
            evidencemimetype = config.get(str(evidenceItem), 'evidencemimetype')
            evidencefilename = config.get(str(evidenceItem),'evidencefilename')
            evidencefilepath = config.get(str(evidenceItem), 'evidencefilepath')
            evidencefilesize = config.get(str(evidenceItem), 'evidencefilesize')
            evidencefilecreationtime = config.get(str(evidenceItem), 'evidencefilecreationtime')
            evidencefileaccessedtime = config.get(str(evidenceItem), 'evidencefileaccessedtime')
            evidencefilemodifiedtime = config.get(str(evidenceItem), 'evidencefilemodifiedtime')
            evidencefileextension = config.get(str(evidenceItem), 'evidencefileextension')
            evidencefilehash = config.get(str(evidenceItem), 'evidencefilehash')
            evidenceaddeddatetime = config.get(str(evidenceItem), 'evidenceaddeddatetime')
            asrtranscription_engine_used = config.get(str(evidenceItem), 'asrtranscription_engine_used')
            asrtranscription_model_used = config.get(str(evidenceItem), 'asrtranscription_model_used')
            transcriptlocation = config.get(str(evidenceItem), 'transcriptlocation')
            keywordslist = config.get(str(evidenceItem), 'keywords')




            if "DeepSpeech" in asrtranscription_model_used:
                ASRDetails = asrtranscription_model_used.split(" ")
                asrtranscription_engine_used = ASRDetails[0]
                asrtranscription_model_used = ASRDetails[1]
                asrtranscription_engine_used = os.path.basename(asrtranscription_engine_used)
                asrtranscription_model_used = os.path.basename(asrtranscription_model_used)


            reportPDF.set_font('helvetica', '', 18)
            reportPDF.cell(30, 10, evidenceItem, ln=True)
            reportPDF.set_font('helvetica', '', 12)
            reportPDF.cell(0, 5, "Evidence ID - " + evidenceid, ln=True)
            reportPDF.cell(0, 5, "Evidence Source Full Path - " + evidenceitem, ln=True)
            reportPDF.cell(0, 5, "Evidence MIME Type - " + evidencemimetype, ln=True)
            reportPDF.cell(0, 5, "Evidence File Name - " + evidencefilename, ln=True)
            reportPDF.cell(0, 5, "Evidence Source Folder - " + evidencefilepath, ln=True)
            reportPDF.cell(0, 5, "Evidence File Size - " + evidencefilesize + " bytes", ln=True)
            reportPDF.cell(0, 5, "Evidence Created on - " + evidencefilecreationtime, ln=True)
            reportPDF.cell(0, 5, "Evidence Last Accessed - " + evidencefileaccessedtime, ln=True)
            reportPDF.cell(0, 5, "Evidence Last Modified - " + evidencefilemodifiedtime, ln=True)
            reportPDF.cell(0, 5, "Evidence File Extension - " + evidencefileextension, ln=True)
            reportPDF.cell(0, 5, "Evidence File Hash - " + evidencefilehash, ln=True)
            reportPDF.cell(0, 5, "Evidence added to case on - " + evidenceaddeddatetime, ln=True)
            reportPDF.cell(0, 5, "ASR Engine utilised to generate transcript - " + asrtranscription_engine_used, ln=True)
            reportPDF.cell(0, 5, "ASR Model utilised to generate transcript - " + asrtranscription_model_used, ln=True)
            reportPDF.cell(0, 5, "Transcript File Location - ", ln=True)
            reportPDF.multi_cell(0, 5, transcriptlocation)
            reportPDF.cell(0, 5, "Keywords Identified: ", ln=True)
            keywordslist = keywordslist.replace("[","")
            keywordslist = keywordslist.replace("]", "")
            keywordslist = keywordslist.split(",")
            for keyword in keywordslist:
                if keyword is not None and len(keyword.split("|")) == 2:
                    word,timeframe = keyword.split("|")
                    start,end = timeframe.split("-")
                    reportPDF.multi_cell(0, 5,
                                         "Keyword of " + str(word) + " was detected in the audio of " + evidencefilename + " file between " + str(start) + " and " + str(end))
                else:
                    word = keyword.split("|")
                    reportPDF.multi_cell(0, 5,
                                         "None of the Case Keywords were found in " + evidencefilename)

            reportPDF.set_font('helvetica', '', 18)
            reportPDF.cell(10, 10, "Transcript of " + evidenceItem, ln=True)
            reportPDF.set_font('helvetica', '', 12)
            transcriptFile = open(transcriptlocation, "r")
            for line in transcriptFile:
                cleanedLine = line.rstrip()
                reportPDF.multi_cell(0, 5, txt=cleanedLine)
    reportPath = casePath + "\\Reports\\" + CaseConfigName + " Report" + ".pdf"
    reportPDF.output(reportPath)
    now = datetime.now()
    modifiedDateTime = now.strftime("%m/%d/%Y, %H:%M:%S")
    config.set('CaseConfiguration', 'modifieddatetime', modifiedDateTime)
    config.set('CaseConfiguration', 'ReportPath', reportPath)
    with open(CaseConfigFile, 'w') as configfile:
        config.write(configfile)
    print("Report has been generated. Report Path: \n" + reportPath)


