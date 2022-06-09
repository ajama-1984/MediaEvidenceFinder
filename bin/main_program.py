import self as self
from file_Identification import identify_file
from audio_extraction import extract_audio_from_source
# from CMUsphinx_speech2text import pocketsphinx_S2T
# from keyword_searching import search_Keywords
from Case import Case
from evidence import Evidence

if __name__ == '__main__':
    userChoice = input("Press 1 for New Case or 2 to open an existing Case \n")
    if userChoice == "1":
        CurrentCase = Case.createCase(self)
        func_code = Case.caseFuncCodeCheck(self,currentCase=CurrentCase)
        if func_code == "200":
            print(func_code)
            caseID = Case.get_caseID(self, CurrentCase)
            caseName = Case.get_caseName(self, CurrentCase)
            caseDescription = Case.get_caseDescription(self, CurrentCase)
            CaseConfigName = Case.get_CaseConfigName(self, CurrentCase)
            investigator = Case.get_investigator(self, CurrentCase)
            casePath = Case.get_casePath(self, CurrentCase)
            CreatedTime = Case.get_CreatedTime(self, CurrentCase)
            ModifiedDateTime = Case.get_ModifiedDateTime(self, CurrentCase)
            userChoice = input("Press 1 to add and process evidence \n")
            if userChoice == "1":
                evidenceToProcess = Evidence.selectEvidence(self,caseID=caseID)
        else:
            if func_code == "409":
                print(func_code)
                print("Case Already Exists")
    else:
        if userChoice == "2":
            CurrentCase = Case.openCase(self)
            func_code = Case.caseFuncCodeCheck(self, currentCase=CurrentCase)
            print(func_code)
            if func_code == "200":
                caseID = Case.get_caseID(self,CurrentCase)
                caseName = Case.get_caseName(self, CurrentCase)
                caseDescription = Case.get_caseDescription(self, CurrentCase)
                CaseConfigName = Case.get_CaseConfigName(self,CurrentCase)
                investigator = Case.get_investigator(self, CurrentCase)
                casePath = Case.get_casePath(self, CurrentCase)
                CreatedTime = Case.get_CreatedTime(self, CurrentCase)
                ModifiedDateTime = Case.get_ModifiedDateTime(self, CurrentCase)
            userChoice = input("Press 1 to add and process evidence \n")
            if userChoice == "1":
                evidenceToProcess = Evidence.selectEvidence(self,caseID=caseID)
        else:
            print("Invalid Selection - Exiting Program")