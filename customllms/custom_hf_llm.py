from typing import Any, List, Mapping, Optional
from baselib import aiutils as aiutils
from baselib import httputils as http
from baselib import baselog as log

from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM

import requests

"""
**************************************************
* HFCustomLLM
**************************************************
"""
class HFCustomLLM(LLM):
    n: int
    name: str

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")
        return self._talkToTheHand(prompt)

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"n": self.n, "name": self.name}
    
    def _talkToTheHand(self, prompt:str):
        params = self._getParameters1()
        response: requests.Response = self._queryModel(prompt,params)
        return response.json()

    def _queryModel(self, prompt, parameters):
        apiKey = aiutils.getHFAPIKey()
        hfEndPointUrl = aiutils.getSampleHFEndPoint()
        headers = {"Authorization": f"Bearer {apiKey}"}
        payload = {
            "inputs": prompt,
            "parameters": parameters
        }
        response = requests.post(hfEndPointUrl, headers=headers, json=payload)
        http.understandResponse(response)
        return response
    
    def _extractGeneratedText(self, response: requests.Response):
        return response.json()[0]['generated_text']

    def _getParameters1(self):
        return {
                "max_new_tokens": 200,
                "temperature": 0.6,
                "top_p": 0.9,
                "do_sample": False,
                "return_full_text": False
        }

    def _getParameters(self):
        return {
            "max_length": 200
        }

    def _getTestPrompt(self):
        question = "What is the population of Jacksonville, Florida?"
        return question

    def _getTestPrompt2(self):
        question = "What is the population of Jacksonville, Florida?"
        context = "As of the most current census, Jacksonville, Florida has a population of 1 million."
        prompt = f"""Use the following context to answer the question at the end.
        {context}
        Question: {question}
        """
        return prompt
    
    def selfTest(self: LLM):
        answer: str = self.invoke("All roses are read")
        log.ph("Answer from self test LLM",answer)
"""
**************************************************
* EOF_Class: HFCustomLLM
**************************************************
"""
def testHFCustomLLM():
    llm = HFCustomLLM(n=10, name="Satya")
    llm.selfTest()

def localTest():
    log.ph1("Starting local test")
    testHFCustomLLM()
    log.ph1("End local test")

if __name__ == '__main__':
    localTest()