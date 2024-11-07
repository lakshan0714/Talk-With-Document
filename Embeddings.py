import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceBgeEmbeddings


class Embedding:

    def __init__(self,model_name = "BAAI/bge-large-en-v1.5",
                 model_kwargs = {'device': 'cpu'},
                 encode_kwargs = {'normalize_embeddings': True},
                 collection_name="Vector_DB"):
        
        self.model_name=model_name
        self.model_kwargs=model_kwargs
        self.encode_kwargs=encode_kwargs
        self.collection_name = collection_name



        self.embeddings = HuggingFaceBgeEmbeddings(
            model_name=self.model_name,
            model_kwargs=self.model_kwargs,
            encode_kwargs=self.encode_kwargs,
        )

    

    def Create_Embeddings(self,PDF_path:str):

        if not os.path.exists(PDF_path):
            raise FileNotFoundError("File does not exsist")
        
        loader=PyPDFLoader(PDF_path)
        Docs=loader.load()

        text_splitter=RecursiveCharacterTextSplitter(
            chunk_size=1000,chunk_overlap=250

        )

        splits=text_splitter.split_documents(Docs)

        if not splits:
            raise ValueError("No Text Chunks Were Created")
        
        try:
            Vector_DP=FAISS.from_documents(splits , self.embeddings)
            Vector_DP.save_local("faiss_local")
        
        except Exception as e:
            raise ConnectionError(f"{e}")
        
        return "Vector Database Created Succesfully"


        
     

    




