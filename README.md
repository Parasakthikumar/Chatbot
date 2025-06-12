# 🧠 ERP Chatbot with Natural Language SQL Queries

This project is an intelligent **ERP-integrated chatbot** built using **FastAPI**, **PostgreSQL**, **LangChain**, **FAISS**, and **React.js** frontend. The bot can answer natural language queries about **company assets, maintenance logs, departments, employees, and vendors**, powered by a combination of:

- ✅ SQL query generation from user input
- ✅ Retrieval-Augmented Generation (RAG) for schema questions
- ✅ Redis caching for faster repeated queries
- ✅ FAISS vector search for document-based answers
- ✅ Typing-friendly conversation UI

---
The system is built using the following components:

- **FastAPI**: Used for building the REST API backend.
- **PostgreSQL**: Serves as the main relational database to store ERP data such as assets, employees, maintenance logs, departments, and vendors.
- **LangChain** + **OpenAI GPT-4**: Powers both SQL generation and schema-level question answering through a combination of LLMs and vector-based retrieval.
- **FAISS**: Used to create a vector store from documentation and table metadata, enabling Retrieval-Augmented Generation (RAG).
- **React.js (Vite)**: Frontend interface for user interaction with the chatbot.
- **Redis** (optional): Provides caching support to store frequent queries and reduce latency.

The chatbot supports:
- Executing real-time SQL queries based on user input.
- Providing responses for schema-related or metadata-level questions using FAISS-based retrieval.
- Maintaining short-term conversation context.
- Handling fuzzy input, including typo correction and synonym recognition.

## ⚙️ Tech Stack

| Layer            | Tools Used                               |
|------------------|-------------------------------------------|
| Frontend         | React.js (with Vite)                      |
| Backend API      | FastAPI                                   |
| AI Logic         | LangChain + OpenAI GPT-4                  |
| Vector Search    | FAISS                                     |
| Embeddings       | OpenAIEmbeddings                          |
| Database         | PostgreSQL (via SQLAlchemy & SQLModel)    |
| Caching          | Redis (optional)                          |

---

## 🏁 How to Run the Project

### 📦 Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL installed and running
- Redis (optional for caching)
- OpenAI API key
---
### 2. Create and Activate Virtual Environment

##bash##


python -m venv venv


venv\Scripts\activate  # On Windows
# OR on Mac/Linux
# source venv/bin/activate

3. Install Dependencies

    pip install -r requirements.txt

4. Set Up Environment Variables
   
    Create a .env file in the root directory:

    env

    OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxx

    DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/your_db_name

6. Create the Database and Tables

    python create_tables.py

7. Load Sample Data

    python load_data.py

8. Generate Vector Store (for schema RAG)

    python rag/vector_store.py

9. Start FastAPI Backend

    uvicorn main:app --reload

    The backend API will be available at:

    http://localhost:8000


💬 Chatbot Frontend (Optional)

    If you're using a React.js frontend (like Chatbot-UI):

Steps to Run:

    Navigate to the frontend folder or clone a separate UI repo.

Run the following commands:

**bash**
    npm install

    npm run dev

    Frontend will run at:

    http://localhost:8000/chat

✅ Supported Query Types

Type	Example Queries

Asset info & status	“What is the status of generator GNT-243?”

Maintenance history	“When was the last service done for AC A123?”

Vendor-asset mapping	“Which vendor supplied Laptop LAP-445?”

Employee or department info	“List employees from IT department.”

Schema-level questions	“What does the Assets table contain?”

🔁 Caching with Redis (Optional)

Enable Redis to speed up responses for repeated queries.

Redis must be running locally on the default port 6379.

🧠 Conversation Context + Fuzzy Matching

✅ Follow-up questions supported

e.g.: “What is his name?” after “Who repaired the generator?”


✅ Typo correction:

e.g.: “maintainance” → “maintenance”

✅ Enum/synonym mapping:

e.g.: “under repair” → “maintenance”

📃 Sample Data Includes


assets.csv

maintenance_logs.csv

vendors.csv

asset_vendor_links.csv

employees.csv, departments.csv

All available in the sample_data/ folder.
