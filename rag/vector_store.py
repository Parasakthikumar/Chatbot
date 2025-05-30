# rag/vector_store.py

import os
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from rag.schema_doc import schema_docs
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def create_vector_store():
    embeddings = OpenAIEmbeddings()
    docs = [Document(page_content=desc, metadata={"table": table}) for table, desc in schema_docs.items()]
    db = FAISS.from_documents(docs, embeddings)
    db.save_local("faiss_index")
    print("✅ FAISS vector store created and saved!")

if __name__ == "__main__":
    create_vector_store()
