import self as self
from Case import Case
from evidence import Evidence
from ASR import ASREngine
if __name__ == '__main__':
    print("========================================================")
    print("Welcome to MediaEvidenceFinder Application")
    print("========================================================")
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
            print("========================================================")
            userChoice = input("Press 1 to add evidence\n")
            if userChoice == "1":
                CaseConfigFileName = Case.getCaseConfigFileName(self, CurrentCase)
                evidenceToProcess = Evidence.selectEvidence(self,caseID=caseID)
                func_code = Evidence.evidenceFuncCodeCheck(self, evidenceToProcess)
                filesIdentified = evidenceToProcess[2]
                if func_code == "200":
                    Evidence.processEvidence(self, caseID, CaseConfigFileName, func_code, filesIdentified,CurrentCase)
                    userChoice = input(
                        "Press 1 to add evidence, 2 to view evidence or 3 to transcribe evidence using Automated Speech Recognition \n")
                    if userChoice == "1":
                        evidenceToProcess = Evidence.selectEvidence(self, caseID=caseID)
                        func_code = Evidence.evidenceFuncCodeCheck(self, evidenceToProcess)
                        filesIdentified = evidenceToProcess[2]
                        if func_code == "200":
                            ProcessEvidence = Evidence.processEvidence(self, caseID, CaseConfigFileName, func_code,
                                                                       filesIdentified, CurrentCase)
                        else:
                            print("Evidence Identification Failed. Exiting Program")
                            exit(0)
                    else:
                        if userChoice == "2":
                            casePath = Case.get_casePath(self, CurrentCase)
                            print(CaseConfigFileName)
                            print(casePath)
                            EvidenceList = Case.getEvidenceIDList(self, CurrentCase)
                            print(EvidenceList)
                            Evidence.retrieveEvidence(self, CaseConfigFileName, CurrentCase)

                            print(EvidenceList)
                            print(CaseConfigFileName)
                            print(CurrentCase)
                            ASREngine.ASREngine(self, CaseConfigFileName, CurrentCase)
                        else:
                            print("Invalid Selection - Exiting Program")
                            exit(0)

            # else:
            #     if userChoice == "2":
            #         CaseConfigFileName = Case.getCaseConfigFileName(self, CurrentCase)
            #         Evidence.retrieveEvidence(self, CaseConfigFileName, CurrentCase)
            #         userChoice = input(
            #             "Press 1 to add evidence or 2 to transcribe evidence using Automated Speech Recognition \n")
            #         if userChoice == "1":
            #             evidenceToProcess = Evidence.selectEvidence(self, caseID=caseID)
            #             func_code = Evidence.evidenceFuncCodeCheck(self, evidenceToProcess)
            #             filesIdentified = evidenceToProcess[2]
            #             if func_code == "200":
            #                 ProcessEvidence = Evidence.processEvidence(self, caseID, CaseConfigFileName, func_code,
            #                                                            filesIdentified, CurrentCase)
            #             else:
            #                 print("Evidence Identification Failed. Exiting Program")
            #                 exit(0)
            #         else:
            #             if userChoice == "2":
            #                 casePath = Case.get_casePath(self, CurrentCase)
            #                 print(CaseConfigFileName)
            #                 print(CurrentCase)
            #                 ASREngine.ASREngine(self, CaseConfigFileName, CurrentCase)
            #             else:
            #                 print("Invalid Selection - Exiting Program")
            #                 exit(0)

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
                        ProcessEvidence = Evidence.processEvidence(self,caseID,CaseConfigFileName,func_code,filesIdentified, CurrentCase)
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
                                ProcessEvidence = Evidence.processEvidence(self, caseID, CaseConfigFileName, func_code,
                                                                           filesIdentified, CurrentCase)
                            else:
                                print("Evidence Identification Failed. Exiting Program")
                                exit(0)
                        else:
                            if userChoice == "2":
                                casePath = Case.get_casePath(self, CurrentCase)
                                print(CaseConfigFileName)
                                print(CurrentCase)
                                ASREngine.ASREngine(self, CaseConfigFileName, CurrentCase)
                    else:
                        print("Invalid Selection - Exiting Program")
            else:
                if func_code == "404":
                    print("Invalid Case Config File")
                    exit(0)
        else:
            print("Invalid Selection - Exiting Program")