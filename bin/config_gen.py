from configparser import ConfigParser
from Case import Case
config = ConfigParser
class Config:
    def __init__(self, configFilename):
        ConfigParser.__init__(self)
        self.configFilename = configFilename

        self._options = {
            'caseID': None,
            'caseName': None,
            'caseDescription': None,
            'investigator': None,
            'CaseConfigName': None,
            'createdDate': None,
            'ModifiedDateTime': None
        }
        self._CaseConfiguration = {}

    def createConfig (self)
