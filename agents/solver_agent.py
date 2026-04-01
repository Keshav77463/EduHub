import os
import sys
import re
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

def extract_json(text):
    """Extract JSON from LLM response that may contain markdown fences or extra text."""
    text = text.strip()
    text = re.sub(r'^```(?:json)?\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r'\{[\s\S]*\}', text)
        if match:
            return json.loads(match.group())
        raise

from src.rag.retriever import retrieve_documents


load_dotenv()

def solve_problem(problem_text, topic, vector_store):
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0
    )
    chunks = retrieve_documents(problem_text, vector_store)

    context = "\n\n".join([doc.page_content for doc in chunks])

    prompt = f"""You are a JEE math solver.
    Use this context to solve the problem.
    Topic: {topic}
    Context: {context}
    Problem: {problem_text}

    Return ONLY this JSON, no markdown, no extra text:
    {{
        "answer": "...",
        "steps": ["step1", "step2"],
        "confidence": 0.9,
        "sources": []
    }}
    IMPORTANT: Return ONLY the JSON object. No other text."""

    # Step 5: invoke + clean + parse
    response = llm.invoke(prompt)
    result = extract_json(response.content)

    # Step 6: HITL check
    if result["confidence"] < 0.7:
        print("⚠️ HITL: Low confidence!")

    return result