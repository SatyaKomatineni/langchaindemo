from baselib import fileutils as fileutils
from baselib import baselog as log

def localTest():
    log.ph1("Starting local test")
    s = fileutils.getTempDataRoot()
    log.dprint(s)
    log.dprint ("End local test")

if __name__ == '__main__':
    localTest()