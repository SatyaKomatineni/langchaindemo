"""
*************************************************
* About
*************************************************
1. Should use HF local transformer for embedding
2. Should use HF pulic TGI as the text infernce
3. Uses Chromadb local
*************************************************
"""

"""
*************************************************
* Base libs
*************************************************
"""
from baselib import baselog as log
from customllms.custom_fb_hf_llm import FB_HFCustomLLM
from typing import Tuple
"""
*************************************************
* LangChain and HF
*************************************************
"""
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from vectorlib.database_repo import DatabaseRepo
from vectorlib.database import Database
from langchain_core.vectorstores import VectorStore
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.language_models.llms import LLM

"""
*************************************************
* Local stuff: siblings
*************************************************
"""
from ui.wizard import Wizard

"""
*************************************************
* Class Wizard
*************************************************
log.turnOffDebug()
"""
class LangChainHFWizard2(Wizard):
    llm: LLM
    prompt: PromptTemplate
    retriever: VectorStoreRetriever

    def __init__(self):
        #get the prompt
        self.prompt = self._getTemplate()

        #get the llm HF Public TGI LLM
        self.llm = DatabaseRepo.get_hf_LLM()

        #vector db stuff
        db: VectorStore = DatabaseRepo.getSOFUDatabase2().get()
        self.retriever = db.as_retriever(search_kwargs={"k": 3})
        self.chain = _getChain(self.llm, self.prompt, self.retriever)
        
    def _getTemplate(self) -> PromptTemplate:    
        template = """Instructions: Use only the following context to answer the question.
Context: {context}
Question: {question}
"""
        prompt = PromptTemplate(template=template, input_variables=["context", "question"])
        return prompt
    
    #
    # Interface
    def question(self, question: str) -> Tuple[str, str]:
        answer = self.chain.invoke(question)
        return (question, answer)

"""
*************************************************
* Some utility funcs
*************************************************
"""
def _getChain(llm: LLM, prompt: PromptTemplate, retriever: VectorStoreRetriever):
    chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
    return chain


def test():
    wizard = LangChainHFWizard2()
    q, a = wizard.question("What is the Chips Act?")
    log.ph("Final answer", a)

def localTest():
    #log.turnOffDebug()
    log.ph1("Starting local test")
    test()
    log.ph1("End local test")

if __name__ == '__main__':
    localTest()