
# 🎓 EduHub — AI-Powered JEE Math Tutor

A multi-agent Retrieval-Augmented Generation (RAG) system that solves JEE math problems<br/>with step-by-step explanations, automatic verification, and multimodal input support.

---

## ✨ Features

| Feature | Description |
|---|---|
| **Multi-Agent Pipeline** | Dedicated agents for parsing, routing, solving, and verifying math problems |
| **RAG-Powered Answers** | Retrieves relevant context from a PDF knowledge base before generating solutions |
| **Multimodal Input** | Accepts **text**, **images** (via OCR), and **audio** (via Whisper) |
| **Automatic Verification** | A separate verifier agent independently re-solves and cross-checks every answer |
| **Human-in-the-Loop (HITL)** | Flags low-confidence answers, unclear problems, and incorrect solutions for human review |
| **Conversation Memory** | Persists all Q&A sessions to MongoDB for history tracking and analytics |
| **Streamlit Dashboard** | Interactive web UI with tabbed solution view, analysis panel, and verification status |

--

### Agent Details

| Agent | Role | Model | Temperature |
|---|---|---|---|
| **Parser** | Extracts structured problem data (text, variables, constraints) | Llama 3.3 70B | 0 |
| **Intent Router** | Classifies topic (probability, algebra, calculus, etc.), difficulty, and solver type | Llama 3.3 70B | 0 |
| **Solver** | Generates step-by-step solution using RAG context | Llama 3.3 70B | 0 |
| **Verifier** | Independently re-solves and validates the solver's answer | Llama 3.3 70B | 0.3 |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **LLM** | [Llama 3.3 70B Versatile](https://groq.com/) via Groq API |
| **Embeddings** | [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) (Sentence Transformers) |
| **Vector Store** | [ChromaDB](https://www.trychroma.com/) with LangChain integration |
| **Orchestration** | [LangChain](https://www.langchain.com/) (Groq, HuggingFace, Chroma, Community loaders) |
| **OCR** | [EasyOCR](https://github.com/JaidedAI/EasyOCR) |
| **Speech-to-Text** | [OpenAI Whisper](https://github.com/openai/whisper) |
| **Database** | [MongoDB Atlas](https://www.mongodb.com/atlas) via PyMongo |
| **Frontend** | [Streamlit](https://streamlit.io/) |
| **Package Manager** | [uv](https://docs.astral.sh/uv/) |

---

<<<<<<< Updated upstream

## 📁 Project Structure


=======
## 📁 Project Structure

```
>>>>>>> Stashed changes
EduHub/
├── app.py                          # Streamlit application entry point
├── pyproject.toml                  # Project metadata & dependencies
├── LICENSE                         # MIT License
│
├── agents/                         # LLM-powered agents
│   ├── parser_agent.py             # Parses raw problem into structured JSON
│   ├── intent_router_agent.py      # Classifies topic, difficulty & solver type
│   ├── solver_agent.py             # Solves the problem using RAG context
│   └── verifier.py                 # Independently verifies the solver's answer
│
├── src/
│   ├── pipeline.py                 # Orchestrates the full agent pipeline
│   │
│   ├── rag/                        # Retrieval-Augmented Generation modules
│   │   ├── data_ingestion.py       # Loads PDFs & splits into deduplicated chunks
│   │   ├── embedder.py             # Creates ChromaDB vector store from chunks
│   │   ├── retriever.py            # Similarity search over vector store
│   │   ├── answer_generator.py     # Standalone RAG answer generator
│   │   └── main.py                 # RAG pipeline test script
│   │
│   ├── multimodal/                 # Input modality handlers
│   │   ├── ocr_transcriber.py      # Image → text via EasyOCR
│   │   └── whisper_transcriber.py  # Audio → text via Whisper
│   │
│   └── db/                         # Database layer
│       └── memory.py               # MongoDB conversation persistence
│
└── data/
    ├── knowledge_base/             # PDF documents for RAG ingestion
    └── chroma_db/                  # Persisted ChromaDB vector store
<<<<<<< Updated upstream

=======
```
>>>>>>> Stashed changes

---

## 🚀 Getting Started

### Prerequisites

- **Python** ≥ 3.11
- **uv** package manager ([install guide](https://docs.astral.sh/uv/getting-started/installation/))
- **Groq API Key** — [Get one here](https://console.groq.com/)
- **MongoDB Atlas URI** — [Create a free cluster](https://www.mongodb.com/atlas)

### 1. Clone the Repository

```bash
git clone https://github.com/Keshav77463/EduHub.git
cd EduHub
```

### 2. Install Dependencies

```bash
uv sync
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
MONGODB_URI=your_mongodb_connection_string_here
DB_NAME=eduhub
```

### 4. Add Knowledge Base Documents

Place your JEE math PDF documents in:

```
data/knowledge_base/
```

These PDFs are automatically ingested, chunked, and embedded into ChromaDB on startup.

### 5. Run the Application

```bash
uv run streamlit run app.py
```

The app will open at **http://localhost:8501**.

---

## 💡 Usage

1. **Set your User ID** in the sidebar (used for conversation history tracking).
2. **Choose an input type**:
   - **Text** — Type or paste your math problem directly.
   - **Image** — Upload a photo of a handwritten or printed problem (PNG/JPG).
   - **Audio** — Upload a voice recording describing the problem (WAV/MP3/M4A).
3. **Click "🚀 Solve Problem"** and view results across three tabs:

| Tab | Contents |
|---|---|
| 📝 **Solution** | Step-by-step answer with confidence score |
| 🔍 **Analysis** | Detected topic, difficulty, and parsed constraints |
| ✅ **Verification** | Independent verification verdict and explanation |

### HITL Alerts

The system automatically triggers Human-in-the-Loop alerts when:
- 🛑 The problem is **unclear** or the topic is **unknown**
- ⚠️ The solver's **confidence is below 70%**
- 🛑 The verifier flags the answer as **incorrect**

<<<<<<< Updated upstream

=======
---
>>>>>>> Stashed changes

## 🔧 Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | API key for Groq LLM inference |
| `MONGODB_URI` | MongoDB Atlas connection string |
| `DB_NAME` | MongoDB database name |
<<<<<<< Updated upstream
-
=======

---
>>>>>>> Stashed changes

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Built with ❤️ for JEE aspirants
<<<<<<< Updated upstream
</p>
=======
</p>
>>>>>>> Stashed changes
