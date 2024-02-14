"""
#**********************************************
Module Name: baselog

Description: 
1. To provide pretty print statements
2. Allow for h1, h2, h3 etc
3. Possibly provide time stamps

Usage:
1. Just see the functions

#Date: 1/20/24
#**********************************************
"""
import regex as re

   
"""
#**********************************************
Backlog:
1. Provide levels to debug to better control print statements
2. Provide a enum with print statements (info, debug, trace, etc)
#**********************************************
"""
#**********************************************
# Define module-level variables and constants here
#**********************************************
#None

#**********************************************
# Functions
#**********************************************

global_debug = True

def turnOffDebug():
    global global_debug
    global_debug = False

    
def dprint(text: str):
    if global_debug == False :
        return
    print(text)

def p(text: str):
    dprint(f"{text}")

def ph(h: str,m: object):
    dprint(f"\n{h}")
    dprint("***********************")
    dprint(f"{m}")

def ptype(context: str, o: object):
    dprint(f"Type of {context}:\n{type(o)}")

def uph1(h: str):
    print(f"\n{h}")
    print("***********************")

def uph(h: str,m: object):
    print(f"\n{h}")
    print("***********************")
    print(f"{m}")

def ph1(h: str):
    dprint(f"\n{h}")
    dprint("***********************")

def prompt(text: str) -> str:
    return input(f"\n> {text}")

#**********************************************
# log classification
#**********************************************
def warn(m: str):
    dprint(f"warn: {m}")

def trace(m: str):
    dprint(f"trace: {m}")
    
def info(m: str):
    dprint(f"info: {m}")

#**********************************************
# Validation functions
#**********************************************

def validate_not_null_or_empty(context: str, *args):
    for arg in args:
        if arg is None:
            raise ValueError(f"The specified Argument {arg} cannot be null or empty.\nContext: {context}")
        elif isinstance(arg, str) and not arg.strip():
            raise ValueError(f"The specified Argument {arg} cannot be an empty string\nContext: {context}")


def examine_large_string(text, max_length, context: str):
    ph1(f"Examining a large string: {context}")
    if text is None:
        dprint("The input string is None.")
        return
    if not text.strip():
        dprint("The input string is empty.")
        return
    dprint("It is a valid string")
    dprint(f"Size of the string: {len(text)} characters")
    dprint(f"\n{text[:max_length]}")

def isValidString(s: str):
    return not isValidString(s)

def isEmptyString(s: str):
    return bool(s and not s.isspace())

#**********************************************
# End: Validation functions
#**********************************************
    
#**********************************************
# Utility functions
#**********************************************
def is_roman_numeral(s):
    # Regular expression pattern for Roman numerals
    pattern = r'^[IVXLCDM]+$'

    # Match the pattern with the string
    if re.match(pattern, s):
        return True
    else:
        return False
    
def summarizeDictionary(d: dict):
    ph1("Summarizing a dictionary")
    size = len(d)
    if size == 0:
        dprint("It is an empty dictionary")
        return
    dprint(f"Size: {len(d)}")
    dprint(f"Printing first row")
    pair = next(enumerate(d.items()))
    dprint(f"{pair[1]}")

def summarizeLargeText(large_text):
    validate_not_null_or_empty(large_text)
    dprint(large_text[:200])
    
def testSummarizeDictionary():
    d = {1:"1", 2:"2"}
    summarizeDictionary(d)

#**********************************************
# Utility functions
#**********************************************

def localTest():
    ph1("Starting local test")
    testSummarizeDictionary()
    print ("End local test")

if __name__ == '__main__':
    localTest()