
from baselib import baselog as log
from customllms import custom_fb_hf_llm as CustomLLM

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


log.turnOffDebug()

question = "Who won the FIFA World Cup in the year 1994? "

template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate(template=template, input_variables=["question"])

llm = CustomLLM.FB_HFCustomLLM(n=5,name="FB LLM")

llm_chain = LLMChain(prompt=prompt, llm=llm)

reply = llm_chain.invoke({"question":question})
log.uph("Final answer from LLM", reply)