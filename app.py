
from baselib import baselog as log
from customllms.custom_fb_hf_llm import FB_HFCustomLLM


from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from vectorlib.database import DatabaseRepo
from vectorlib.database import Database
from langchain_core.vectorstores import VectorStore
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

log.turnOffDebug()

"""
*************************************************
* Prep the template
*************************************************
"""
template = """Instructions: Use only the following context to answer the question.

Context: {context}
Question: {question}
"""
prompt = PromptTemplate(template=template, input_variables=["context", "question"])

"""
*************************************************
* question
*************************************************
"""
#question = "What is the CHIPS Act?"
question = "Who all are attending the state of the union? can you put their names in a list?"
#question = "what are the key topics covered in the state of the union?"

"""
*************************************************
* get the LLM
*************************************************
"""
llm = DatabaseRepo.get_fbhf_LLM()
db: VectorStore = DatabaseRepo.getSOFUDatabase().get()

retriever = db.as_retriever(search_kwargs={"k": 1})
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
output = chain.invoke(question)
log.uph("Final answer from LLM", output)