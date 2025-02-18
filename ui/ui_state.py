
from baselib import aiutils as aiutils
from baselib import baselog as log
from baselib import fileutils as fileutils

from ui.questions import QuestionRepo
class ApplicationState():
    #Local variables
    log_messages: list[str]
    questionRepo: QuestionRepo


    #class variables
    class_save_filename = "application_state.data"

    #functions
    def __init__(self):
        self.log_messages = []
        self.questionRepo = QuestionRepo()

    def addMessage(self, message: str):
        self.log_messages.append(message)

    def clear(self):
        log.info("Clearing messages from display log")
        self.log_messages.clear()
    
    def save(self):
        log.info(f"Saving state to {ApplicationState.class_save_filename}")
        fileutils.store_object_to_file(self, ApplicationState.class_save_filename)

    @staticmethod
    def translatedFilename():
        return fileutils.getTempDataFilename(ApplicationState.class_save_filename)

    @staticmethod
    def restore():
        fullpath = ApplicationState.translatedFilename()
        if not fileutils.exists(fullpath):
            log.info(f"File {fullpath} does not exsit. Returning empty state")
            return ApplicationState()
        
        log.info(f"Restoring state from {fullpath}")
        self_obj = fileutils.read_object_from_file(fullpath)
        return self_obj

