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

# -----------------------------------------
# ENV
# -----------------------------------------
load_dotenv()

VECTOR_DB_PATH = "hr_faiss_index"

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
)

# -----------------------------------------
# PROMPT
# -----------------------------------------
prompt = ChatPromptTemplate.from_template("""
You are an HR Support Assistant.

Answer employee questions using ONLY the provided company documents.
If the answer is not found in the documents, say:
"I'm not sure based on current HR policies."

Be clear, professional, and policy-aligned.

Conversation History:
{history}

HR Context:
{context}

Employee Question:
{question}
""")


# -----------------------------------------
# CORE FUNCTION (Reusable)
# -----------------------------------------
def get_response(question: str, memory: deque) -> str:
    """
    Get a response from the HR chatbot.
    
    Args:
        question: User's question
        memory: deque object to track conversation history
    
    Returns:
        Response text from the LLM
    """
    docs = retriever.invoke(question)
    context = "\n\n".join(doc.page_content for doc in docs)

    # format conversation history for prompt
    history_text = "\n\n".join(
        f"Employee: {q}\nHR Bot: {a}" for q, a in memory
    )

    response = llm.invoke(
        prompt.format_messages(
            context=context,
            question=question,
            history=history_text,
        )
    )

    return response.content
