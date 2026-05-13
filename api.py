import os
import sys
import tempfile
import shutil

from fastapi import FastAPI, File, UploadFile, Form

sys.path.append(os.path.dirname(__file__))

from src.pipeline import run_pipeline
from src.rag.embedder import get_or_create_vector_store
from src.db.memory import Mongomemory

# --- Load vector store (skips PDF re-ingestion if chroma_db already exists) ---
vector_store = get_or_create_vector_store(os.path.join(os.path.dirname(__file__), "data", "knowledge_base"))

app = FastAPI()


# ---------- GET ----------

@app.get("/")
def home():
    return {"message": "EduHub API is running"}


@app.get("/history")
def get_history(user_id: str, limit: int = 10):
    memory = Mongomemory()
    history = memory.get_history(user_id, limit=limit)
    items = []
    for chat in history:
        items.append({
            "question": chat.get("question", ""),
            "topic": chat.get("router_result", {}).get("topic", "unknown"),
            "verdict": chat.get("verifier_result", {}).get("verdict", "unknown"),
            "timestamp": str(chat.get("timestamp", "")),
        })
    return items


# ---------- POST ----------

@app.post("/solve/text")
def solve_text(question: str = Form(...), user_id: str = Form("api_user")):
    result = run_pipeline(
        raw_input=question,
        input_type="text",
        user_id=user_id,
        vector_store=vector_store,
    )
    return result


@app.post("/solve/image")
def solve_image(file: UploadFile = File(...), user_id: str = Form("api_user")):
    suffix = os.path.splitext(file.filename or "")[1]
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    shutil.copyfileobj(file.file, tmp)
    tmp.close()

    result = run_pipeline(
        raw_input=tmp.name,
        input_type="image",
        user_id=user_id,
        vector_store=vector_store,
    )
    os.remove(tmp.name)
    return result


@app.post("/solve/audio")
def solve_audio(file: UploadFile = File(...), user_id: str = Form("api_user")):
    suffix = os.path.splitext(file.filename or "")[1]
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    shutil.copyfileobj(file.file, tmp)
    tmp.close()

    result = run_pipeline(
        raw_input=tmp.name,
        input_type="audio",
        user_id=user_id,
        vector_store=vector_store,
    )
    os.remove(tmp.name)
    return result


# ---------- PUT ----------

@app.put("/history/update")
def update_user_id(old_user_id: str = Form(...), new_user_id: str = Form(...)):
    """Update user_id across all conversation history entries."""
    memory = Mongomemory()
    result = memory.collection.update_many(
        {"user_id": old_user_id},
        {"$set": {"user_id": new_user_id}},
    )
    return {
        "message": f"Updated {result.modified_count} records from '{old_user_id}' to '{new_user_id}'"
    }
