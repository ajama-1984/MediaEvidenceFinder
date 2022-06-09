from Case import Case
import os
from file_Identification import identify_file
class Evidence(Case):
    def __init__(self,fileID, fileName, fileType, caseID, filePath, transcriptPath, fileModifiedDateTime, ASREngine, ASRModel):
        self.fileName = fileName
        self.fileID = fileID
        self.fileType = fileType
        self.selfcaseID = caseID
        self.filePath = filePath
        self.transcriptPath = transcriptPath
        self.fileModifiedDateTime = fileModifiedDateTime
        self.ASREngine = ASREngine
        self.ASRModel = ASRModel

    def selectEvidence(self,caseID):
        # TO-DO - GET E01 LIBRARY INTEGRATED
        evidenceFolderUsrPath = input ("Provide Folder to Evidnece \n")
        evidenceFolderPath = os.path.normpath(evidenceFolderUsrPath)
        if os.path.exists(evidenceFolderPath):
            print("Path Valid")
            fileIdentification = identify_file(evidenceFolderPath)
            print(fileIdentification)














