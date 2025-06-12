from langchain.prompts import PromptTemplate
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain
from sqlalchemy.exc import SQLAlchemyError
from database import engine
from sqlalchemy import text
from sqlalchemy.orm import Session
import re

# 🧠 Initialize SQL database object
db = SQLDatabase(engine)

# 💬 LLM
llm = ChatOpenAI(temperature=0, model="gpt-4")

# 🧱 SQL Prompt Template (just generate SQL, don’t execute)
_SQL_PROMPT = PromptTemplate(
    input_variables=["input", "table_info"],
    template="""
Given an input question, generate a syntactically correct PostgreSQL query to run.

Only use the tables and columns listed below:
{table_info}

Question: {input}
SQLQuery:
""",
)

# 🔗 LLM Chain to generate SQL
sql_llm_chain = LLMChain(llm=llm, prompt=_SQL_PROMPT, verbose=True)

# ✅ Run SQL manually after cleaning
def run_sql_chain(question: str):
    try:
        # Step 1: Get table info from LangChain’s database tool
        table_info = db.get_table_info()

        # Step 2: Generate SQL using LLMChain
        sql_response = sql_llm_chain.invoke({
            "input": question,
            "table_info": table_info
        })

        raw_sql = sql_response["text"]

        # Step 3: Clean the generated SQL
        sql_text = raw_sql.strip()
        if (sql_text.startswith('"') and sql_text.endswith('"')) or \
           (sql_text.startswith("'") and sql_text.endswith("'")):
            sql_text = sql_text[1:-1]

        sql_text = re.sub(r";\s*LIMIT", r" LIMIT", sql_text, flags=re.IGNORECASE)
        sql_text = sql_text.rstrip(";")

        print("✅ Cleaned SQL to execute:", sql_text)

        # Step 4: Execute manually using SQLAlchemy
        with Session(engine) as session:
            result = session.execute(text(sql_text)).fetchall()

        if not result:
            return "No records found."

        # Step 5: Format result
        return "\n".join(str(row) for row in result)

    except SQLAlchemyError as e:
        print("❌ SQLAlchemy Error:", str(e))
        return "There was an error executing the SQL query."

    except Exception as e:
        print("❌ Unexpected Error:", str(e))
        return "An unexpected error occurred during query processing."
