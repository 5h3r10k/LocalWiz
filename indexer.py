import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

# Configurable variables
RAW_DATA_DIRECTORY = "./scraped_pages"
EMBEDDINGS_DIRECTORY = "./db"
MODEL_NAME = "nomic-embed-text:latest"
CHUNK_SIZE = 1500
CHUNK_OVERLAP = 300
SHOW_PROGRESS = True
GLOB_PATTERN = "**/*.txt"

# load documents from directory of scraped pages
loader = DirectoryLoader(RAW_DATA_DIRECTORY, glob=GLOB_PATTERN)
print("Directory loaded into loader")
documents = loader.load()
print(f"Number of documents loaded: {len(documents)}")

# create embeddings instance
embeddings = OllamaEmbeddings(model=MODEL_NAME, show_progress=SHOW_PROGRESS)

# create text splitter instance
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    add_start_index=True,
)

# Split documents into chunks
texts = text_splitter.split_documents(documents)

# Create embeddings directory if it doesn't exist
if not os.path.exists(EMBEDDINGS_DIRECTORY):
    os.makedirs(EMBEDDINGS_DIRECTORY)

# Create vector store
vectorstore = Chroma.from_documents(
    documents=texts,
    embedding=embeddings,
    persist_directory=EMBEDDINGS_DIRECTORY,
)

print("Vector store created and persisted")