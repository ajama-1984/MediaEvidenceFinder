import os
from os.path import expanduser
from configparser import ConfigParser
from datetime import datetime
from tkinter import *
from tkinter import filedialog


class Case:
    def __init__(self, caseID, CaseConfigName, caseName, caseDescription, investigator, createdDateTime,
                 ModifiedDateTime, NumberOfEvidenceItems, EvidenceIDList, ReportPath, case_Keywords, casePath):
        self.caseID = caseID
        self.caseName = caseName
        self.caseDescription = caseDescription
        self.investigator = investigator
        self.createdDateTime = createdDateTime
        self.CaseConfigName = CaseConfigName
        self.casePath = casePath
        self.ModifiedDateTime = ModifiedDateTime
        self.NumberOfEvidenceItems = NumberOfEvidenceItems
        self.EvidenceIDList = EvidenceIDList
        self.ReportPath = ReportPath
        self.case_Keywords = case_Keywords

    def createCase(self):
        caseID = input("Provide CaseID: \n")
        caseName = input("Provide Name: \n")
        caseDescription = input("Provide Case Description: \n")
        investigator = input("Enter Name of Investigator: \n")
        CaseConfigName = input("Enter name of case configuration file: \n")
        ModifiedDateTime = "null"
        NumberOfEvidenceItems = "0"
        EvidenceIDList = ' '
        ReportPath = ""
        case_Keywords = ""
        parent_dir = expanduser("~")
        workingDir = "MediaEvidenceFinder\\" + CaseConfigName
        casePath = os.path.join(parent_dir, workingDir)
        if os.path.exists(casePath):
            print("Case Folder already exists")
            func_code = "409"
            print(func_code)
            return func_code
        else:
            print(
                "A case with the following settings will be created \n" + "CaseID: " + caseID + "\nName of Case: " + caseName + "\nDescription of Case: " + caseDescription + "\nName of Investigator: " + investigator + "\nName of Case Configuration File: " + CaseConfigName)

            os.makedirs(casePath)
            now = datetime.now()  # current date and time
            CreatedTime = now.strftime("%m/%d/%Y, %H:%M:%S")
            config = ConfigParser()
            config['CaseConfiguration'] = {}
            CaseConfiguration = config['CaseConfiguration']
            CaseConfiguration['caseID'] = caseID
            CaseConfiguration['caseName'] = caseName
            CaseConfiguration['caseDescription'] = caseDescription
            CaseConfiguration['investigator'] = investigator
            CaseConfiguration['CaseConfigName'] = CaseConfigName
            CaseConfiguration['casePath'] = casePath
            CaseConfiguration['CreatedTime'] = CreatedTime
            CaseConfiguration['ModifiedDateTime'] = ModifiedDateTime
            CaseConfiguration['NumberOfEvidenceItems'] = NumberOfEvidenceItems
            CaseConfiguration['EvidenceIDList'] = EvidenceIDList
            CaseConfiguration['ReportPath'] = ReportPath
            CaseConfiguration['case_Keywords'] = case_Keywords
            caseconfigFullFileName = CaseConfigName + '.CASE'
            caseconfigFullFilePath = casePath + "\\" + caseconfigFullFileName
            print (caseconfigFullFilePath)
            print(caseconfigFullFileName)
            os.chdir(casePath)
            os.mkdir("Transcripts")
            os.mkdir("Reports")
            os.mkdir("ExtractedAudioFiles")
            os.mkdir("AudioChunks")
            with open(caseconfigFullFileName, 'w') as configfile:
                config.write(configfile)
                func_code = "200"

            configDict = dict()
            configDict.update({"caseID":caseID})
            configDict.update({"caseName": caseName})
            configDict.update({"caseDescription": caseDescription})
            configDict.update({"CaseConfigName": CaseConfigName})
            configDict.update({"investigator": investigator})
            configDict.update({"casePath": casePath})
            configDict.update({"CreatedTime": CreatedTime})
            configDict.update({"ModifiedDateTime": ModifiedDateTime})
            configDict.update({"NumberOfEvidenceItems": NumberOfEvidenceItems})
            configDict.update({"evidenceidlist": EvidenceIDList})
            configDict.update({"ReportPath": ReportPath})
            configDict.update({"case_Keywords": case_Keywords})
            return func_code, configDict, caseconfigFullFilePath

    def openCase(self):
        userpath = input ("Please provide path to .CASE Config file \n")
        userpath = userpath.replace('"','')
        config = ConfigParser()
        config['CaseConfiguration'] = {}
        caseFile = os.path.normpath(userpath)
        filename, extension = (os.path.splitext(caseFile))
        file_exists = os.path.exists(caseFile)
        if extension == ".CASE" and file_exists == True:
            config.read(caseFile)
            caseID = (config.get('CaseConfiguration','caseID'))
            caseName = (config.get('CaseConfiguration', 'caseName'))
            caseDescription = (config.get('CaseConfiguration', 'caseDescription'))
            investigator = (config.get('CaseConfiguration', 'investigator'))
            CaseConfigName = (config.get('CaseConfiguration', 'CaseConfigName'))
            casePath = (config.get('CaseConfiguration', 'casePath'))
            CreatedTime = (config.get('CaseConfiguration', 'CreatedTime'))
            ModifiedDateTime = (config.get('CaseConfiguration', 'ModifiedDateTime'))
            NumberOfEvidenceItems = (config.get('CaseConfiguration', 'NumberOfEvidenceItems'))
            EvidenceIDList = (config.get('CaseConfiguration', 'evidenceidlist'))
            ReportPath = (config.get('CaseConfiguration', 'ReportPath'))
            case_Keywords = (config.get('CaseConfiguration', 'case_Keywords'))
            configDict = dict()

            configDict.update({"caseID":caseID})
            configDict.update({"caseName": caseName})
            configDict.update({"caseDescription": caseDescription})
            configDict.update({"CaseConfigName": CaseConfigName})
            configDict.update({"investigator": investigator})
            configDict.update({"casePath": casePath})
            configDict.update({"CreatedTime": CreatedTime})
            configDict.update({"ModifiedDateTime": ModifiedDateTime})
            configDict.update({"NumberOfEvidenceItems": NumberOfEvidenceItems})
            configDict.update({"evidenceidlist": EvidenceIDList})
            configDict.update({"ReportPath": ReportPath})
            configDict.update({"case_Keywords": case_Keywords})
            print(configDict)
            func_code = "200"
            return func_code,configDict,caseFile
        else:
            print("Invalid Case Config File")
            func_code = "404"
            return func_code

    def get_caseID(self,currentCase):
        caseDetails = currentCase[1]
        caseID = caseDetails['caseID']
        return caseID

    def get_caseName(self,currentCase):
        caseDetails = currentCase[1]
        caseName = caseDetails['caseName']
        return caseName

    def get_caseDescription(self,currentCase):
        caseDetails = currentCase[1]
        caseDescription = caseDetails['caseDescription']
        return caseDescription

    def get_CaseConfigName(self,currentCase):
        caseDetails = currentCase[1]
        CaseConfigName = caseDetails['CaseConfigName']
        return CaseConfigName

    def get_investigator(self,currentCase):
        caseDetails = currentCase[1]
        investigator = caseDetails['investigator']
        return investigator

    def get_casePath(self,currentCase):
        caseDetails = currentCase[1]
        casePath = caseDetails['casePath']
        return casePath

    def get_CreatedTime(self,currentCase):
        caseDetails = currentCase[1]
        CreatedTime = caseDetails['CreatedTime']
        return CreatedTime

    def get_ModifiedDateTime(self,currentCase):
        caseDetails = currentCase[1]
        ModifiedDateTime = caseDetails['ModifiedDateTime']
        return ModifiedDateTime

    def getCaseConfigFileName (self, currentCase):
        caseConfigFileName = currentCase[2]
        return caseConfigFileName

    def getNumberOfEvidenceItems (self, currentCase):
        caseDetails = currentCase[1]
        NumberOfEvidenceItems = caseDetails['NumberOfEvidenceItems']
        return NumberOfEvidenceItems

    def getEvidenceIDList (self,currentCase):
        caseDetails = currentCase[1]
        EvidenceIDList = caseDetails['evidenceidlist']
        return EvidenceIDList

    def getReportPath (self,currentCase):
        caseDetails = currentCase[1]
        ReportPath = caseDetails['ReportPath']
        return ReportPath

    def getcase_Keywords (self,currentCase):
        caseDetails = currentCase[1]
        case_Keywords = caseDetails['case_Keywords']
        return case_Keywords

    def caseFuncCodeCheck (self,currentCase):
        func_code = currentCase[0]
        return func_code


