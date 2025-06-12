# rag/vector_store.py

import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from sqlalchemy import create_engine, MetaData

# Step 1: Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
db_url = os.getenv("DATABASE_URL")

# Step 2: Check for API key
print(f"🔑 API key from env (length {len(openai_api_key or '')}): '{openai_api_key}'")
if not openai_api_key:
    raise ValueError("❌ OPENAI_API_KEY not found in environment variables.")
if not db_url:
    raise ValueError("❌ DATABASE_URL not found in environment variables.")

def create_vector_store():
    # Step 3: Connect to database and reflect schema
    engine = create_engine(db_url)
    metadata = MetaData()
    metadata.reflect(bind=engine)

    # Step 4: Convert table schemas to documents
    documents = []
    for table_name, table in metadata.tables.items():
        columns = [col.name for col in table.columns]
        schema_text = f"Table: {table_name}\nColumns: {', '.join(columns)}"
        documents.append(Document(page_content=schema_text, metadata={"table": table_name}))
        print(f"📄 Document created for table: {table_name}")

    # Step 5: Create vector store
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vector_store = FAISS.from_documents(documents, embeddings)
    vector_store.save_local("faiss_index")
    print("✅ FAISS vector store created and saved!")

if __name__ == "__main__":
    create_vector_store()
