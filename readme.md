# Chatbot with Memory and Multi-Question Retrieval

This project implements a chatbot capable of answering questions by leveraging multi-query generation, memory injection, and retrieval-augmented generation (RAG). It supports any language, automatically translating inputs and outputs when needed.

---

## **Quick Start**

### 1. Clone the Repository

```bash
git clone <repository_url>
cd <repository_folder>
```

### 2. Create a .env file based on the provided .env.dist:

```bash
PATH_FILES_INPUT=./data/input_files       # Path to the documents for building the vector database
PATH_DB_OUTPUT=./data/vector_db            # Output path for the vector DB
EMBEDDING_MODEL_ID=sentence-transformers/all-MiniLM-L6-v2   # Hugging Face embedding model original model used in env.dist
LLM_MODEL_ID=gpt-4-turbo                   # OpenAI model name (or any supported LLM), original model used in env.dist
```

### 3. Install Dependencies

Ensure you have Python 3.8+ and install the required libraries (Python currently used in local machine is 3.10.16):

```bash
pip install -r requirements.txt
```

### 4. Prepare the Vector Database

Run the script to process your input documents:

```bash
python feed_vector_db.py
```

This will load, split, and translate documents if needed, and store them in the vector database.

### 5. Run the Chatbot

```bash
python main.py
```

You'll be asked whether to enable memory:

1 → Chatbot will remember past interactions.

2 → Stateless chatbot.

Then, start asking your questions directly.
(The chatbot will handle translations automatically.)

---

### Main Functionalities

Language-Aware Chatbot: Automatically detects and translates inputs and outputs.

Multi-Query Retrieval: Generates multiple reformulations of a question to improve retrieval quality.

Memory Injection: Optionally include past interactions to provide more contextual responses.

Similarity Filtering: Filters retrieved contexts to ensure diversity and relevance.

Easy Configuration: Just edit the .env file to change models and paths.

### Project Structure

```bash
├── main.py               # Entry point to run the chatbot
├── feed_vector_db.py     # Script to populate the vector database
├── answer_geneartion.py  # Main logic for answer generation
├── utility_functions.py  # Supporting functions for QA and processing
├── memory.py             # Functions for memory management
├── multi_question.py     # Multi-query generation and retrieval
├── templates.py          # Prompt templates for LLMs
├── constats.py           # Constants for fallback answers
└── .env.dist             # Example environment configuration
```

### Important Notes

This project uses external services (like OpenAI or Hugging Face). Make sure your API keys are properly set in your environment.

Only documents from PATH_FILES_INPUT are used for building the chatbot knowledge base.

The chatbot always tries to respond in a fact-based manner, returning fallback responses if no relevant information is found.

```

```
