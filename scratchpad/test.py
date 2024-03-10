from baselib import baselog as log
from baselib import fileutils as fileutils


class MyBaseClass:
    def __init__(self, name: str, age: int):
        self.name:str = name
        self.age: int = age

    #If you want to print the class
    def __str__(self):
        return f"{self.name}, {self.age}"

def testBaseClass():
    x = MyBaseClass("hello",5)
    log.info(f"{x}")

def localTest():
    log.ph1("Starting local test")
    log.dprint(fileutils.getTempDataRoot())
    log.dprint ("End local test")

if __name__ == '__main__':
    localTest()
    testBaseClass()