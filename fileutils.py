
import baselog as log
import os

"""
***********************************
Static directories functions
***********************************
"""
def getDataRoot():
    s = r'.'
    return s
    
def getDatasetRoot():
    return os.path.join(getDataRoot(),"datasets")

def getSonnetsRoot():
    return os.path.join(getDatasetRoot(), "sonnets")


def pathjoin(seg1: str, path: str):
    return os.path.join(seg1,path)

def getTempDataRoot():
    return os.path.join(getDataRoot(),"tempdata")


"""
***********************************
writing to files
***********************************
"""
def save_text_to_file(text, filename):
    """
    Saves the given text to a file.

    Args:
    text (str): The text to save.
    filename (str): The name of the file to save the text to.

    Returns:
    None
    """
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)

def testSaveToFile():
    text_to_save = "Hello, this is a sample text."
    filename = "./temp/sample.txt"
    save_text_to_file(text_to_save, filename)

"""
***********************************
Reading from files
***********************************
"""
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        file_contents = file.read()
    return file_contents


"""
***********************************
General utilities
***********************************
"""
def getEnvVariable(name, default):
    value = os.environ[name] 
    if value == None:
        return default
    return value

def localTest():
    log.ph1("Starting local test")
    log.dprint(getTempDataRoot())
    log.ph1("End local test")

if __name__ == '__main__':
    localTest()
