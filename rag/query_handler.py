from rag.qa_chain import create_qa_chain

qa_chain = create_qa_chain()  # Load once when server starts

async def handle_query(q: str):
    print("Received query:", q)

    try:
        response = qa_chain.invoke(q)  # invoke returns the answer string or dict
        # Wrap the response inside a dict with query and result keys
        return {
            "answer": {
                "query": q,
                "result": response if isinstance(response, str) else str(response)
            }
        }
    except Exception as e:
        print("Error in handle_query:", str(e))
        return {"error": "Something went wrong while processing the query."}
