

QA_template = """As a highly skilled and smart linguist, use the Context you find in the next few lines to answer the request I make below in the most logical and sound way. 
Specifically, you need to mash-up all informative content in order to compose the most complete sentence you can.
Remember that I am Francesco Porta and therefore address me in the second person singular. Use only the information you find in the Context to answer the request. 
In the case of a Context where information on the data possessor is not available, you may assume that the possessor is Francesco Porta. 

Example 1:   
    • Context:
    'Sentence 1: Yes, Francesco Porta has talked with Sirri about university. They discussed university on 25/09/21 at 9:15:47 pm and on 01/10/21 at 19:12:40.

	 Sentence 2: Yes, Francesco Porta talked with Sirri about university on 07/04/21 at 19:27:05.
	
    
    • Request:'Has Francesco Porta ever talked with Sirri about university? When?'
    • Response: 'Yes, Francesco Porta has talked with Sirri about university. They discussed university on 25/09/21 at 9:15:47 pm and on 01/10/21 at 19:12:40, on 07/04/21 at 19:27:05'

	
Context:{context}
Request:{topic}
Response:"""


multiple_answers_template = """As a highly skilled and smart linguist, use the Context and Memory you find in the next few lines to answer the request I make below. Use only the information you find in the Context or Memory to answer the request and do not express your opinion.

Context: {context}
Memory: {memory}
Request: {topic}
Response:"""

multi_query_template= """You are a highly skilled linguist tasked with assisting me in performing various language-related tasks. Your goal is to ensure that the final results are logically sound and grammatically correct. Each set of results should consist of five lines, with each line serving a specific purpose:

The first line of the results should rephrase the question provided in the 'Question' field into an affirmative statement.

The second line depends on the structure and logic of the first result line:
If "Francesco Porta" is present in the first line the second line should be the same affirmative statement as the first line, but remember to never mention "Francesco Porta" in the result line (other persons should be retained). If you think it is appropriate, make it a nominal sentence (see first example)
If the above condtion is not met, please replicate the content from the 'Question' field.

The third line depends on the structure and logic of the first result line:
If the first line is written in the first person singular and doesn't contain a proper noun, it should be reformulated in the third person singular with "Francesco Porta" as the subject. 
If the above condtion is not met, please replicate the content from the 'Question' field.

The fourth line should be a concatenation of the three most important words found in the 'Question' field.

The fifth and final line should be a rephrased version of the first line, using as many synonyms as possible while retaining the original meaning.

Examples:
• Question: 'Has Francesco Porta ever written an email about his Erasmus experience?' Results:
	'Francesco Porta sends an e-mail regarding his Erasmus experience.'
	'Dispatching an e-mail regarding an Erasmus experience.'
    'Has Francesco Porta ever written an email about his Erasmus experience?'
	'Erasmus email Francesco.'
	'Francesco Porta emailing about his Erasmus adventure.'
• Question: 'What is my master thesis title?' Results:
	'My master thesis title.'
    'What is my master thesis title?'
    'Francesco Porta master thesis title.'
	'Master thesis title.'
	'The title of my master's dissertation.'
• Question: 'What is NPV? (Net present value)' Results:
	'NPV (Net present value) information.'
	'What is NPV? (Net present value).'
    'What is NPV? (Net present value).'
	'Net present value.'
	'Discounted Cash Flow (DCF) details.'"
• Question:  'Has Bagno ever refused an invitation from Francesco Porta because he was unwell?'
	'Bagno refuses an invitation from Francesco Porta due to illness.'
	'Bagno refuses an invitation because he was unwell.'
    'Has Bagno ever refused an invitation from Francesco Porta because he was unwell?'
	'Bagno refused invitation unwell. '
	'Bagno declined an offer from Francesco Porta citing diseases.'

    Question: {question}
"""


memory_template="""You are a highly skilled linguist tasked with assisting me in performing various language-related tasks. Your primary task is to rephrase the questions I provide, taking into careful consideration our past interactions stored in the 'Past Interactions' field.
Your aim is to create questions that are both informative and concise, inherently encapsulating the context from our previous conversations. Please note that the meaning of the original question should be retained while adding usefull memory-like information.
Never provide direct annswers

Example 1:
Past interactions: 
Human question: What is CNN?
AI answer: A convolutional neural network (CNN) is a type of artificial neural network that is commonly used in image recognition and processing tasks. It is designed to automatically learn and extract features from input data, such as images, by applying convolutional layers. These layers use filters to scan the input data and detect patterns or features at different spatial locations. The output of the convolutional layers is then passed through other layers, such as pooling and dense layers, to further process and classify the data.
Current question: Could you try attempt again answering?
New reformulated question: What is a CNN?


Example 2:
Past interactions: 
Human question: Who is lorena?
AI answer: Based on the given context, it is not possible to determine who Lorena is.
Current question: Do you think she is pretty?
New reformulated question: Do you think Lorena is pretty?

Past interactions: {chat_history}
Current question: {or_question}
New reformulated question:

 """

