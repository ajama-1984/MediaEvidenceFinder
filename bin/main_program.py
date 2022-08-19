print("#####################################################")
print("PLEASE NOTE:")
print("The Media Evidence Finder Tool is initialising. This can take several minutes. Please Wait!")
print("None of the ASR Engines are utilising GPU Acceleration. Expect reduced transcription speed.")
print("#####################################################")
import self as self
from Case import Case
from evidence import Evidence
from ASR import ASREngine
if __name__ == '__main__':
    # Main program sequence handling user inputs and program flow.
    print("========================================================")
    print("Welcome to MediaEvidenceFinder Application")
    print("========================================================")
    # Existing or new case
    userChoice = input("Press 1 for New Case or 2 to open an existing Case \n")
    if userChoice == "1":
        # Call Create Case function if new case selected
        CurrentCase = Case.createCase(self)
        func_code = Case.caseFuncCodeCheck(self,currentCase=CurrentCase)
        if func_code == "200":
            # Once case is coreated the case details are updated into the current case object
            caseID = Case.get_caseID(self, CurrentCase)
            caseName = Case.get_caseName(self, CurrentCase)
            caseDescription = Case.get_caseDescription(self, CurrentCase)
            CaseConfigName = Case.get_CaseConfigName(self, CurrentCase)
            investigator = Case.get_investigator(self, CurrentCase)
            casePath = Case.get_casePath(self, CurrentCase)
            CreatedTime = Case.get_CreatedTime(self, CurrentCase)
            ModifiedDateTime = Case.get_ModifiedDateTime(self, CurrentCase)
            print("========================================================")
            userChoice = input("Press 1 to add evidence\n")
            if userChoice == "1":
                # The Case configuration file is fetched, and the select, process and retrieve evidence functions are
                # called. User is able to add evidence and see the evidence that is added
                CaseConfigFileName = Case.getCaseConfigFileName(self, CurrentCase)
                evidenceToProcess = Evidence.selectEvidence(self,caseID=caseID)
                func_code = Evidence.evidenceFuncCodeCheck(self, evidenceToProcess)
                filesIdentified = evidenceToProcess[2]
                if func_code == "200":
                    # User is presented with the summary of evidence identified by the tool, user can decide whether
                    # to proceed with adding the evidence to the case
                    Evidence.processEvidence(self, CaseConfigFileName, func_code, filesIdentified,CurrentCase)
                    userChoice = input(
                        "1 to view evidence or 2 to transcribe evidence using Automated Speech Recognition \n")
                    # User can view the evidence again or transcribe the identified evidence using one of the ASR Engines
                    if userChoice == "1":
                        casePath = Case.get_casePath(self, CurrentCase)
                        EvidenceList = Case.getEvidenceIDList(self, CurrentCase)
                        Evidence.retrieveEvidence(self, CaseConfigFileName, CurrentCase)
                        userChoice = input(
                            "Press 1 transcribe evidence \n")
                        if userChoice == "1":
                            ASREngine.ASREngine(self, CaseConfigFileName, CurrentCase)
                        else:
                            print("Invalid Selection - Exiting Program")
                            exit(0)
                    else:
                        if userChoice == "2":
                            ASREngine.ASREngine(self, CaseConfigFileName, CurrentCase)
        else:
            if func_code == "409":
                print(func_code)
                print("Case Already Exists")
    else:
        if userChoice == "2":
            CurrentCase = Case.openCase(self)
            func_code = Case.caseFuncCodeCheck(self, currentCase=CurrentCase)
            if func_code == "200":
                caseID = Case.get_caseID(self,CurrentCase)
                caseName = Case.get_caseName(self, CurrentCase)
                caseDescription = Case.get_caseDescription(self, CurrentCase)
                CaseConfigName = Case.get_CaseConfigName(self,CurrentCase)
                investigator = Case.get_investigator(self, CurrentCase)
                casePath = Case.get_casePath(self, CurrentCase)
                CreatedTime = Case.get_CreatedTime(self, CurrentCase)
                ModifiedDateTime = Case.get_ModifiedDateTime(self, CurrentCase)
                CaseConfigFileName = Case.getCaseConfigFileName(self, CurrentCase)
                print("Case " + caseName + " has been loaded")
                print("========================================================")
                userChoice = input("Press 1 to add evidence or 2 to view Evidence currently added \n")
                if userChoice == "1":
                    evidenceToProcess = Evidence.selectEvidence(self,caseID=caseID)
                    func_code = Evidence.evidenceFuncCodeCheck(self,evidenceToProcess)
                    filesIdentified = evidenceToProcess[2]
                    if func_code == "200":
                        ProcessEvidence = Evidence.processEvidence(self,CaseConfigFileName,func_code,filesIdentified, CurrentCase)
                        Evidence.retrieveEvidence(self, CaseConfigFileName, CurrentCase)
                        userChoice = input(
                            "Press 1 transcribe evidence using Automated Speech Recognition \n")
                        if userChoice == "1":
                            casePath = Case.get_casePath(self, CurrentCase)
                            ASREngine.ASREngine(self, CaseConfigFileName, CurrentCase)
                    else:
                        print("Evidence Identification Failed. Exiting Program")
                        exit(0)
                else:
                    if userChoice == "2":
                        Evidence.retrieveEvidence(self, CaseConfigFileName, CurrentCase)
                        userChoice = input("Press 1 to add evidence or 2 to transcribe evidence using Automated Speech Recognition \n")
                        if userChoice == "1":
                            evidenceToProcess = Evidence.selectEvidence(self, caseID=caseID)
                            func_code = Evidence.evidenceFuncCodeCheck(self, evidenceToProcess)
                            filesIdentified = evidenceToProcess[2]
                            if func_code == "200":
                                ProcessEvidence = Evidence.processEvidence(self, CaseConfigFileName, func_code,
                                                                           filesIdentified, CurrentCase)
                            else:
                                print("Evidence Identification Failed. Exiting Program")
                                exit(0)
                        else:
                            if userChoice == "2":
                                casePath = Case.get_casePath(self, CurrentCase)
                                ASREngine.ASREngine(self, CaseConfigFileName, CurrentCase)
                    else:
                        print("Invalid Selection - Exiting Program")
            else:
                if func_code == "404":
                    print("Invalid Case Config File")
                    exit(0)
        else:
            print("Invalid Selection - Exiting Program")