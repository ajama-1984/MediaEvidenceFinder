# Evidence Class and functions

from Case import Case
import os
from configparser import ConfigParser
from file_Identification_test import file_identification, list_files
from halo import Halo
import time
class Evidence(Case):
    def __init__(self,fileID, fileName, fileType, caseID, filePath, transcriptPath, fileModifiedDateTime, ASREngine, ASRModel):
        self.fileName = fileName
        self.fileID = fileID
        self.fileType = fileType
        self.caseID = caseID
        self.filePath = filePath
        self.transcriptPath = transcriptPath
        self.fileModifiedDateTime = fileModifiedDateTime
        self.ASREngine = ASREngine
        self.ASRModel = ASRModel

    def selectEvidence(self,caseID):
        evidenceFolderUsrPath = input ("Provide Folder to Evidence \n")
        evidenceFolderPath = os.path.normpath(evidenceFolderUsrPath)
        if os.path.exists(evidenceFolderPath):
            print("Path Valid")
            with Halo(text='Finding Media Files. Please Wait!', spinner='dots'):
                listfiles = list_files(evidenceFolderPath)
                file_ident = file_identification(evidenceFolderPath,listfiles)
                func_code = file_ident[0]
                files_identified = file_ident[1]
                return func_code, caseID, files_identified

    def processEvidence(self,caseFile,func_code,files_identified,CurrentCase):
        if files_identified is not None and func_code == "200":
            print("Looking for Media files - Please Wait")
            print("========================================================")
            print("The following Media files were detected and will be imported as evidence")
            print("======================================================== ")
            for key, value in files_identified.items():
                identifiedItem = key
                identifiedItemproperties = str(value)
                identifiedItemAttribute = identifiedItemproperties.split('|')
                identifiedItemFileName = identifiedItemAttribute[1]
                print(identifiedItemFileName)
            print("========================================================")
            import_check = input("Proceed with Importing the above files as Evidence - Yes or No? \n")
            if import_check == "Yes" or "y" or "yes":
                with Halo(text='Adding detected files to case. Please Wait! \n', spinner='dots'):
                    time.sleep(5)
                    NumberOfEvidenceItems = Case.getNumberOfEvidenceItems(self,CurrentCase)
                    config = ConfigParser(strict=False)
                    config.read(caseFile)
                    listEvidence = Case.getEvidenceIDList(self, CurrentCase)
                    listEvidence = listEvidence.split(",")
                    for key, value in files_identified.items():
                        ExistingEvidencelist = Case.getEvidenceIDList(self, CurrentCase)
                        NumberOfEvidenceItems = int(NumberOfEvidenceItems)
                        NumberOfEvidenceItems += 1
                        # print(NumberOfEvidenceItems)
                        EvidenceListName = "Evidence" + str(NumberOfEvidenceItems)
                        # print(EvidenceListName)
                        listEvidence.append(EvidenceListName)
                        config[EvidenceListName] = {}
                        EvidenceItemConfiguration = config[EvidenceListName]
                        evidenceItem = key
                        Evidenceproperties = str(value)
                        EvidenceAttribute = Evidenceproperties.split('|')
                        evidencemimeType = EvidenceAttribute[0]
                        evidenceFileName = EvidenceAttribute[1]
                        evidenceFilePath = EvidenceAttribute[2]
                        evidenceFileSize = EvidenceAttribute[3]
                        evidenceFileCreationTime = EvidenceAttribute[4]
                        evidenceFileAccessedTime = EvidenceAttribute[5]
                        evidenceFileModifiedTime = EvidenceAttribute[6]
                        evidenceFileExtension = EvidenceAttribute[7]
                        evidenceFileHash = EvidenceAttribute[9]
                        evidenceAddedDateTime = EvidenceAttribute[10]

                        # print(evidenceFileName)
                        strNumberOfEvidenceItems = str(NumberOfEvidenceItems)

                        EvidenceItemConfiguration['evidenceID'] = strNumberOfEvidenceItems
                        EvidenceItemConfiguration['evidenceItem'] = evidenceItem
                        EvidenceItemConfiguration['evidencemimeType'] = evidencemimeType
                        EvidenceItemConfiguration['evidenceFileName'] = evidenceFileName
                        EvidenceItemConfiguration['evidenceFilePath'] = evidenceFilePath
                        EvidenceItemConfiguration['evidenceFileSize'] = evidenceFileSize
                        EvidenceItemConfiguration['evidenceFileCreationTime'] = evidenceFileCreationTime
                        EvidenceItemConfiguration['evidenceFileAccessedTime'] = evidenceFileAccessedTime
                        EvidenceItemConfiguration['evidenceFileModifiedTime'] = evidenceFileModifiedTime
                        EvidenceItemConfiguration['evidenceFileExtension'] = evidenceFileExtension
                        EvidenceItemConfiguration['evidenceFileHash'] = evidenceFileHash
                        EvidenceItemConfiguration['evidenceAddedDateTime'] = evidenceAddedDateTime
                        EvidenceItemConfiguration['aSRTranscription_Engine_Used'] = ""
                        EvidenceItemConfiguration['aSRTranscription_Model_Used'] = ""
                        EvidenceItemConfiguration['transcriptLocation'] = ""

                        config.get('CaseConfiguration', 'numberofevidenceitems')
                        config.set('CaseConfiguration', 'numberofevidenceitems', strNumberOfEvidenceItems)
                        addedEvidence = ','.join(str(x) for x in listEvidence)
                        config.get('CaseConfiguration', 'evidenceidlist')
                        config.set('CaseConfiguration', 'evidenceidlist', addedEvidence)
                    with open(caseFile, 'w') as configfile:
                        config.write(configfile)
                        func_code = "200"
                        print("Detected Media Files added as Evidence")
                        return func_code
            else:
                if import_check == "No" or "no" or "n":
                    print("The Files have not been imported as evidence")
                else:
                    print("Invalid Selection Exiting the Program")
                    exit(0)


    def retrieveEvidence (self, CaseConfigFileName, currentCase):
        config = ConfigParser(strict=False)
        config['CaseConfiguration'] = {}
        config.read(CaseConfigFileName)
        EvidenceList = (config.get('CaseConfiguration', 'evidenceidlist'))
        EvidenceList = EvidenceList.split(",")
        EvidenceList[:] = [x for x in EvidenceList if x]
        for evidenceItem in EvidenceList:
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

            print("Evidence ID: " + evidenceid)
            print("Evidence Source Full Path: " + evidenceitem)
            print("Evidence MIME Type: " + evidencemimetype)
            print("Evidence File Name: " + evidencefilename)
            print("Evidence Source Folder: " + evidencefilepath)
            print("Evidence File Size: " + evidencefilesize)
            print("Evidence Created on: " + evidencefilecreationtime)
            print("Evidence Last Accessed: " + evidencefileaccessedtime)
            print("Evidence Last Modified: " + evidencefilemodifiedtime)
            print("Evidence File Extension: " + evidencefileextension)
            print("Evidence File Hash (SHA-1): " + evidencefilehash)
            print("Evidence Added on: " + evidenceaddeddatetime)
            print("========================================================")

    def evidenceFuncCodeCheck (self,currentEvidence):
        func_code = currentEvidence[0]
        return func_code