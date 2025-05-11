import os
import lancedb
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import LanceDB
from textblob import TextBlob
from langdetect import detect
import string
import re

def contains_only_punctuation(s):
    pattern = f'^[{re.escape(string.punctuation)}]+$'
    return bool(re.match(pattern, s))

#env
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(dotenv_path= os.path.join(CURRENT_DIR,".env"))
PATH_FILES_INPUT = os.getenv("PATH_FILES_INPUT")
EMBEDDING_MODEL_ID = os.getenv("EMBEDDING_MODEL_ID")
PATH_DB_OUTPUT = os.getenv("PATH_DB_OUTPUT")

size_adapter = 3.2
overlap_adapter = 3.5 
embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_ID)
loader = DirectoryLoader(path = PATH_FILES_INPUT)

raw_documents = loader.load()
print("Loading_executed")

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000*size_adapter, chunk_overlap=100*overlap_adapter)
documents = text_splitter.split_documents(raw_documents)
documents = [doc for doc in documents if  not contains_only_punctuation(doc.page_content)]
print("Finished splitting")
print("Number of document: "+str(len(documents)))

db_connection = lancedb.connect(PATH_DB_OUTPUT)

i,j = 0,0
for doc in documents:
    
    source = doc.metadata['source']
    doc_lang = detect(doc.page_content)

    if doc_lang != "en":
        try:
            blob = TextBlob(doc.page_content)
            doc.page_content=blob.translate(from_lang=doc_lang, to='en').string
            j = j+1
        except:
            i = i+1
            print("The number of not translated documents is "+str(i))

    if "pdf" in source:

        title = source.split("\\")[-1].split(".")[0]
        doc.page_content= "Contextual information: " + title+ "\n"+ doc.page_content
  
print("Splitting_executed")
db = LanceDB.from_documents(documents, embedding_model, connection=db_connection)
print("DB_charged with loader ")

print("End")

