"""
Core HR Chatbot logic - extracted for reuse in CLI and Streamlit UI.
"""
import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from collections import deque
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
from functools import lru_cache

# -----------------------------------------
# ENV
# -----------------------------------------
load_dotenv()

VECTOR_DB_PATH = "faiss_index"

# -----------------------------------------
# LOAD VECTOR DB
# -----------------------------------------
embeddings = HuggingFaceEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2")

vectorstore = FAISS.load_local(
    VECTOR_DB_PATH,
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# -----------------------------------------
# LLM
# -----------------------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY")
    #google_api_key = st.secrets["GOOGLE_API_KEY"]
)

# -----------------------------------------
# PROMPT
# -----------------------------------------
prompt = ChatPromptTemplate.from_template("""
You are an Support Assistant.

Answer questions using ONLY the provided  documents.
If the answer is not found in the documents, say:
"I'm not sure based on current information available."

Be clear, professional, and aligned with the information provided.

Conversation History:
{history}

Context:
{context}

Question:
{question}
""")



@lru_cache(maxsize=128)
def get_relevant_docs(question: str) -> str:
    """
    Retrieve relevant documents from the vector store based on the question, with caching.
    """
    print(f"CHACHE-DEBUG: Retrieving docs for question: {question}")
    docs = retriever.invoke(question)
    return "\n\n".join(doc.page_content for doc in docs)
# -----------------------------------------
# CORE FUNCTION (Reusable)
# -----------------------------------------
def get_response(question: str, memory: tuple) -> str:
    """
    Get a response from the HR chatbot.
    
    Args:
        question: User's question
        memory: deque object to track conversation history
    
    Returns:
        Response text from the LLM
    """
    context = get_relevant_docs(question)
    #docs = retriever.invoke(question)
    #context = "\n\n".join(doc.page_content for doc in docs)

    # format conversation history for prompt
    history_text = "\n\n".join(
        f"User: {q}\nAssistant: {a}" for q, a in memory
    )

    response = llm.invoke(
        prompt.format_messages(
            context=context,
            question=question,
            history=history_text,
        )
    )

    return response.content
