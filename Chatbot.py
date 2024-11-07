from Embeddings import Embedding
from langchain_community.vectorstores import FAISS
from langchain_mistralai import ChatMistralAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
import os
from dotenv import load_dotenv
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
import traceback
from dotenv import load_dotenv



class Chatbot:

    def __init__ (self, model_name ="BAAI/bge-large-en-v1.5",
            model_kwargs = {"device": "cpu"},
            encode_kwargs = {"normalize_embeddings": True},
            collection_name="Vector_DB",
            llm_model="mistral-large-latest"        
    ):
    
        
        self.model_name=model_name
        self.model_kwargs=model_kwargs
        self.encode_kwargs=encode_kwargs
        self.collection_name = collection_name
        self.llm_model=llm_model

       
       
     


        self.embeddings = HuggingFaceBgeEmbeddings(
            model_name=self.model_name,
            model_kwargs=self.model_kwargs,
            encode_kwargs=self.encode_kwargs)
    

        self.new_vector_store = FAISS.load_local(
                           "faiss_local" , self.embeddings, allow_dangerous_deserialization=True)
        
        self.retriever=self.new_vector_store.as_retriever()

        
        self.llm=ChatMistralAI(
            model=self.llm_model,
            api_key="j3Equsw7oun87HjYroXXnFJ9LvWcUoDE"

            #temperature=0.2
            
        )

        self.system_prompt = (
    "Use the given context to answer the question. "
    "If you don't know the answer, say you don't know. "
    "Provide page no of the pdf related to answer. "
    "Context: {context}"
)
        self.prompt = ChatPromptTemplate.from_messages(
    [
        ("system", self.system_prompt),
        ("human", "{input}"),
    ]
)
        self.question_answer_chain = create_stuff_documents_chain(self.llm, self.prompt)
        self.chain = create_retrieval_chain(self.retriever, self.question_answer_chain)


        

    def get_response(self,query):
        try:
            response=self.chain.invoke({"input":query})
            return response["answer"]
        
        except Exception as e:

            traceback.print_exc()
            return f"Couldn't process the response: {e}"
        


'''
chat=Chatbot()
x=chat.get_response(query="How to adjust the temprature?")
print(x)
'''









