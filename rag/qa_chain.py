from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI


def get_retrieval_qa_chain():
    embeddings = OpenAIEmbeddings()
    vectordb = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

    retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 3})

    # ✅ Memory for conversation context
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    qa = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(temperature=0),
        retriever=retriever,
        memory=memory,
        return_source_documents=False,
        verbose=True
    )

    return qa
