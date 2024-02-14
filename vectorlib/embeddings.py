from typing import Any, Dict, List, Optional

import requests
from langchain_core.embeddings import Embeddings
from langchain_community.embeddings import (
    HuggingFaceHubEmbeddings,
    HuggingFaceInferenceAPIEmbeddings
)

from baselib import fileutils as fileutils
from baselib import baselog as log
from baselib import aiutils as aiutils
import time
import getpass

from langchain_core.utils.utils import convert_to_secret_str

"""
************************************************
* class: GenURLEmbedder(Embeddings)
*
* A base class for implementing URL based embedders
*
* 1. Import from the base interface
* 2. Implement the 2 necessary methods
* 3. Parameterize for URL to call, API token etc.
* 4. Provide a simple single threaded implementation
*
* Derived classes neeed to supply the init params
* 
* See the derived class FB_HF_Embeddings(GenURLEmbedder)
*
* Note:
* Uses a few utility libraries for logging, reading files,
* getting URLs, Tokens etc.
* 
************************************************
"""
class GenURLEmbedder(Embeddings):
    url: str
    params: dict
    token: str
    def __init__(self, url: str, token: str, params: dict) :
        self.url = url
        self.params = params
        self.token = token
           
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        self._implementAPIDelay_p()
        response = requests.post(
                self.url, 
                json={"inputs": texts}, 
                headers={"Authorization": f"Bearer {self.token}"}
            )
        response.raise_for_status()
        return response.json()
    
    def embed_query(self, text: str) -> List[float]:
        return self.embed_documents([text])[0]

    # _tm stands for template method
    def _getDelayInSecs_tm(self) -> int:
        return 0
    
    #This is implemented here. No need to overwrite
    #called a protocol method
    def _implementAPIDelay_p(self):
        secs:int = self._getDelayInSecs_tm()
        if secs <=0 :
            return
        log.warn(f"Waiting for {secs} seconds before invoking the api due to rate reasons")
        time.sleep(secs)

"""
************************************************
* class: FB_HF_Embeddings(GenURLEmbedder):
*
* An instantiable base class that uses HF model for embeddings
*
************************************************
"""
class FB_HF_Embeddings(GenURLEmbedder):
    def __init__(self) :
        url = aiutils.getSampleEmbeddingAPI()
        token = aiutils.get_FB_HFAPIKey()
        params = {}
        super().__init__(url=url,token=token,params=params)

    # wait for 5 seconds
    def _getDelayInSecs_tm(self) -> int:
        return 5

"""
*************************************************
* Using 
* from langchain_community.embeddings import HuggingFaceHubEmbeddings
*************************************************
"""    

def x():
    pass

class FB_HF_InferenceAPIEmbeddings(HuggingFaceInferenceAPIEmbeddings):
    def __init__(self) :
        url = aiutils.getSampleEmbeddingAPI()
        token = aiutils.get_FB_HFAPIKey()
        apikey = convert_to_secret_str(token)
        super().__init__(
            api_url = url,
            api_key=apikey
        )


def _testHubEmeddings():
    x = FB_HF_InferenceAPIEmbeddings()
    r = x.embed_query("hello world")
    log.ph("Hub Embedding test", r)

"""
************************************************
* Test locally
************************************************
"""
def testEmbedding():
    e = FB_HF_Embeddings()
    r = e.embed_query("Hello World")
    log.ph("Sample embedding", r)

def localTest():
    log.ph1("Starting local test")
    #testEmbedding()
    _testHubEmeddings()
    log.ph1("End local test")

if __name__ == '__main__':
    localTest()
    