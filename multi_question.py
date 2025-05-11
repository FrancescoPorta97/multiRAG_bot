from templates import multi_query_template
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List

class LineList(BaseModel):
    # "lines" is the key (attribute name) of the parsed output
    lines: List[str] = Field(description="Lines of text")


class LineListOutputParser(PydanticOutputParser):
    def __init__(self) -> None:
        super().__init__(pydantic_object=LineList)

    def parse(self, text: str) -> LineList:
        lines = text.strip().split("\n")
        return LineList(lines=lines)

def multi_query_generation (original_question, llm_model_id):
    llm = ChatOpenAI(model_name=llm_model_id, temperature=0.45)
    QUERY_PROMPT = PromptTemplate(
    input_variables = ["question"],
    template = multi_query_template
)
    output_parser = LineListOutputParser()

    multi_query_chain = QUERY_PROMPT | llm
    questions = multi_query_chain.invoke(original_question).content.split('\n')
    final_questions = ["Represent this sentence for searching relevant passages: "+ x for x in questions]
    return final_questions

def get_multi_documents(queries,db):

    final_docs=[]
    final_docs_cont=[]
    retriever=db.as_retriever(search_type="similarity",search_kwargs={'k': 2})
    for query in queries:
        final_docs = final_docs + retriever.get_relevant_documents(query=query)

    [final_docs_cont.append(x.page_content) for x in final_docs]
    un_final_docs=[]
    un_final_docs_cont=[]
    i=0    
    for content in final_docs_cont:
        if content not in un_final_docs_cont:
            un_final_docs.append(final_docs[i])
            un_final_docs_cont.append(content)
        
        i=i+1
    
    return un_final_docs


    
    



    