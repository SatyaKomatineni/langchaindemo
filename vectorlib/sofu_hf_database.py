
from abc import ABC, abstractmethod
from langchain_community.vectorstores import Chroma
from langchain_core.vectorstores import VectorStore
from langchain_core.embeddings import Embeddings
from langchain_core.language_models.llms import LLM
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_core.documents.base import Document
from langchain.text_splitter import CharacterTextSplitter


# Local stuff
from vectorlib import chromautils as chromautils
from customllms.custom_fb_hf_inference_llm import FBHFTextGenInferenceLLM

from baselib import baselog as log
from baselib import fileutils as fileutils
from vectorlib.embeddings import FB_HF_InferenceAPIEmbeddings
from vectorlib.database import Database

"""
1. has no dependency on FB HF APIs
2. Uses HF Transformer
3. Uses HF API for text gen end point

What does it do:
1. It takes a State of the Union Text from 2023 from datasets sub dir
2. Chunks it with TextLoader in to 2000 characters
3. Load them into Chroma db vecor database
4. Makes it all available as a db ready for search

"""
class SOFU_HF_Database(Database):
    db: Chroma
    v_name: str = "State of the Union Chroma Database 2"
    filename: str = "sofu_chromadb_2"

    def __init__(self):
        self._create()
        
    def _create(self):
        #self.db = chromautils.get_persistent_sofu_vector_db()
        self.db = self._createWithEmbeddings(
                self.getRelatedEmbeddings(),
                self.getDbPath())
        #The following will check not to do twice
        self._populateDatabase()

    def _createWithEmbeddings(self, embeddings: Embeddings, dbpath: str) -> Chroma:
        log.info(f"Creating database: {self.name()}")
        db = Chroma(persist_directory=dbpath, embedding_function=embeddings)
        return db

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
        if number_of_vectors > 0 :
            return True
        return False
    
    def getRelatedEmbeddings(self) -> Embeddings:
        return SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    
    def getDbPath(self) -> str:
        return fileutils.getTempDataFilename(self.filename)
    
    def _populateDatabase(self):
        if self.isItReady():
            log.warn(f"'{self.name()}' db is ready. No need to populate")
            return
        
        log.warn(f"{self.name()} is not populated likely. Populating now")
        #get the doc chunks
        log.info("Getting SOFU chunks")
        docs = chromautils._getStateOfTheUnionDocChunks()
        docs_str_list = [doc.page_content for doc in docs]
        self.db.add_texts(docs_str_list)
        log.info(f"'{self.name()}' db is populated")

"""
*************************************************
* Private methods
*************************************************
"""

def test():
    db = SOFU_HF_Database()
    db.examine()

def localTest():
    log.ph1("Starting local test")
    test()
    log.ph1("End local test")

if __name__ == '__main__':
    localTest()