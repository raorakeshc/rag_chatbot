import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# -----------------------------------------
# ENV
# -----------------------------------------
load_dotenv()

DATA_FOLDER = "documents"
VECTOR_DB_PATH = "hr_faiss_index"

# -----------------------------------------
# LOAD PDFs
# -----------------------------------------
documents = []

for file in os.listdir(DATA_FOLDER):
    if file.endswith(".pdf"):
        loader = PyPDFLoader(os.path.join(DATA_FOLDER, file))
        documents.extend(loader.load())

print(f"Loaded {len(documents)} pages from PDFs")

# -----------------------------------------
# SPLIT TEXT
# -----------------------------------------
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
)

chunks = text_splitter.split_documents(documents)
print(f"Created {len(chunks)} text chunks")

# -----------------------------------------
# EMBEDDINGS
# -----------------------------------------

embeddings = HuggingFaceEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2")
# -----------------------------------------
# STORE IN VECTOR DB
# -----------------------------------------
vectorstore = FAISS.from_documents(chunks, embeddings)
vectorstore.save_local(VECTOR_DB_PATH)

print("HR knowledge base successfully indexed")
