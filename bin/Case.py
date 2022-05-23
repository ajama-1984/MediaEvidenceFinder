import os
from os.path import expanduser
from configparser import ConfigParser
from datetime import datetime
from tkinter import *
from tkinter import filedialog


class Case:
    def __init__(self, caseID, CaseConfigName, caseName, caseDescription, investigator, createdDateTime,
                 ModifiedDateTime, casePath):
        self.caseID = caseID
        self.caseName = caseName
        self.caseDescription = caseDescription
        self.investigator = investigator
        self.createdDateTime = createdDateTime
        self.CaseConfigName = CaseConfigName
        self.casePath = casePath
        self.ModifiedDateTime = ModifiedDateTime

    def createCase(self):
        caseID = input("Provide CaseID: \n")
        caseName = input("Provide Name: \n")
        caseDescription = input("Provide Case Description: \n")
        investigator = input("Enter Name of Investigator: \n")
        CaseConfigName = input("Enter name of case configuration file: \n")
        ModifiedDateTime = "null"
        parent_dir = expanduser("~")
        workingDir = "MediaEvidenceFinder\\" + CaseConfigName
        casePath = os.path.join(parent_dir, workingDir)
        if os.path.exists(casePath):
            print("Case Folder already exists")
        else:
            print(
                "A case with the following settings will be created \n" + caseID + " " + caseName + " " + caseDescription + " " + investigator + " " + CaseConfigName)
            os.makedirs(casePath)
            now = datetime.now()  # current date and time
            currentDate_time = now.strftime("%m/%d/%Y, %H:%M:%S")
            config = ConfigParser()
            config['CaseConfiguration'] = {}
            CaseConfiguration = config['CaseConfiguration']
            CaseConfiguration['caseID'] = caseID
            CaseConfiguration['caseName'] = caseName
            CaseConfiguration['caseDescription'] = caseDescription
            CaseConfiguration['investigator'] = investigator
            CaseConfiguration['CaseConfigName'] = CaseConfigName
            CaseConfiguration['casePath'] = casePath
            CaseConfiguration['CreatedTime'] = currentDate_time
            CaseConfiguration['ModifiedDateTime'] = ModifiedDateTime

            caseconfigFullFileName = CaseConfigName + '.CASE'
            print(caseconfigFullFileName)
            os.chdir(casePath)
            os.mkdir("Transcripts")
            os.mkdir("Reports")
            os.mkdir("ExtractedAudioFiles")
            with open(caseconfigFullFileName, 'w') as configfile:
                config.write(configfile)
                func_code = "200"

            return func_code, caseID, CaseConfigName, caseName, caseDescription, investigator, currentDate_time, ModifiedDateTime, casePath

    def openCase(self):
        case_file_extensions = ['*.CASE']
        # ftypes = [
        #     ('Case Config files', case_file_extensions),
        #     ('All files', '*'),
        # ]
        # userpath = filedialog.askopenfilename(title="Select file", filetypes=ftypes)
        userpath = input ("Please provide path to .CASE Config file \n")
        config = ConfigParser()
        config['CaseConfiguration'] = {}
        caseFile = os.path.normpath(userpath)
        #print(caseFile)
        filename, extension = (os.path.splitext(caseFile))
        if extension == ".CASE":
            config.read(caseFile)
            #print(config.sections())
            caseID = (config.get('CaseConfiguration','caseID'))
            caseName = (config.get('CaseConfiguration', 'caseName'))
            caseDescription = (config.get('CaseConfiguration', 'caseDescription'))
            investigator = (config.get('CaseConfiguration', 'investigator'))
            CaseConfigName = (config.get('CaseConfiguration', 'CaseConfigName'))
            casePath = (config.get('CaseConfiguration', 'casePath'))
            CreatedTime = (config.get('CaseConfiguration', 'CreatedTime'))
            ModifiedDateTime = (config.get('CaseConfiguration', 'ModifiedDateTime'))

            configDict = dict()

            #TO-DO - FOR LOOP FOR ALL CASE ITEMS
            configDict.update({"caseID":caseID})
            configDict.update({"caseName": caseName})
            configDict.update({"caseDescription": caseDescription})
            configDict.update({"CaseConfigName": CaseConfigName})
            configDict.update({"investigator": investigator})
            configDict.update({"casePath": casePath})
            configDict.update({"CreatedTime": CreatedTime})
            configDict.update({"ModifiedDateTime": ModifiedDateTime})

            # print(configDict)
            #
            # print(caseID + "\n" + caseName + "\n" + caseDescription + "\n" + investigator + "\n" + CaseConfigName + "\n" + casePath + "\n" +CreatedTime + "\n" + ModifiedDateTime)

            #OpenedCase = Case.__init__(self,caseID,CaseConfigName,caseName,caseDescription, investigator,CreatedTime,ModifiedDateTime,casePath)

            func_code = "200"

            return func_code,configDict
        else:
            print("Invalid Case Config File")
            func_code = "404"
            return func_code
