import path
import magic
from pathlib import Path
import glob, os

def identify_file():
    pathToFolder = input("Please provide folder containing evidence:")
    if os.path.exists(pathToFolder):
        os.chdir(pathToFolder)
        for file in glob.glob():
                fileName = Path(file).name
                mime = magic.Magic(mime=True)
                file_type = mime.from_file(file)
                if str(file_type).__contains__("audio") or str(file_type).__contains__("video"):
                    func_code = "200"
                    return fileName,file_type,func_code
                else:
                    func_code = "422"
                    pathToFolder, fileName, file_type, func_code
        else:
            func_code = "404"
            return func_code