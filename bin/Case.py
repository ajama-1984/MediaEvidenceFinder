import os
from os.path import expanduser
from configparser import ConfigParser
from datetime import datetime
from tkinter import *
from tkinter import filedialog
class Case:
    def __init__(self, caseID ,CaseConfigName, caseName, caseDescription, investigator,createdDateTime,ModifiedDateTime):
        self.caseID = caseID
        self.caseName = caseName
        self.caseDescription = caseDescription
        self.investigator = investigator
        self.createdDateTime = createdDateTime
        self.CaseConfigName = CaseConfigName
        self.ModifiedDateTime = ModifiedDateTime
    def createCase (self):
        caseID = input("Provide CaseID: \n")
        caseName = input("Provide Name: \n")
        caseDescription = input("Provide Case Description: \n")
        investigator = input("Enter Name of Investigator: \n")
        CaseConfigName = input("Enter name of case configuration file: \n")
        parent_dir = expanduser("~")
        workingDir = "MediaEvidenceFinder"
        path = os.path.join(parent_dir, workingDir)
        if os.path.exists(path):
            for filename in os.listdir(path):
                if CaseConfigName in filename:
                    print("Case Config File already exists")
                else:
                    print("A case with the following settings will be created \n" + caseID + " " + caseName + " " + caseDescription + " " + investigator + " " + CaseConfigName)
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
                    CaseConfiguration['CreatedTime'] = currentDate_time
                    CaseConfiguration['ModifiedDateTime'] = 'null'
                    caseconfigFullFileName = CaseConfigName + '.ini'
                    print(caseconfigFullFileName)
                    os.chdir(path)
                    with open(caseconfigFullFileName, 'w') as configfile:
                        config.write(configfile)
                    return Case
        else:
            print("A case with the following settings will be created \n"  + caseID + " " + caseName + " " + caseDescription + " " + investigator + " " + CaseConfigName)
            os.mkdir(path)
            now = datetime.now()  # current date and time
            currentDate_time = now.strftime("%m/%d/%Y, %H:%M:%S")
            config = ConfigParser()
            config['CaseConfiguration'] = {}
            CaseConfiguration= config['CaseConfiguration']
            CaseConfiguration['caseID'] = caseID
            CaseConfiguration['caseName'] = caseName
            CaseConfiguration['caseDescription'] = caseDescription
            CaseConfiguration['investigator'] = investigator
            CaseConfiguration['CaseConfigName'] = CaseConfigName
            CaseConfiguration['CreatedTime'] = currentDate_time
            CaseConfiguration['ModifiedDateTime'] = 'null'
            caseconfigFullFileName = CaseConfigName + '.ini'
            print(caseconfigFullFileName)
            os.chdir(path)
            with open(caseconfigFullFileName,'w') as configfile:
                config.write(configfile)
            return Case

    def openCase(self):
        path = filedialog.askopenfilename()
        print(path)




