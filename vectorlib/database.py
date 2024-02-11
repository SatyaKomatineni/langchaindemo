
from abc import ABC, abstractmethod
from langchain_community.vectorstores import Chroma

# Local stuff
import chromautils as chromautils
from baselib import baselog as log

class Database(ABC):

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def isItReady(self) -> bool:
        pass

    def raise_for_status(self):
        if self.isItReady() == False :
            raise Exception("Database is not ready: {self.name()}")

    @abstractmethod
    def examine(self):
        pass

    @abstractmethod
    def _create(self):
        pass

    @abstractmethod
    def doesitExist(self) -> bool:
        pass

    # Not threadsafe at the moment
    def create(self):
        if self.doesitExist():
            return
        self._create()

class SOFU_Database(Database):
    db: Chroma
    v_name: str = "State of the Union Chroma Database"

    def __init__(self):
        self._create()
        
    def _create(self):
        self.db = chromautils.get_persistent_sofu_vector_db()

    def get(self):
        return self.db

    def doesitExist(self) -> bool:
        if self.db == None :
            return False
        return True

    def name(self):
        return self.v_name

    def examine(self):
        log.ph("Examinging the vector store", f"Name: {self.name()}")
        x = self.db._collection.count()
        log.info(f"Number of vectors:{x}")

    def isItReady(self) -> bool:
        number_of_vectors = self.db._collection.count()
        if number_of_vectors >= 0 :
            return True
        return False
    
"""
****************************************
* A repo of global objects
****************************************
"""
class DatabaseRepo:
    class_sofu_db: Database = SOFU_Database()

    @staticmethod
    def getSOFUDatabase() -> Database:
        return DatabaseRepo.class_sofu_db
    
"""
****************************************
* Testing
****************************************
"""
def test1():
    db_container = SOFU_Database()
    db_container.raise_for_status()
    db_container.examine()

def test2():
    db_container = DatabaseRepo.getSOFUDatabase()
    db_container.raise_for_status()
    db_container.examine()

def localTest():
    log.ph1("Starting local test")
    test2()
    log.ph1("End local test")

if __name__ == '__main__':
    localTest()
