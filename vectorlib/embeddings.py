from typing import Any, Dict, List, Optional

import requests
from langchain_core.embeddings import Embeddings

from baselib import fileutils as fileutils
from baselib import baselog as log
from baselib import aiutils as aiutils

class GenURLEmbedder():
    url: str
    params: dict
    token: str
    def __init__(self, url: str, token: str, params: dict) :
        self.url = url
        self.params = params
        self.token = token
           
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        response = requests.post(
                self.url, 
                json={"inputs": texts}, 
                headers={"Authorization": f"Bearer {self.token}"}
            )
        response.raise_for_status()
        return response.json()
    
    def embed_query(self, text: str) -> List[float]:
        return self.embed_documents([text])[0]

class FB_HF_Embeddings(GenURLEmbedder):
    def __init__(self) :
        url = aiutils.getSampleEmbeddingAPI()
        token = aiutils.get_FB_HFAPIKey()
        params = {}
        super().__init__(url=url,token=token,params=params)

def testEmbedding():
    e = FB_HF_Embeddings()
    r = e.embed_query("Hello World")
    log.ph("Sample embedding", r)

def localTest():
    log.ph1("Starting local test")
    testEmbedding()
    log.ph1("End local test")

if __name__ == '__main__':
    localTest()
    