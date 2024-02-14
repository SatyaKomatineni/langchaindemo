#langchain stuff
from langchain_community.llms import HuggingFaceTextGenInference

# From local libs
from baselib import aiutils as aiutils
from baselib import httputils as http
from baselib import baselog as log
from baselib import langchain_utils as lutils

from langchain_core.language_models.llms import LLM
from langchain_core.outputs.llm_result import LLMResult


class FBHFTextGenInferenceLLM(HuggingFaceTextGenInference):
    def __init__(self):
        llm_api_url = aiutils.getFB_HF_LLM_Endpoint()
        api_token = aiutils.get_FB_HFAPIKey()
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

def test():
    llm = FBHFTextGenInferenceLLM()
    answer: LLMResult = llm.generate(["All roses are read"])
    lutils.examineTextFrom_HF_LLM_Reply(answer)
    text = lutils.getSingleText_From_HF_LLM_Reply(answer)
    log.ph("Answer from self test LLM",text)


def localTest():
    log.ph1("Starting local test")
    test()
    log.ph1("End local test")

if __name__ == '__main__':
    localTest()