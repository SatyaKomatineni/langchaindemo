from baselib import baselog as log
from baselib import fileutils as fileutils

def localTest():
    log.ph1("Starting local test")
    log.dprint(fileutils.getTempDataRoot())
    log.dprint ("End local test")

if __name__ == '__main__':
    localTest()