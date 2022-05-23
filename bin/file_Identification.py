import magic
import glob, os
import ffmpeg
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata

def identify_file(EvidencePath):
    dbdict = dict()
    if os.path.exists(EvidencePath):
        print("Path Exists")
        for filename in os.scandir(EvidencePath):
            file_path = filename.path
            mime = magic.Magic(mime=True)
            file_type = mime.from_file(file_path)
            parser = createParser(file_path)
            metadata = extractMetadata(parser)
            print(metadata)
            if str(file_type).__contains__("audio") or str(file_type).__contains__("video"):
                file_properties = str(file_type) + str(metadata)
                dbdict.update({filename:file_properties})
        func_code = "200"
        print(dbdict)
        print(func_code)
        return func_code, dbdict
    else:
        func_code = "404"
        print(func_code)
        return func_code

if __name__ == '__main__':
    identify_file()