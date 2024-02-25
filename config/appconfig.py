"""
*************************************************
* File specific imports
*************************************************
"""
from pydantic import BaseModel
from typing import List
import json
import tomlkit

"""
*************************************************
* other libs
*************************************************
"""
from baselib import baselog as log
from baselib import fileutils as fileutils

class AppConfig (BaseModel):
    api_token_name: str = ""
    embedding_api: str = ""
    llm_api: str =""


"""
*************************************************
* Main utility functions
*************************************************
"""
def _getASampleConfigObjct():
    o = AppConfig()
    o.api_token_name = "api-token-name"
    o.embedding_api = "embedding api"
    o.llm_api = "llm api"
    return o

def _getAppTOMLConfigFilename() -> str:
    dataroot = fileutils.getAppDataRoot()
    return fileutils.pathjoin(dataroot, "appconfig.toml")

def readTOMLConfigFile() -> AppConfig:
    configfile = _getAppTOMLConfigFilename()
    toml_str = fileutils.read_text_file(configfile)
    parsed_toml: tomlkit.TOMLDocument = tomlkit.parse(toml_str)
    json_str: str = json.dumps(parsed_toml,indent=4)
    dict = json.loads(json_str)
    obj = AppConfig(**dict)
    return obj

"""
*************************************************
* JSON related
*************************************************
"""
def _getAppConfigFilename() -> str:
    dataroot = fileutils.getAppDataRoot()
    return fileutils.pathjoin(dataroot, "appconfig.json")

def _readJSONConfigFile():
    configfile = _getAppConfigFilename()
    with open(configfile, 'r') as file:
        data = json.load(file)
        obj = AppConfig(**data)

"""
*************************************************
* Produce sample files
*************************************************
"""

def _produceASampleConfigfile():
    sampleConfigFilename = fileutils.getAppDataRootFilename("sample_config.json")
    log.ph("Producing a sample config file", sampleConfigFilename)
    o = _getASampleConfigObjct()
    o_json_pretty = o.model_dump_json(indent=4)
    fileutils.save_text_to_file(o_json_pretty, sampleConfigFilename)

def _produceASampleConfigfileTOML():
    sampleConfigFilename = fileutils.getAppDataRootFilename("sample_config.toml")
    log.ph("Producing a sample config file", sampleConfigFilename)
    o = _getASampleConfigObjct()
    o_json_pretty = o.model_dump_json(indent=4)
    d = json.loads(o_json_pretty)
    toml = tomlkit.dumps(d)
    fileutils.save_text_to_file(toml, sampleConfigFilename)




def _test2():
    _produceASampleConfigfile()
    _produceASampleConfigfileTOML()

def _test3():
    config: AppConfig = _readTOMLConfigFile()
    log.ph("App Token", config.api_token_name)

def _test1():
    filename = fileutils.getAppDataRootFilename("sample_config.json")
    log.ph("Sample config file", filename)

def localTest():
    log.ph1("Starting local test")
    #_test1()
    #_test2()
    _test3()
    log.ph1("End local test")

if __name__ == '__main__':
    localTest()