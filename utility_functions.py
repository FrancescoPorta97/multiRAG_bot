from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from textblob import TextBlob
import time
import asyncio
from templates import QA_template, multiple_answers_template
from langdetect import detect
from multi_question import multi_query_generation, get_multi_documents
from scipy.spatial import distance
import numpy as np

def generate_answers(or_question, multiple_answers, llm_model_id):
    multiple_answers = [multiple_answers[x] for x in range(len(multiple_answers))]
    QA_PROMPT = PromptTemplate.from_template(QA_template)
    llm = ChatOpenAI(model_name=llm_model_id, temperature=0.0)
    chain=LLMChain(llm=llm, prompt=QA_PROMPT)

    final_context=""
    i=1
    for answer in multiple_answers:
        final_context=final_context+"Sentence "+str(i)+": "+answer+"\n\n"
        i=i+1
    
    time_chain = time.time()
    inputs = [{"context":final_context, "topic":or_question}]
    result=chain.apply(inputs)
    time_chain = time.time()-time_chain            

    return final_context, time_chain, result

def generate_multiple_answers(original_question, db, memory, llm_model_id):
    multiple_answer_prompt = PromptTemplate.from_template(multiple_answers_template)
    llm = ChatOpenAI(model_name=llm_model_id, temperature=0.0)
    chain = LLMChain(llm=llm, prompt=multiple_answer_prompt)
    queries = multi_query_generation(original_question, llm_model_id)
    docs = get_multi_documents(queries, db)
    inputs = [{"context": doc.page_content,"memory": memory, "topic": original_question} for doc in docs]

    async def main_test():
        result = await chain.aapply(inputs)
        return result

    result =asyncio.run(main_test())
                    
    return result

def answering_cleaning(answers, embedding, embedding_nc):
    min_similarity=1

    answers=[answers[x]["text"] for x in range(len(answers))]
    embedding_answers=[]
    return_answers=[]
    if type(answers)==list:
        for answer in answers:
            embedding_answer=np.array(embedding.embed_query(answer))
            embedding_answers.append(embedding_answer)
            cosine_sim=1-distance.cosine(embedding_nc,embedding_answer)
            if cosine_sim< min_similarity:
                min_similarity=cosine_sim
                final_answer_1=answer
                final_embedding_1=embedding_answer
        
        return_answers.append(final_answer_1)
        embedding_answers= [arr.tolist() for arr in embedding_answers]
        final_embedding_1 = final_embedding_1.tolist()
        embedding_answers.remove(final_embedding_1)
        embedding_answers= [np.array(lista) for lista in embedding_answers]
        final_embedding_1=np.array(final_embedding_1)
        answers.remove(final_answer_1)
        
        i=0
        for ans in embedding_answers:
            sim_2_nc=1-distance.cosine(embedding_nc,ans)
            sim_1_2=1-distance.cosine(final_embedding_1, ans)
            if sim_1_2/sim_2_nc > 1.5:
                return_answers.append(answers[i])
            i=i+1
        return return_answers
    else:
        return answers

def change_language(question):

    question_lang = detect(question)
    if question_lang != "en":
        try:
            blob = TextBlob(question)
            question = blob.translate(from_lang=question_lang, to='en').string
        except:
            print("I couldn't translate the question")

    return question

def reformulate_answer(answer, answer_lang):

    try:
        blob = TextBlob(answer)
        answer = blob.translate(from_lang='en', to=answer_lang).string
    except:
        print ("I could not reformulate the answer")

    return answer
        


                


        

                


