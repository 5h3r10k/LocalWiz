from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough

# Configurable variables
EMBEDDINGS_DIRECTORY = "./db"
MODEL_NAME = "nomic-embed-text"
LOCAL_LLM = 'gemma2:9b'
KEEP_ALIVE_DURATION = "3h"
MAX_TOKENS = 512
TEMPERATURE = 0
RETRIEVAL_K = 5

# Using OllamaEmbeddings to generate text embeddings with the specified model
embeddings = OllamaEmbeddings(model=MODEL_NAME, show_progress=False)

# initialize chroma db to source embeddings
db = Chroma(persist_directory=EMBEDDINGS_DIRECTORY,
            embedding_function=embeddings)

# creating the retriever and configuring it to use the similarity search with k=5
retriever = db.as_retriever(
    search_type="similarity",
    search_kwargs={"k": RETRIEVAL_K}
)

# Initialize the local language model with the specified parameters
llm = ChatOllama(model=LOCAL_LLM,
                 keep_alive=KEEP_ALIVE_DURATION,  # Keep the model alive for 3 hours
                 max_tokens=MAX_TOKENS,  # Max tokens for each response
                 temperature=TEMPERATURE)  # Temperature for deterministic responses

# Create a prompt template
# Defining a structured template for the input prompt to the language model
template = """<bos><start_of_turn>user\nYou are a helpful question and answer bot. Answer the question based only on the following context and extract a meaningful answer. \
Please write in full sentences with correct spelling and punctuation. If it makes sense to use lists, please use lists. \
If the context does not contain the answer, please respond that you are unable to find an answer. \

CONTEXT: {context}

QUESTION: {question}

<end_of_turn>
<start_of_turn>model\n
ANSWER:"""
prompt = ChatPromptTemplate.from_template(template)

# creating the RAG chain using LCEL (LangChain Expression Language)
# setup the chain of ops: retrieving context, formatting the prompt, generating answers
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
)

# function for streaming questions and answers
def ask_question(question):
    print("Answer:\n\n", end=" ", flush=True)
    # Stream the response in chunks for real-time display
    for chunk in rag_chain.stream(question):
        print(chunk.content, end="", flush=True)
    print("\n")

# main loop startup for asking questions
if __name__ == "__main__":
    while True:
        user_question = input("Ask a question (or type 'quit' to exit): ")
        if user_question.lower() == 'quit':
            break
        answer = ask_question(user_question)