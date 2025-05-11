from answer_geneartion import answer_generation
from dotenv import load_dotenv
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(dotenv_path= os.path.join(CURRENT_DIR,".env"))
EMBEDDING_MODEL_ID = os.getenv("EMBEDDING_MODEL_ID")
LLM_MODEL_ID = os.getenv("LLM_MODEL_ID")
PATH_DB_OUTPUT = os.getenv("PATH_DB_OUTPUT")

if __name__ == "__main__":

    print("Decide if you want memory chatbot or not, press 1 for memory, 2 without it")
    memory_decision = input()
    memory = []
    while True:
        print("\n")
        print("Insert a question to the chatbot in any language")
        original_question = input()
        answer, memory = answer_generation(memory_decision, original_question,
                                          memory, LLM_MODEL_ID, EMBEDDING_MODEL_ID,
                                          PATH_DB_OUTPUT )
        print("\n")
        print(answer)
        


    



     

    


