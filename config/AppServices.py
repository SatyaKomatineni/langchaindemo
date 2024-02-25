"""
*************************************************
* baselib related imports
*************************************************
"""
from baselib import baselog as log

from config.appconfig import AppConfig
from config import appconfig as appconfig

def _getAppConfigObject():
    log.info("Reading Application configuration file")
    return appconfig.readTOMLConfigFile()

def initAppServices(cls):
    log.ph1("Initializing App Services")
    cls.class_app_config = _getAppConfigObject()
    return cls

@initAppServices
class AppServices:
    class_app_config: AppConfig
    @staticmethod
    def config():
        return AppServices.class_app_config
    
"""
*************************************************
* Testing
*************************************************
"""
def _testConfig1():
    token = AppServices.config().api_token_name
    log.ph("Token from config", token)

def _testConfig2():
    a = AppServices.config().embedding_api
    log.ph("embedding api", a)

def test():
    _testConfig1()
    _testConfig2()

def localTest():
    log.ph1("Starting local test")
    test()
    log.ph1("End local test")

if __name__ == '__main__':
    localTest()