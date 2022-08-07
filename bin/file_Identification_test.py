# File identification Functions
import os
import exiftool
import hashlib
from datetime import datetime

def list_files(EvidencePath):

    evidenceList = []
    for root, dirs, files in os.walk(EvidencePath):
        for name in files:
            evidenceList.append(os.path.join(root, name))
    return evidenceList

def file_identification(EvidencePath, evidenceList):
    dbdict = dict()
    if os.path.exists(EvidencePath):
        for filename in evidenceList:
            file_sha1_hash = hashlib.sha1(open(filename,'rb').read()).hexdigest()
            with exiftool.ExifToolHelper() as et:
                metadata = et.get_metadata(filename)
                for d in metadata:
                    sourceFile = d.get("File:FileName")
                    sourceFileDirectory = d.get("File:Directory")
                    FileSize = d.get("File:FileSize")
                    FileModifyDate = d.get("File:FileModifyDate")
                    FileAccessDate = d.get("File:FileAccessDate")
                    FileCreateDate = d.get("File:FileCreateDate")
                    FileType = d.get("File:FileType")
                    MIMEType = d.get("File:MIMEType")
                    FileExtension = d.get("FileTypeExtension")
                    now = datetime.now()
                    ImportedTime = now.strftime("%m/%d/%Y, %H:%M:%S")
                    if str(MIMEType).__contains__("audio") or str(MIMEType).__contains__("video"):
                        file_properties = str(MIMEType) + "|" + str(sourceFile) + "|" + str(sourceFileDirectory) + "|" + str(FileSize) + "|" + str(FileModifyDate) + "|" + str(FileAccessDate) + "|" + str(FileCreateDate) + "|" + str(FileType) + "|" + str(FileExtension) + "|" + file_sha1_hash + "|" + ImportedTime
                        dbdict.update({filename:file_properties})
        func_code = "200"
        return func_code, dbdict
    else:
        func_code = "404"
        return func_code
