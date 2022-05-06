import path
import magic
from pathlib import Path
import glob, os

def identify_file():
    dbdict = {}
    pathToFolder = input("Please provide folder containing evidence:")
    if os.path.exists(pathToFolder):
        print("Path Exists")
        for filename in os.scandir(pathToFolder):
            file_name = filename.path
            mime = magic.Magic(mime=True)
            file_type = mime.from_file(file_name)
            if str(file_type).__contains__("audio") or str(file_type).__contains__("video"):
                dbdict.update({file_name:file_type})
        func_code = "200"
        print(dbdict)
        print(func_code)
        return func_code,dbdict
    else:
        func_code = "404"
        print(func_code)
        return func_code

if __name__ == '__main__':
    identify_file()