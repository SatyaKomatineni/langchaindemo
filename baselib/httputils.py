"""
#**********************************************
Module Name: http utils

Description: 
1. http utils
2. Turning out to be very specifc to hugging face

Usage:
1. See the functions

#Date: 1/20/24
#**********************************************
"""

#**********************************************
# Imports
#**********************************************
from baselib import baselog as log
import requests

#**********************************************
# Define module-level variables and constants here
#**********************************************
#None

#**********************************************
# Functions
#**********************************************

def understandResponse(response: requests.Response):
    log.ph1("Examining Types")
    log.ptype("response object", response)
    log.ptype("Headers", response.headers)
    log.ptype("payload", response.text)

    code = response.status_code
    log.ph("Status", code)
    log.ph("Headers", response.headers)
    log.ph("Text", response.text)

    r = getJsonIfValid(response, None)
    if (r == None):
        print("Not able to convert to json")
    else:
        log.ph1("Examing body")
        log.ptype("Converted Json", r)
        log.ptype("First json", r[0])
        log.ph("Converted Json",r)

def getJsonIfValid(response: requests.Response, default):
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError as e:
        log.ph("JSON Exception",e)
        return default
    
def getHFSingleGeneratedText(response: requests.Response) -> str:
    response.raise_for_status()
    dictionaryList = response.json()
    dictionary = dictionaryList[0]
    return dictionary["generated_text"]