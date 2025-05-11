from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from templates import memory_template

def reformulation_memory(memory,k):
    string_mem="\n"
    size=len(memory)
    i=0
    if size<k*2:
        for interaction in memory:
            string_mem=string_mem+interaction+"\n"
    else:
        for i in range(size-k*2,size):
            string_mem=string_mem+memory[i]+"\n"
            i=i+1
    return string_mem
            
def inject_memory(original_quesion, memory, k, llm_model_id):
    memory = reformulation_memory(memory,k)
    MEMORY_PROMPT = PromptTemplate.from_template(memory_template)

    llm = ChatOpenAI(model_name=llm_model_id, temperature=0.0)
    chain = LLMChain(llm=llm, prompt=MEMORY_PROMPT)
    inputs = [{"or_question":original_quesion, "chat_history":memory}]
    question = chain.apply(inputs)[0]["text"]

    return question, memory




    