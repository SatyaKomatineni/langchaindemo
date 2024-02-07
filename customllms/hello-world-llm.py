from baselib import baselog as log

from typing import Any, List, Mapping, Optional

from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM

class HelloWorldCustomLLM(LLM):
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
        return "Hello World"

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"n": self.n, "name": self.name}
    

def testHelloWorldLLM():
    llm = HelloWorldCustomLLM(n=10, name="Satya")
    s = llm.invoke("A rose is pink")
    log.ph("Output", s)
    log.ph("LLM itself",llm)

def localTest():
    log.ph1("Starting local test")
    testHelloWorldLLM()
    log.ph1("End local test")

if __name__ == '__main__':
    localTest()