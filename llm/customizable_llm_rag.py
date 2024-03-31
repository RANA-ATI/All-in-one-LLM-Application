import chromadb
import replicate
from pypdf import PdfReader
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    SentenceTransformersTokenTextSplitter,
)
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

replicate = replicate.Client(api_token='<your_replicate_api_token>') # Put your api_token

chroma_client = chromadb.Client()
chroma_collection = None

def initialize_chroma_collection():
    global chroma_collection
    if chroma_collection is None:
        embedding_function = SentenceTransformerEmbeddingFunction()
        chroma_collection = chroma_client.create_collection("rag-llm4", embedding_function=embedding_function)

def embeddingsCreationStoring(file_paths):
    global chroma_collection
    initialize_chroma_collection()

    pdf_texts = []
    for file_path in file_paths:
        reader = PdfReader(file_path)
        pdf_texts.extend([p.extract_text().strip() for p in reader.pages])

    # Filter the empty strings
    pdf_texts = [text for text in pdf_texts if text]

    character_splitter = RecursiveCharacterTextSplitter(
        # It will split on the basis of these below characters like newline etc
        separators=["\n\n", "\n", ". ", " ", ""],
        # If after splitting at separators, it got a big length then it will break down into chunk size of 1000 characters maximum
        chunk_size=1000,
        chunk_overlap=0,
    )
    
    character_split_texts = character_splitter.split_text("\n\n".join(pdf_texts))

    token_splitter = SentenceTransformersTokenTextSplitter(
        chunk_overlap=0, tokens_per_chunk=256
    )  # tokens_per_chunk is context window which means that it one chunk would have 256 tokens

    # We shall use all the chunks made by character text splitter and we are resplitting them using the token text splitter
    token_split_texts = []
    for text in character_split_texts:
        token_split_texts += token_splitter.split_text(text)

    ids = [str(i) for i in range(len(token_split_texts))]

    chroma_collection.add(ids=ids, documents=token_split_texts)

    return "Stored Embeddings in Vector DB"


def rag(query):
    print(chroma_collection)
    # Here chroma automatically embeds using the embedding function we have used above the query and give retrieved documents
    results = chroma_collection.query(query_texts=[query], n_results=5)
    retrieved_documents = results["documents"][0]

    information = "\n\n".join(retrieved_documents)

    output = replicate.run(
        # Let this remain the same no matter if your api_token expires.
        "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
        input={
            "prompt":f"You are a helpful expert research assistant. Your users are asking questions about information contained in reports or files."
                "You will be shown the user's question, and the relevant information from the files or reports. Answer the user's question using only this information." 
                f"Question: {query}. \n Information: {information}",
            }
    )

    ans = []
    for item in output:
        ans.append(item)

    str1 = ''.join(str(e) for e in ans)

    # System Prompt
    return str1