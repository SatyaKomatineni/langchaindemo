#langchain stuff
from langchain_community.llms import HuggingFaceTextGenInference

# From local libs
from baselib import aiutils as aiutils
from baselib import httputils as http
from baselib import baselog as log
from baselib import fileutils as fileutils

from langchain_core.language_models.llms import LLM
from langchain_core.outputs.llm_result import LLMResult
from config.AppServices import AppServices

class ConfigHFLLM(HuggingFaceTextGenInference):
    def __init__(self):
        llm_api_url = AppServices.config().llm_api
        api_token = self._getToken()
        super().__init__(
            inference_server_url=llm_api_url,
            max_new_tokens=512,
            top_p=0.9,
            server_kwargs={
                "headers": {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_token}"
                }
            }
        )
    def _getToken(self):
        token_name = AppServices.config().api_token_name
        token = fileutils.getEnvVariable(token_name, None)
        if (token == None):
            raise Exception(f"No env variable found: {token_name}")
        return token



def test():
    llm = ConfigHFLLM()
    answer: LLMResult = llm.generate(["All roses are read"])
    log.ph("Answer from self test LLM",answer)


def localTest():
    log.ph1("Starting local test")
    test()
    log.ph1("End local test")

if __name__ == '__main__':
    localTest()