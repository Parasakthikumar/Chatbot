import os
from langchain_openai import OpenAIEmbeddings  # or langchain_community if not switched yet
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def load_vector_store():
    embeddings = OpenAIEmbeddings()
    db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    return db

def create_qa_chain():
    db = load_vector_store()
    retriever = db.as_retriever()
    llm = ChatOpenAI(model_name="gpt-4", temperature=0)
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    return qa

if __name__ == "__main__":
    qa_chain = create_qa_chain()
    query = "Explain the asset maintenance process"
    result = qa_chain.run(query)
    print("Answer:", result)
