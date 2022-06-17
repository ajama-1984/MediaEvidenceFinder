from Case import Case
import os
from configparser import ConfigParser
from file_Identification_test import file_identification, list_files
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
            listfiles = list_files(evidenceFolderPath)
            file_ident = file_identification(evidenceFolderPath,listfiles)
            func_code = file_ident[0]
            files_identified = file_ident[1]
            return func_code, caseID, files_identified

    def processEvidence(self,caseID,caseFile,func_code,files_identified,CurrentCase):
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
                print("Adding Evidence to CASE configuration file")
                NumberOfEvidenceItems = Case.getNumberOfEvidenceItems(self,CurrentCase)
                config = ConfigParser(strict=False)
                NumberOfEvidenceItems = int(NumberOfEvidenceItems)
                updatedNumberOfEvidenceItems = str(NumberOfEvidenceItems + 1)
                EvidenceListName = str("Evidence" + updatedNumberOfEvidenceItems)
                listofEvidence = []
                config[EvidenceListName] = {}
                config['CaseConfiguration'] = {}
                EvidenceItemConfiguration = config[EvidenceListName]
                config.read(caseFile)
                for key, value in files_identified.items():
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
                    NumberOfEvidenceItems = int(NumberOfEvidenceItems)
                    updatedNumberOfEvidenceItems = str(NumberOfEvidenceItems + 1)
                    print(evidenceFileName)
                    print(NumberOfEvidenceItems)
                    EvidenceItemConfiguration['evidenceID'] = updatedNumberOfEvidenceItems
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
                    EvidenceIDList = str(listofEvidence.append(EvidenceListName))
                    print(EvidenceIDList)
                    config.set('CaseConfiguration', 'NumberOfEvidenceItems',updatedNumberOfEvidenceItems)
                    config.set('CaseConfiguration', 'EvidenceIDList', EvidenceIDList)
                    with open(caseFile, 'w') as configfile:
                        config.write(configfile)
                        func_code = "200"
                        return func_code
            else:
                if import_check == "No" or "no" or "n":
                    print("The Files have not been imported as evidence")
                else:
                    print("Invalid Selection Exiting the Program")
                    exit(0)

    def evidenceFuncCodeCheck (self,currentEvidence):
        func_code = currentEvidence[0]
        return func_code