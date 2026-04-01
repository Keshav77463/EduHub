import os
import re
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

def extract_json(text):
    """Extract JSON from LLM response that may contain markdown fences or extra text."""
    text = text.strip()
    # Remove markdown code fences
    text = re.sub(r'^```(?:json)?\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Try to find a JSON object in the text
        match = re.search(r'\{[\s\S]*\}', text)
        if match:
            return json.loads(match.group())
        raise
def parse_problem(raw_problem):
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0
    )
    prompt = f"""You are a math problem parser.
    Parse this problem and return ONLY valid JSON with no extra text, 
    no markdown, no ```json blocks, just pure JSON:

    Problem: {raw_problem}

    Return this exact JSON format:
    {{
        "problem_text": "...",
        "topic": "...",
        "variables": [],
        "constraints": [],
        "needs_clarification": false
    }}"""
    response = llm.invoke(prompt)
    result = extract_json(response.content)
    if result["needs_clarification"] == True:
        print("HITL triggered: problem needs clarification")
    return result


