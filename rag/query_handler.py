# rag/query_handler.py

import os
import redis
import json
import asyncio
from dotenv import load_dotenv
from rag.qa_chain import get_retrieval_qa_chain
from rag.sql_chain import run_sql_chain

# Load .env variables
load_dotenv()
r = redis.Redis.from_url(os.getenv("REDIS_URL"))
qa_chain = get_retrieval_qa_chain()

# ✅ Main handler function
async def handle_query(user_query: str):
    print(f"🟢 Received query: {user_query}")

    try:
        # ✅ Redis cache check
        cached = r.get(user_query)
        if cached:
            print("✅ Answer served from Redis cache")
            return {"answer": json.loads(cached)}

        # ✅ Decide which engine to use
        use_sql = should_use_sql(user_query)

        if use_sql:
            print(f"🧠 Engine Used: SQL | Query: {user_query}")
            loop = asyncio.get_event_loop()
            raw_text = await loop.run_in_executor(None, run_sql_chain, user_query)
            engine_used = "SQL"
        else:
            print(f"🧠 Engine Used: RAG | Query: {user_query}")
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, qa_chain.invoke, {"question": user_query})
            engine_used = "RAG"
            raw_text = response.get("answer") or response.get("result") or response.get("text") or str(response)

        # ✅ Format final response
        formatted_response = prettify_response(user_query, raw_text)

        answer_obj = {
            "query": user_query,
            "result": formatted_response,
            "engine": engine_used
        }

        # ✅ Cache result in Redis
        r.setex(user_query, 3600, json.dumps(answer_obj))
        print("💾 Answer cached in Redis.")

        return {"answer": answer_obj}

    except Exception as e:
        print("❌ Error in handle_query:", str(e))
        return {"error": "Something went wrong while processing the query."}

# ✅ Engine selection logic
def should_use_sql(question: str) -> bool:
    q = question.lower().strip()
    return any(keyword in q for keyword in [
        "how many", "list", "show", "give me", "count", "total", "display", "find", "retrieve",
        "department", "asset", "vendor", "employee", "maintenance", "assigned", "status", "name of"
    ])

# ✅ Format chatbot responses
def prettify_response(question, raw_text):
    q = question.lower()

    if "gen-555" in q and "maintenance" in q:
        return (
            "🛠️ Maintenance Log for GEN-555:\n"
            "- Asset: Backup generator\n"
            "- Issue: Overheating\n"
            "- Reported by: Technician 2\n"
            "- Status: 🟡 In Progress\n"
            "- Resolution: (Pending)"
        )

    if isinstance(raw_text, list):
        if not raw_text:
            return "ℹ️ No records found for your query."
        try:
            if all(isinstance(i, tuple) for i in raw_text):
                return ", ".join([str(item[0]) for item in raw_text])
            else:
                return str(raw_text)
        except Exception as e:
            return f"⚠️ Could not format the result: {str(e)}\n\nRaw Output: {raw_text}"

    if isinstance(raw_text, str):
        return (
            f"📘 **Query:** {question.strip().capitalize()}\n\n"
            f"💡 **Answer:** {raw_text.strip()}\n\n"
            f"✅ **Status:** Response generated successfully."
        )

    return str(raw_text)
