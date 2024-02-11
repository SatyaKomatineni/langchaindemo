from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents.base import Document
from langchain_core.vectorstores import VectorStore
from langchain.text_splitter import CharacterTextSplitter

from baselib import fileutils as fileutils
from baselib import baselog as log
from vectorlib.embeddings import FB_HF_Embeddings

def _getStateOfTheUnionDocChunks() -> list[Document]:
    # Get the file path
    dspath = fileutils.getDatasetRoot()
    sou_doc_name = "state_of_the_union.txt"
    sou_file_path = fileutils.pathjoin(dspath,sou_doc_name)

    # Read from file using text loader
    log.ph("Reading from", sou_file_path)
    loader = TextLoader(sou_file_path, encoding="utf-8")
    documents = loader.load()

    # split it into chunks
    text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    return docs

def createChromaDBFromDocs(documentList: list[Document]):
    # create the open-source embedding function
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    return Chroma.from_documents(documentList,embedding_function)

"""
************************************************
* Public functions
************************************************
"""

"""
1. Uses Sentence transformer embeddings
"""
def get_in_memory_sofu_vector_db() -> VectorStore: 
    log.ph1("Creating in memory vector store")
    docs = _getStateOfTheUnionDocChunks()
    db = createChromaDBFromDocs(docs)
    log.info("Vector store successfully created")
    return db

def get_persistent_sofu_vector_db() -> VectorStore:

    #get the chromadb db directory
    log.info("Getting the chromadb directory")
    chromadb_dir = _getChromaDbFileName()

    #Get the embedder (Uses the API to load them)
    fb_embeddings = FB_HF_Embeddings()
    
    db = Chroma(persist_directory=chromadb_dir, embedding_function=fb_embeddings)
    return db

"""
1. Uses FB Embeddings
"""
def create_persistent_sofu_vector_db() -> VectorStore: 

    log.ph1("Creating a persistent vector store")

    #get the chromadb db directory
    log.info("Getting the chromadb directory")
    chromadb_dir = _getChromaDbFileName()

    #get the doc chunks
    log.info("Getting SOFU chunks")
    docs = _getStateOfTheUnionDocChunks()

    #Get the embedder (Uses the API to load them)
    fb_embeddings = FB_HF_Embeddings()

    # Make the db from documents
    log.info(f"Creating the persistent chromadb at {chromadb_dir}")
    db = Chroma.from_documents(documents=docs, 
            embedding=fb_embeddings, 
            persist_directory=chromadb_dir)
    
    log.info("Vector store successfully created")
    return db

def _getChromaDbFileName() -> str:
    tempDataDir = fileutils.getTempDataRoot()
    return fileutils.pathjoin(tempDataDir, "sofu_chromadb")

"""
************************************************
* Testing functions
************************************************
"""
def _testPersistentChromaDB():
    db = get_persistent_sofu_vector_db()

def testSOFU():
    docs = _getStateOfTheUnionDocChunks()
    log.dprint(f"Number of docs:{len(docs)}")
    log.summarizeLargeText(f"{docs[0]}")

def testChroma():
    docs = _getStateOfTheUnionDocChunks()
    db = createChromaDBFromDocs(docs)

    # query it
    query = "What did the president say about Ketanji Brown Jackson"
    docs = db.similarity_search(query)

    # print results
    pc = docs[0].page_content
    log.ph1("Similarity Search")

def _examineDb(db: VectorStore):
    log.ph1 ("Examinging the vector store")
    x = db._collection.count()
    log.info(f"Number of vectors:{x}")

def localTest():
    log.ph1("Starting local test")
    #testSOFU()
    #db = create_persistent_sofu_vector_db()
    db = get_persistent_sofu_vector_db()
    _examineDb(db)
    log.ph1("End local test")

if __name__ == '__main__':
    localTest()
