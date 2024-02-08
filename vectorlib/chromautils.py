from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents.base import Document

from baselib import fileutils as fileutils
from baselib import baselog as log

def getStateOfTheUnion() -> list[Document]:
    dspath = fileutils.getDatasetRoot()
    sou_doc_name = "state_of_the_union.txt"
    sou_file_path = fileutils.pathjoin(dspath,sou_doc_name)
    log.ph("Reading from", sou_file_path)
    loader = TextLoader(sou_file_path, encoding="utf-8")
    documents = loader.load()
    return documents

def createChromaDBFromDocs(documentList: list[Document]):
    # create the open-source embedding function
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    return Chroma.from_documents(documentList,embedding_function)

def testSOFU():
    docs = getStateOfTheUnion()
    log.dprint(f"Number of docs:{len(docs)}")
    log.summarizeLargeText(f"{docs[0]}")

def testChroma():
    docs = getStateOfTheUnion()
    db = createChromaDBFromDocs(docs)

    # query it
    query = "What did the president say about Ketanji Brown Jackson"
    docs = db.similarity_search(query)

    # print results
    pc = docs[0].page_content
    log.ph1("Similarity Search")

def localTest():
    log.ph1("Starting local test")
    testChroma()
    log.ph1("End local test")

if __name__ == '__main__':
    localTest()
