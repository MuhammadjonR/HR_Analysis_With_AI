import os
import chromadb
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever

class CVDatabase:
    def __init__(self, folder_path="./cv_folder"):
        self.folder_path = folder_path
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")

    def build_or_load(self):
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)
            return None


        loader = DirectoryLoader(self.folder_path, glob="./*.pdf", loader_cls=PyPDFLoader)
        docs = loader.load()
        
        if not docs:
            print("Papkada PDF fayllar topilmadi.")
            return None

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
        chunks = splitter.split_documents(docs)

        client = chromadb.EphemeralClient() 
        
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            client=client,
            collection_name="cv_collection"
        )

        v_retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
        bm25_retriever = BM25Retriever.from_documents(chunks)
        bm25_retriever.k = 5
        
        return EnsembleRetriever(
            retrievers=[bm25_retriever, v_retriever], 
            weights=[0.3, 0.7]
        )