from utility_functions import generate_answers, generate_multiple_answers, answering_cleaning, change_language, reformulate_answer
from memory import inject_memory
from langchain_huggingface import HuggingFaceEmbeddings
import numpy as np
import lancedb
from langdetect import detect
from langchain_community.vectorstores import LanceDB
from constats import nc_query

def answer_generation(memory_decision, original_question, memory, llm_model_id, embedding_model_id, rag_db_path):

    db_connection = lancedb.connect(rag_db_path)
    embedding_model = HuggingFaceEmbeddings(model_name = embedding_model_id)
    db = LanceDB(connection = db_connection,
                  embedding = embedding_model)
    
    embedding_nc=np.array(embedding_model.embed_query(nc_query))

    original_question_lang = detect(original_question)
    cLanguage_question = change_language(original_question)
    if memory_decision =="1" and memory != []: 
        question, memory_string = inject_memory(cLanguage_question, memory, 4, llm_model_id)
        multiple_answers = generate_multiple_answers(question, db, 
                                                     memory= memory_string, 
                                                     llm_model_id = llm_model_id)
    else:
        question = cLanguage_question
        multiple_answers = generate_multiple_answers(question, db,
                                                      memory="", 
                                                      llm_model_id = llm_model_id)

    multiple_answers = answering_cleaning(multiple_answers, embedding_model, embedding_nc)
    final_context, time_chain_2, answer = generate_answers(original_question, multiple_answers, llm_model_id)
    answer = reformulate_answer(answer[0]["text"], original_question_lang)
    memory.append("Human question: "+ original_question)
    memory.append("AI answer: " + answer)

    return answer, memory

