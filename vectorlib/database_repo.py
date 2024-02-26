
# Langchain
from langchain_core.language_models.llms import LLM

#logging
from baselib import baselog as log

# Local
from vectorlib.database import (
    SOFU_Database,
    Database
)
from vectorlib.sofu_hf_database import SOFU_HF_Database
from customllms.custom_fb_hf_inference_llm import FBHFTextGenInferenceLLM
from customllms.custom_hf_llm import HFCustomLLM
from customllms.config_hf_inference_llm import ConfigHFLLM

"""
****************************************
* A repo of global objects
****************************************
"""
class DatabaseRepo:
    class_sofu_db: Database = SOFU_Database()
    class_fbhf_llm = FBHFTextGenInferenceLLM()

    class_sofu_db2: Database = SOFU_HF_Database()
    #class_hf_llm = HFCustomLLM(n=1, name="HF TGI LLM")
    class_hf_llm = ConfigHFLLM()

    @staticmethod
    def getSOFUDatabase() -> Database:
        return DatabaseRepo.class_sofu_db
    
    @staticmethod
    def get_fbhf_LLM() -> LLM:
        return DatabaseRepo.class_fbhf_llm
    
    @staticmethod
    def getSOFUDatabase2() -> Database:
        return DatabaseRepo.class_sofu_db2
    
    @staticmethod
    def get_hf_LLM() -> LLM:
        return DatabaseRepo.class_hf_llm
"""
*************************************************
* Local testing
*************************************************
"""
def _test2():
    db_container = DatabaseRepo.getSOFUDatabase()
    db_container.raise_for_status()
    db_container.examine()

def test():
    _test2()

def localTest():
    log.ph1("Starting local test")
    test()
    log.ph1("End local test")

if __name__ == '__main__':
    localTest()