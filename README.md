# LocalWiz

A fully localized RAG-based solution for querying and interpreting documents in a chatbot environment.


## Background

My initial project, UniWiz, was a chatbot that could answer questions based on a knowledge base. In UniWiz, API calls are made to the OpenAI API to generate embeddings and responses. This allows for powerful processing but presents a concern when it comes to privacy and data security. With the OpenAI API approach, using private data for the knowledge base would introduce a security risk, as the data would be sent to the OpenAI servers for processing.

To address this concern, I began exploration on a fully localized solution. This project is just that; a fully local solution for querying and interpreting a knowledge base without external API calls. The project is built on the RAG (Retrieval-Augmented Generation) framework, which is a combination of a retriever and a generator. The retriever is responsible for finding relevant documents, and the generator is responsible for generating responses based on the retrieved documents.

## Project Stack

The project is built using the following technologies:

- Python runtime (3.12)
- [Ollama](https://ollama.com/)

## Project Structure

This application consists of 3 major components:
- Scraper
- Indexer
- Retriever

### Scraper

The scraper is a supplemental component that allows for the knowledge base to be built based on an existing website online. The scraper is built using libraries such as `BeautifulSoup` and `requests` to scrape the website and store the data in a directory. Advanced whitelisting and blacklisting options are provided. The scraper is a one-time use component that is used to build the knowledge base and can be reused if the knowledge base needs to be updated.

### Indexer

The indexer is responsible for indexing the documents in the knowledge base into an embeddings vector store. LangChain is used to preprocess the documents and break them into equally sized chunks for the embeddings model.

The embeddings model can be locally run usinng Ollama. The embeddings model in use for this project is `nomic-embed-text:latest` which can be downloaded and run using guides from Ollama. The embeddings model is used to generate embeddings for the documents in the knowledge base. These embeddings, which are stored in a vector store (Chroma), are used by the retriever to find relevant documents.

### Retriever

The retriever is responsible for finding relevant documents based on the user query. The retriever is the chatbot environment which, based on the user's query, retrieves the most relevant documents from the knowledge base and generates a response. An LLM is required for this stage, and the specific model being used in this project is Google's `gemma2:9b` through Ollama.


## Running the Project

To run the project, follow these steps:

1. Clone the repository to your local machine. It is recommended to clone somewhere local, as the scraping will produce many files and may take up significant disk space.
2. Install the required dependencies using `pip3 install -r requirements.txt`.
3. Install Ollama and the required models. The models required are `nomic-embed-text:latest` and `gemma2:9b`. The embeddings model can be downloaded from the Ollama website and run locally. The LLM model can also be downloaded from the Ollama website and run locally. Please refer to the Ollama documentation for more information.
4. Place the root URL of the website you want to scrape in the isolated `root_url` variable in the `scraper.py` file. Also set the 'allowed_urls' and 'blocked_urls' variables to whitelist and blacklist domain starters respectively. The `allowed_urls` variable must not be empty, or else nothing will be scraped.
5. Run the scraper using `python3 scraper.py`. This will scrape the website and store the data in a new directory `scraped_pages`.
6. Run the indexer using `python3 indexer.py`. This will index the documents in the `scraped_pages` directory and store the embeddings in the `db` directory.
7. Run the retriever using `python3 retriever.py`. This will start the chatbot environment, and you can ask questions based on the knowledge base you have built.


## Ending Notes

This is a prototype of a tool that can answer questions on secure knowledge bases. Secure and efficient answers for sensitive documents such as legal documents, medical records, and more can be provided using this tool. 

Potential use cases:
- Legal document interpretation (searching for a specific clause in a contract)
- Medical record interpretation (understanding all instances of a specific diagnosis in past patients)
- Enterprise document search (searching for how-to guides that can be scattered across multiple documents)
- Personal document search (asking for a list of all your expenses in the past year)