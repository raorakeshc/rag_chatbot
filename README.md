# Support Chatbot - RAG Application

A smart HR Support Assistant powered by Retrieval-Augmented Generation (RAG) that answers employee questions based on company  documents and policies.

## 🎯 Overview

This application combines advanced AI technologies to provide instant, accurate  support by:
- **Retrieving** relevant information from company  documents
- **Augmenting** queries with document-based context
- **Generating** intelligent, policy-aligned responses using Google's Gemini LLM

## ✨ Features

- 💬 **Conversational UI** - Streamlit-based web interface with message history
- 📚 **Document-Based Responses** - Answers backed by actual  documents
- 🧠 **Context Memory** - Maintains conversation history for coherent multi-turn dialogs
- 🚀 **Fast Retrieval** - FAISS vector database for efficient document search
- 🤖 **AI-Powered** - Google Generative AI (Gemini) for natural language responses
- 🔒 **Policy-Aligned** - Ensures responses follow company guidelines

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Framework** | LangChain (orchestration) |
| **Embeddings** | Hugging Face (sentence-transformers/all-MiniLM-L6-v2) |
| **Vector DB** | FAISS (Facebook AI Similarity Search) |
| **LLM** | Google Generative AI (Gemini 3 Flash) |
| **UI** | Streamlit |
| **Language** | Python 3.x |

## 📋 Prerequisites

- Python 3.9+
- Google API Key (for Gemini LLM)
- HR policy documents in PDF format

## 🚀 Quick Start

### 1. Clone/Setup Project

```bash
cd rag_chatbot
```

### 2. Create Virtual Environment

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Linux/Mac
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

### 5. Prepare Documents

1. Add HR policy PDFs to the `documents/` folder
2. Run the ingestion script to index documents:

```bash
python ingest.py
```

This creates a FAISS vector database in `hr_faiss_index/`

### 6. Run the Application

```bash
streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501`

## 📁 Project Structure

```
rag_chatbot/
├── streamlit_app.py          # Main Streamlit UI
├── hr_core.py                # Core chatbot logic (reusable)
├── chatbot.py                # CLI version
├── chatbot_refactored.py      # Alternative CLI implementation
├── ingest.py                 # Document ingestion & indexing
├── requirements.txt          # Python dependencies
├── .env                       # Environment variables (create this)
├── documents/                # Input: HR policy PDFs
├── hr_faiss_index/           # Output: Vector database
└── __pycache__/              # Python cache
```

## 🔄 How It Works

### Document Ingestion Pipeline
```
PDFs → Extract Text → Split Chunks → Create Embeddings → Store in FAISS
```

### Query Processing
```
User Question → Search FAISS → Retrieve Top 4 Docs → Generate Response with LLM
```

### Data Flow
1. Employee asks a question via Streamlit UI
2. Question is converted to vector embedding
3. FAISS searches vector database for 4 most relevant documents
4. Relevant documents + conversation history → Gemini LLM
5. LLM generates policy-aligned response
6. Response displayed in chat interface

## 🔧 Configuration

### Vector Database Settings
- **Model**: `sentence-transformers/all-MiniLM-L6-v2` (384 dimensions)
- **Chunk Size**: 800 characters
- **Chunk Overlap**: 150 characters
- **Top-K Retrieval**: 4 documents

### LLM Settings
- **Model**: `gemini-3-flash-preview`
- **Temperature**: 0 (deterministic responses)
- **Max Memory**: Last 5 conversation exchanges

## 📦 Requirements

```
langchain==0.3.27
langchain-openai==0.3.33
langchain-community==0.3.24
langchain-huggingface
sentence-transformers
faiss-cpu
streamlit>=1.28.0
python-dotenv
langchain-google-genai
google-generativeai
```

## 🎓 Usage Examples

### Example 1: Leave Policy
**User**: "How many vacation days do I get per year?"
**Bot**: [Retrieves leave policy document] "According to company policy, employees receive 20 paid vacation days annually..."

### Example 2: Benefits
**User**: "What health insurance options are available?"
**Bot**: [Retrieves benefits document] "We offer both HMO and PPO plans with the following coverage..."

### Example 3: Unknown Query
**User**: "What's the CEO's favorite color?"
**Bot**: "I'm not sure based on current HR policies."

## 🧪 Running Conversations

The app maintains conversation memory to provide context-aware responses:

1. **First Turn**: Direct document retrieval
2. **Subsequent Turns**: Consider previous questions/answers
3. **Memory Size**: Last 5 exchanges stored

## 🔐 Security & Privacy

- ✅ Local vector database (no cloud storage)
- ✅ API key stored in `.env` (not in code)
- ✅ Documents processed locally
- ✅ No data logging to third parties

## 🚨 Common Issues

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: langchain_huggingface` | `pip install langchain-huggingface` |
| `ImportError: sentence_transformers` | `pip install sentence-transformers` |
| `GOOGLE_API_KEY not found` | Create `.env` file with valid API key |
| `FAISS index not found` | Run `python ingest.py` first |

## 📊 Performance

- **Response Time**: 2-5 seconds (LLM dependent)
- **Memory Usage**: ~2GB (on first load with embeddings)
- **Concurrent Users**: Single-user (Streamlit limitation)

## 🎯 Advanced Usage

### CLI Version
For command-line interaction without UI:
```bash
python chatbot.py
```

### Custom Prompts
Edit the prompt template in `hr_core.py`:
```python
prompt = ChatPromptTemplate.from_template("""
Your custom system prompt here...
""")
```

### Add More Documents
1. Add PDFs to `documents/` folder
2. Re-run `ingest.py` to rebuild index
3. Restart Streamlit app

## 🤝 Contributing

To extend this project:
1. Modify `ingest.py` to support additional document types
2. Customize `hr_core.py` prompt for different use cases
3. Enhance `streamlit_app.py` UI with additional features

## 📝 License

Private project - For internal use only

## 📞 Support

For issues or questions:
1. Check the requirements are installed
2. Verify `.env` file configuration
3. Ensure documents are in PDF format in `documents/` folder
4. Check API key validity

## 🔄 Architecture Diagram

```
┌─────────────────────────────────────────────┐
│        Streamlit Web UI                      │
│   (streamlit_app.py)                        │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│        Core Logic (hr_core.py)              │
│  - Conversation Memory                      │
│  - Prompt Management                        │
└────────────────┬────────────────────────────┘
                 │
        ┌────────┴────────┐
        │                 │
┌───────▼──────┐   ┌─────▼────────────┐
│ FAISS Vector │   │ Gemini LLM       │
│ Database     │   │ (Google AI)      │
└──────────────┘   └──────────────────┘
        ▲
        │
┌───────┴──────────────────────────────┐
│  Document Ingestion (ingest.py)      │
│  - PDF Loading                        │
│  - Text Chunking                      │
│  - Embedding Generation               │
└───────────────────────────────────────┘
```

<img width="1898" height="802" alt="image" src="https://github.com/user-attachments/assets/724e7649-ccad-4499-8104-cfed5b272d79" />


---

**Version**: 1.0  
**Created**: February 2026  
**Last Updated**: February 19, 2026
